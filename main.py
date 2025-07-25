# main.py
import os
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from dotenv import load_dotenv
import services
import workflows
from fastapi.middleware.cors import CORSMiddleware # ÚNICA IMPORTACIÓN NUEVA

load_dotenv()

class ChatInput(BaseModel):
    # Usamos tu definición original, que es sintácticamente correcta.
    UserID: str; Answer1: str; Answer2: str; Answer3: str; Answer4: str; Answer5: str; Answer6: str

app = FastAPI(title="Vaitengewon Bot API")

# ==============================================================================
# AQUÍ VA EL BLOQUE DE CORS - Justo después de crear 'app'
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
        # --- NUEVO PASO: Enviar confirmación de respuestas al usuario ---
        workflows.send_user_answers_email(chat_data)
        # --- FIN DEL NUEVO PASO ---

    # Fases 01 y 02: Configuración
    initial_sheet_data = {
        "UserID": user_id, "ConversationState": "6", "Answer1": chat_data['Answer1'],
        "Answer2": chat_data['Answer2'], "Answer3": chat_data['Answer3'], "Answer4": chat_data['Answer4'],
        "Answer5": chat_data['Answer5'], "userEmail": chat_data['Answer6'], "lastUpdate": datetime.now().isoformat()
    }
    services.gspread_append_row("INICIO", initial_sheet_data)
    db_info = services.notion_create_database(user_id)
    if not db_info: return

    update_data = {"NotionDBReady": "TRUE", "dbID": db_info["db_id"], "NotionDB_URL": db_info["db_url"]}
    services.gspread_update_row("INICIO", user_id, update_data)
    print(f"[{user_id}] - Configuración inicial completada.")

    # Fase 03: Generación de Esencia
    if not workflows.run_f03_generate_esencia(user_id=user_id, db_id=db_info["db_id"], idea_negocio=chat_data['Answer2']): return
    
    # Fase 04: Generación del Modelo de Negocio
    if not workflows.run_f04_generate_business_model(user_id=user_id, db_id=db_info["db_id"]): return

    # Fase 05: Generación del PMV
    if not workflows.run_f05_generate_pmv(user_id=user_id, db_id=db_info["db_id"]): return
    
    # Fase 06: Envío de Notificación
    workflows.run_f06_send_notification(user_id=user_id)

    print(f"[{user_id}] - Flujo de trabajo completo finalizado.")

@app.post("/webhook/vaitengewon-bot")
async def start_vaitengewon_process(chat_data: ChatInput, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_vaitengewon_workflow, chat_data.dict())
    return {"status": "success", "message": "Proceso iniciado en segundo plano."}
    
@app.get("/")
def read_root():
    return {"message": "Servidor del Vaitengewon Bot está funcionando."}