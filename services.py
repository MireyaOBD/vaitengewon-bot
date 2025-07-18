# services.py

import gspread
import json
import os
import traceback
import requests
from openai import OpenAI
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- FUNCIÓN CORREGIDA PARA GOOGLE SHEETS ---
def _get_gspread_client():
    """Obtiene el cliente de gspread usando las credenciales de la variable de entorno."""
    try:
        creds_json_str = os.getenv("GSPREAD_CREDENTIALS_JSON")
        if not creds_json_str:
            print("--- ERROR CRÍTICO: La variable de entorno 'GSPREAD_CREDENTIALS_JSON' no está definida. ---")
            return None
        
        creds_dict = json.loads(creds_json_str)
        client = gspread.service_account_from_dict(creds_dict)
        print("--- Conexión con Google Sheets exitosa usando variables de entorno. ---")
        return client
    except json.JSONDecodeError:
        print("--- ERROR CRÍTICO: El contenido de 'GSPREAD_CREDENTIALS_JSON' no es un JSON válido. ---")
        return None
    except Exception as e:
        print(f"--- ERROR CRÍTICO al conectar con Google Sheets: {e} ---")
        return None

def gspread_append_row(sheet_name: str, data: dict):
    try:
        client = _get_gspread_client()
        if not client: return False # El error ya se imprimió

        spreadsheet = client.open_by_key("1UrYTSD6b1AF-mEarlfZlgDRXazwP2Xau9sMtpBhXHLA")
        worksheet = spreadsheet.worksheet(sheet_name)
        headers = worksheet.row_values(1)
        row_to_insert = [data.get(header, "") for header in headers]
        worksheet.append_row(row_to_insert)
        print(f"Fila añadida a la hoja '{sheet_name}'.")
        return True
    except Exception as e:
        print(f"--- ERROR AL AÑADIR FILA EN GOOGLE SHEETS ('{sheet_name}'): {e} ---")
        return False

def gspread_update_row(sheet_name: str, user_id: str, update_data: dict):
    try:
        client = _get_gspread_client()
        if not client: return False

        spreadsheet = client.open_by_key("1UrYTSD6b1AF-mEarlfZlgDRXazwP2Xau9sMtpBhXHLA")
        worksheet = spreadsheet.worksheet(sheet_name)
        
        headers = worksheet.row_values(1)
        try:
            user_id_col_index = headers.index("UserID") + 1
        except ValueError:
            print(f"Error: No se encontró el encabezado 'UserID' en la hoja '{sheet_name}'.")
            return False

        cell = worksheet.find(user_id, in_column=user_id_col_index)
        if not cell:
            print(f"No se encontró el UserID '{user_id}' en la hoja '{sheet_name}'.")
            return False

        for column_name, value in update_data.items():
            if column_name in headers:
                col_index = headers.index(column_name) + 1
                worksheet.update_cell(cell.row, col_index, value)
        
        print(f"Fila para UserID '{user_id}' actualizada en '{sheet_name}'.")
        return True
    except Exception as e:
        print(f"--- ERROR AL ACTUALIZAR FILA EN GOOGLE SHEETS ('{sheet_name}'): {e} ---")
        return False

def gspread_get_row_by_userid(sheet_name: str, user_id: str):
    try:
        client = _get_gspread_client()
        if not client: return None

        spreadsheet = client.open_by_key("1UrYTSD6b1AF-mEarlfZlgDRXazwP2Xau9sMtpBhXHLA")
        worksheet = spreadsheet.worksheet(sheet_name)
        
        headers = worksheet.row_values(1)
        user_id_col_index = headers.index("UserID") + 1
        cell = worksheet.find(user_id, in_column=user_id_col_index)
        if not cell: return None
        row_values = worksheet.row_values(cell.row)
        row_data = dict(zip(headers, row_values))
        print(f"Datos obtenidos para UserID '{user_id}' de la hoja '{sheet_name}'.")
        return row_data
    except Exception as e:
        print(f"--- ERROR AL OBTENER FILA DE GOOGLE SHEETS ('{sheet_name}'): {e} ---")
        return None

