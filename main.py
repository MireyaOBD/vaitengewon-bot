# main.py

import os
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from dotenv import load_dotenv
import services
import workflows
from fastapi.middleware.cors import CORSMiddleware
import traceback 

load_dotenv()

class ChatInput(BaseModel):
    UserID: str; Answer1: str; Answer2: str; Answer3: str; Answer4: str; Answer5: str; Answer6: str

app = FastAPI(title="Vaitengewon Bot API")

# ==============================================================================
# BLOQUE DE CORS
# ==============================================================================
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ==============================================================================

def run_vaitengewon_workflow(chat_data: dict):
    user_id = chat_data['UserID']
    print(f"[{user_id}] - ✅ INICIANDO FLUJO DE TRABAJO COMPLETO...")

    try:
        workflows.send_user_answers_email(chat_data)

        # --- FASE DE CONFIGURACIÓN INICIAL ---
        db_info = services.notion_create_database(user_id)
        if not db_info:
            print(f"[{user_id}] - ❌ DETENIDO: Fallo crítico al crear la base de datos en Notion.")
            return

        # --- GUARDADO INICIAL EN HOJA 'INICIO' (CÓDIGO RESTAURADO) ---
        print(f"[{user_id}] - ...Guardando respuestas iniciales en la hoja 'INICIO'...")
        initial_sheet_data = {
            "UserID": user_id, "ConversationState": "6", "Answer1": chat_data['Answer1'],
            "Answer2": chat_data['Answer2'], "Answer3": chat_data['Answer3'], "Answer4": chat_data['Answer4'],
            "Answer5": chat_data['Answer5'], "userEmail": chat_data['Answer6'], 
            "lastUpdate": datetime.now().isoformat(),
            "NotionDB_URL": db_info.get("db_url"),
            "dbID": db_info.get("db_id")
        }
        if not services.gspread_append_row("INICIO", initial_sheet_data):
                print(f"[{user_id}] - ❌ DETENIDO: Fallo al escribir la fila inicial en Google Sheets 'INICIO'.")
                return
        print(f"[{user_id}] - ✅ Respuestas iniciales guardadas en 'INICIO'.")
        
        # Preparamos el contexto inicial para el primer bloque
        contexto_inicial = {
            "idea_negocio": chat_data.get("Answer2"),
            "que_vende": chat_data.get("Answer2"),
            "a_quien_vende": chat_data.get("Answer4"),
            "producto_principal": chat_data.get("Answer3")
        }
        
        print(f"[{user_id}] - ✅ Configuración inicial completada. DB ID: {db_info.get('db_id')}")

        # --- BLOQUE 1: ESENCIA ---
        contexto_post_esencia = workflows.run_esencia_block(
            user_id=user_id, 
            db_id=db_info.get("db_id"), 
            contexto_inicial=contexto_inicial
        )
        if not contexto_post_esencia:
            print(f"[{user_id}] - ❌ DETENIDO: El bloque ESENCIA falló.")
            return

        # --- BLOQUE 2: MODELO DE NEGOCIO ---
        contexto_post_modelo = workflows.run_business_model_block(
            user_id=user_id,
            db_id=db_info.get("db_id"),
            contexto_inicial=contexto_post_esencia
        )
        if not contexto_post_modelo:
            print(f"[{user_id}] - ❌ DETENIDO: El bloque MODELO DE NEGOCIO falló.")
            return
        
        # --- BLOQUE 3: MVP ---
        contexto_post_mvp = workflows.run_mvp_block(
            user_id=user_id,
            db_id=db_info.get("db_id"),
            contexto_inicial=contexto_post_modelo
        )
        if not contexto_post_mvp:
            print(f"[{user_id}] - ❌ DETENIDO: El bloque MVP falló.")
            return

        # --- FASE FINAL: Notificación de finalización ---
        if not workflows.run_f06_send_notification(user_id=user_id):
            print(f"[{user_id}] - ⚠️ ADVERTENCIA: La notificación final falló.")

        print(f"[{user_id}] - ✅🎉 FLUJO DE TRABAJO COMPLETO FINALIZADO CON ÉXITO.")

    except Exception as e:
        print(f"[{user_id}] - 🔥🔥🔥 ERROR INESPERADO Y FATAL EN EL WORKFLOW: {e} 🔥🔥🔥")
        traceback.print_exc()

# En main.py (rama develop), añade esto al final del archivo

# ==============================================================================
# 6. DEFINICIÓN DE RUTAS (ENDPOINTS)
# ==============================================================================
@app.post("/webhook/vaitengewon-bot")
async def start_vaitengewon_process(chat_data: ChatInput, background_tasks: BackgroundTasks):
    """
    Este endpoint recibe los datos del chat y dispara el workflow completo en segundo plano.
    """
    background_tasks.add_task(run_vaitengewon_workflow, chat_data.dict())
    return {"status": "success", "message": "Proceso iniciado en segundo plano."}
    
@app.get("/")
def read_root():
    """
    Endpoint raíz para verificar que el servidor está activo.
    """
    return {"message": "Servidor del Vaitengewon Bot está funcionando."}