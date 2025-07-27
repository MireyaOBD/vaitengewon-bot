# utils.py

import json

def json_to_markdown(data_input):
    """
    Convierte de forma robusta un objeto JSON (o un string JSON) 
    a un formato de texto Markdown legible, ideal para Notion.
    """
    markdown_output = ""
    
    try:
        # Asegurarse de que tenemos un objeto Python (dict o list) para trabajar
        if isinstance(data_input, str):
            try:
                data = json.loads(data_input)
            except json.JSONDecodeError:
                # Si no es un JSON válido, devolver el string tal cual
                return data_input
        elif isinstance(data_input, (dict, list)):
            data = data_input
        else:
            # Si es otro tipo de dato, lo convertimos a string
            return str(data_input)

        # Función recursiva interna para procesar el JSON
        def _process_item(item, level=0):
            nonlocal markdown_output
            
            if isinstance(item, dict):
                for key, value in item.items():
                    # Usar ## para títulos principales y ### para subtítulos
                    header_prefix = "##" if level == 0 else "###"
                    # Formatear la clave para que sea un buen título
                    formatted_key = str(key).replace('_', ' ').title()
                    markdown_output += f"{header_prefix} {formatted_key}\n\n"
                    # Llamada recursiva para procesar el valor
                    _process_item(value, level + 1)
            
            elif isinstance(item, list):
                # Procesar cada elemento de la lista
                for list_item in item:
                    # Si el elemento de la lista es un diccionario, procesarlo directamente
                    if isinstance(list_item, dict):
                         # Añadir un separador para diferenciar elementos de la lista
                        markdown_output += "---\n"
                        _process_item(list_item, level)
                    else:
                        # Si es un valor simple, añadirlo como un punto de viñeta
                        markdown_output += f"- {str(list_item)}\n"
                markdown_output += "\n" # Espacio después de una lista

            else:
                # Si es un valor simple (string, número, etc.), añadirlo como un párrafo
                markdown_output += f"{str(item)}\n\n"

        _process_item(data)
        return markdown_output.strip()

    except Exception as e:
        print(f"--- ERROR Inesperado al convertir JSON a Markdown: {e} ---")
        # Como plan B, si algo falla, devolvemos el JSON formateado para no perder la información
        return json.dumps(data_input, indent=2, ensure_ascii=False)
    
    # ==============================================================================
# ¡NUEVA FUNCIÓN! - AÑADE ESTO A TU ARCHIVO UTILS.PY
# ==============================================================================
def markdown_to_notion_blocks(markdown_text):
    """
    Convierte un string de texto en formato Markdown simple
    a una lista de bloques compatibles con la API de Notion.
    """
    blocks = []
    # Dividimos el texto en líneas para procesar cada una
    for line in markdown_text.strip().split('\n'):
        stripped_line = line.strip()
        if not stripped_line:
            continue

        if stripped_line.startswith('## '):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": stripped_line.replace('## ', '')}}]
                }
            })
        elif stripped_line.startswith('### '):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": stripped_line.replace('### ', '')}}]
                }
            })
        elif stripped_line == '---':
            blocks.append({
                "object": "block",
                "type": "divider",
                "divider": {}
            })
        elif stripped_line.startswith('- '):
             blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": stripped_line.replace('- ', '')}}]
                }
            })
        else:
            # Cualquier otra línea se trata como un párrafo
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": stripped_line}}]
                }
            })
    return blocks