def openai_generate_text(prompt: str, model: str = "gpt-4o", response_format: str = "text"):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        print(f"--- Enviando prompt a OpenAI (Modelo: {model}, Formato: {response_format}) ---")
        completion_params = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        if response_format == "json_object":
            completion_params["response_format"] = {"type": "json_object"}
        response = client.chat.completions.create(**completion_params)
        content_str = response.choices[0].message.content
        print("--- Respuesta recibida de OpenAI ---")
        if response_format == "json_object":
            return json.loads(content_str)
        else:
            return content_str.strip()
    except Exception as e:
        print(f"--- ERROR DE OPENAI ---\n{e}")
        return None

def notion_create_database(user_id: str):
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    PARENT_PAGE_ID = "22a97e5bdfff80e5b25defc2812a24ef"
    url = "https://api.notion.com/v1/databases"
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}
    payload = {
        "parent": {"page_id": PARENT_PAGE_ID},
        "title": [{"type": "text", "text": {"content": f"Vaitengewon Map para {user_id}"}}],
        "properties": {
            "Módulo": {"title": {}},
            "Index": {"select": {"options": [
                {"name": "ADMINISTRACIÓN", "color": "brown"}, {"name": "ESENCIA", "color": "pink"},
                {"name": "INFRAESTRUCTURA WEB", "color": "blue"}, {"name": "MARCA", "color": "green"},
                {"name": "MARKETING", "color": "purple"}, {"name": "MODELO DE NEGOCIO", "color": "blue"},
                {"name": "PRODUCTO", "color": "gray"}, {"name": "PROGRAMA", "color": "orange"},
                {"name": "PROYECTO", "color": "red"}
            ]}}
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        db_id = response_data["id"]
        db_url = response_data["url"]
        print(f"Base de datos de Notion creada. ID: {db_id}")
        return {"db_id": db_id, "db_url": db_url}
    except requests.exceptions.RequestException as e:
        print(f"--- ERROR AL CREAR DB EN NOTION ---\nError: {e}\nRespuesta: {response.text if 'response' in locals() else 'N/A'}")
        return None
    
def notion_create_page(database_id: str, title: str, content_text: str, index_name: str):
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    url = "https://api.notion.com/v1/pages"
    headers = {"Authorization": f"Bearer {NOTION_API_KEY}", "Content-Type": "application/json", "Notion-Version": "2022-06-28"}

    MAX_LENGTH = 2000
    content_chunks = [content_text[i:i+MAX_LENGTH] for i in range(0, len(content_text), MAX_LENGTH)]
    
    blocks = []
    for chunk in content_chunks:
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": chunk}}]
            }
        })

    properties = {
        "Módulo": {"title": [{"text": {"content": title}}]},
        "Index": {"select": {"name": index_name}}
    }
    payload = {"parent": {"database_id": database_id}, "properties": properties, "children": blocks}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Página de Notion '{title}' creada exitosamente.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"--- ERROR AL CREAR PÁGINA EN NOTION '{title}' ---\nError: {e}\nRespuesta: {response.text if 'response' in locals() else 'N/A'}")
        return None

def send_email(to_address: str, subject: str, html_body: str):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all([smtp_host, smtp_port, smtp_user, smtp_password]):
        print("--- ERROR DE EMAIL: Faltan credenciales SMTP en las variables de entorno. ---")
        return False
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = to_address
    part = MIMEText(html_body, 'html')
    msg.attach(part)

    try:
        print(f"--- Conectando a {smtp_host} en puerto {smtp_port} con SSL ---")
        with smtplib.SMTP_SSL(smtp_host, int(smtp_port)) as server:
            server.login(smtp_user, smtp_password)
            print(f"--- Enviando email a {to_address} ---")
            server.sendmail(smtp_user, to_address, msg.as_string())
        
        print("--- Email enviado exitosamente ---")
        return True
    except Exception as e:
        print(f"--- ERROR AL ENVIAR EMAIL: {e} ---")
        return False