# main.py

import os
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from dotenv import load_dotenv
import services
import workflows
from fastapi.middleware.cors import CORSMiddleware
import traceback # <--- IMPORTACIÓN NECESARIA PARA MANEJAR ERRORES

load_dotenv()

class ChatInput(BaseModel):
    # Usamos tu definición original, que es sintácticamente correcta.
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

# En main.py

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

        # Preparamos el contexto inicial con las respuestas del chat
        contexto_inicial = {
            "idea_negocio": chat_data.get("Answer2"),
            "que_vende": chat_data.get("Answer2"), # O puedes usar Answer3 si es más específico
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

        # (Aquí llamaremos a los siguientes bloques en el futuro)
        # --- BLOQUE 2: MODELO DE NEGOCIO ---
        # contexto_post_modelo = workflows.run_business_model_block(...)
        
        # --- BLOQUE 3: MVP ---
        # contexto_post_mvp = workflows.run_mvp_block(...)

        # Fase Final: Envío de Notificación (la moveremos al final de todo el flujo)
        # if not workflows.run_f06_send_notification(user_id=user_id):
        #     print(f"[{user_id}] - ❌ DETENIDO: La Fase Final (Notificación) falló.")
        #     return

        print(f"[{user_id}] - ✅🎉 FASES IMPLEMENTADAS HASTA AHORA, FINALIZADAS.")

    except Exception as e:
        print(f"[{user_id}] - 🔥🔥🔥 ERROR INESPERADO Y FATAL EN EL WORKFLOW: {e} 🔥🔥🔥")
        traceback.print_exc()