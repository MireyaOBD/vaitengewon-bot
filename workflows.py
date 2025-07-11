# workflows.py
import services
from datetime import datetime
import json

# --- PROMTS FASE 03: ESENCIA ---
PROMPT_PROPOSITO = """
Eres un experto en estrategia de marca y storytelling. Basándote en la siguiente idea de negocio:
"{idea_negocio}"
Formula un "Propósito" claro e inspirador. Responde únicamente con el texto del propósito.
IMPORTANTE: La longitud total de la respuesta no debe exceder los 1980 caracteres. Resume si es necesario.
"""
PROMPT_MISION = """
Eres un estratega de negocios. El propósito de la empresa es: "{proposito}". La idea de negocio es: "{idea_negocio}".
Basado en esto, redacta una Misión que describa QUÉ hace la empresa, A QUIÉN sirve y CÓMO lo hace.
Responde únicamente con el texto de la misión.
IMPORTANTE: La longitud total de la respuesta no debe exceder los 1980 caracteres. Resume si es necesario.
"""
PROMPT_VISION = """
Eres un líder visionario. El propósito es: "{proposito}". La misión es: "{mision}".
Redacta una declaración de Visión inspiradora a largo plazo que describa el impacto ideal que la empresa busca crear.
Responde únicamente con el texto de la visión.
IMPORTANTE: La longitud total de la respuesta no debe exceder los 1980 caracteres. Resume si es necesario.
"""
PROMPT_VALORES = """
Eres un experto en cultura organizacional. El propósito, misión y visión son:
Propósito: "{proposito}"
Misión: "{mision}"
Visión: "{vision}"
Define 5 valores fundamentales que guiarán las acciones de la empresa.
Responde únicamente con los 5 valores, en una lista separada por comas, y una breve explicación de cada uno.
IMPORTANTE: La longitud total de la respuesta no debe exceder los 1980 caracteres. Resume si es necesario.
"""

# --- PROMTS FASE 04: MODELO DE NEGOCIO ---
PROMPT_CLIENTE = """
Eres un experto en estrategia de marketing y "customer research". Tu tarea es analizar un concepto de negocio y generar un perfil de cliente completo, incluyendo un mapa de empatía.
**Contexto del Negocio:**
- Idea de Negocio: {Answer2}
- Producto Propuesto: {Answer3}
- Mercado Objetivo: {Answer4}
- Propósito de la marca: {Propósito}
- Misión de la marca: {Misión}
**Tu Tarea:**
Basándote en el contexto, genera una respuesta en formato JSON. El objeto JSON debe tener dos claves principales: "perfil_cliente" y "mapa_empatia".
1.  **"perfil_cliente"**: Un objeto con las claves "arquetipo_nombre", "geografica", "demografica", "psicografica", "conductual".
2.  **"mapa_empatia"**: Un objeto con las claves "piensa_y_siente", "ve", "oye", "dice_y_hace", "esfuerzos", "resultados".
Genera únicamente el objeto JSON como respuesta, sin texto introductorio ni explicaciones.
IMPORTANTE: La longitud total de la respuesta JSON, convertida a texto, no debe exceder los 1980 caracteres. Para lograrlo, resume las descripciones y justificaciones, pero mantén la estructura completa del JSON solicitado.
"""
PROMPT_PROPUESTA_VALOR = """
Eres un experto en estrategia de producto y marketing narrativo, especializado en el framework de Propuesta de Valor de Osterwalder.
**Contexto del Negocio y Cliente:**
- Idea de Negocio: {Answer2}
- Propósito de Marca: {Propósito}
- Perfil del Cliente: {cliente_perfil}
- Dolores y Frustraciones del Cliente: {cliente_esfuerzos}
- Deseos y Metas del Cliente: {cliente_resultados}
**Tu Tarea:**
Basándote estrictamente en el contexto, genera una respuesta en formato JSON. El objeto JSON debe tener cuatro claves principales: "propuesta_de_valor", "aliviadores_de_frustraciones", "creadores_de_alegrias" y "transformacion_cliente".
IMPORTANTE: La longitud total de la respuesta JSON, convertida a texto, no debe exceder los 1980 caracteres. Para lograrlo, resume las descripciones y justificaciones, pero mantén la estructura completa del JSON solicitado.
"""
PROMPT_FUENTES_INGRESOS = """
Eres un consultor de modelos de negocio, especializado en estrategias de monetización.
**Contexto:**
- Idea de Negocio: {Answer2}
- Cliente: {cliente_perfil}
- Propuesta de Valor: {propuesta_de_valor}
**Tu Tarea:**
Genera un JSON con dos claves: "fuente_principal" y "fuentes_secundarias". Para la principal, describe el modelo de ingresos más lógico y justifícalo. Para las secundarias, sugiere 2 o 3 modelos complementarios a explorar.
IMPORTANTE: La longitud total de la respuesta JSON, convertida a texto, no debe exceder los 1980 caracteres. Para lograrlo, resume las descripciones y justificaciones, pero mantén la estructura completa del JSON solicitado.
"""
PROMPT_INNOVACION = """
Eres un consultor de innovación y estrategia.
**Contexto:**
- Idea de Negocio: {Answer2}
- Propuesta de Valor: {propuesta_de_valor}
- Modelo de Ingresos: {fuentes_ingresos_principal}
**Tu Tarea:**
Genera un JSON con tres claves: "foco_innovacion", "tipo_innovacion" y "justificacion". Para "foco", elige UNA de: Modelo de Ingresos, Red, Estructura, Procesos, Desempeño del Producto, Sistema del Producto, Servicio, Canales, Marca, Compromiso del Cliente. Para "tipo", elige UNA de: Incremental, Radical, Disruptiva. Justifica brevemente la elección.
IMPORTANTE: La longitud total de la respuesta JSON, convertida a texto, no debe exceder los 1980 caracteres. Para lograrlo, resume las descripciones y justificaciones, pero mantén la estructura completa del JSON solicitado.
"""
PROMPT_CANALES = """
Eres un experto en estrategia de canales y marketing "go-to-market".
**Contexto:**
- Idea de Negocio: {Answer2}
- Cliente: {cliente_perfil}
- Propuesta de Valor: {propuesta_de_valor}
**Tu Tarea:**
Genera un JSON con una clave "fases_del_canal", que sea un objeto con 5 claves: "conocimiento", "evaluacion", "compra", "entrega", y "postventa". Para cada una, propón el canal o táctica más efectiva.
IMPORTANTE: La longitud total de la respuesta JSON, convertida a texto, no debe exceder los 1980 caracteres. Para lograrlo, resume las descripciones y justificaciones, pero mantén la estructura completa del JSON solicitado.
"""
PROMPT_RELACIONES_CLIENTES = """
Eres un Director de Crecimiento (Chief Growth Officer).
**Contexto:**
- Propósito de Marca: {Propósito}
- Cliente: {cliente_perfil}
- Canales: {canales_conocimiento}
**Tu Tarea:**
Genera un JSON con tres claves: "plan_captacion", "plan_fidelizacion", y "plan_estimulacion". Para captación, detalla una táctica para web, proactiva, networking y publicidad. Para fidelización, un plan para apóstoles, leales y detractores. Para estimulación, una táctica para aumentar frecuencia y otra para aumentar valor.
IMPORTANTE: La longitud total de la respuesta JSON, convertida a texto, no debe exceder los 1980 caracteres. Para lograrlo, resume las descripciones y justificaciones, pero mantén la estructura completa del JSON solicitado.
"""
PROMPT_ASOCIACIONES_CLAVE = """
Eres un estratega de desarrollo de negocios.
**Contexto:**
- Idea de Negocio: {Answer2}
- Cliente: {cliente_perfil}
- Propuesta de Valor: {propuesta_de_valor}
**Tu Tarea:**
Genera un JSON con una clave "asociaciones_clave", que sea un objeto con 4 claves: "alianza_estrategica_no_competidor", "alianza_con_proveedor_clave", "coopeticion", "joint_venture_futura". Para cada una, describe el socio ideal y cómo la alianza crea una ventaja competitiva.
IMPORTANTE: La longitud total de la respuesta JSON, convertida a texto, no debe exceder los 1980 caracteres. Para lograrlo, resume las descripciones y justificaciones, pero mantén la estructura completa del JSON solicitado.
"""
PROMPT_ACTIVIDADES_CLAVE = """
Eres un Director de Operaciones (COO).
**Contexto:**
- Propuesta de Valor: {propuesta_de_valor}
- Canales: {canales_fases}
- Relaciones: {relaciones_clientes}
- Asociaciones: {asociaciones_clave}
**Tu Tarea:**
Genera un JSON con una clave "actividades_clave", que sea un objeto con 3 claves: "produccion_y_servicio", "marketing_y_ventas", "soporte_y_alianzas". Para cada una, identifica la actividad más CRÍTICA que el negocio debe ejecutar.
IMPORTANTE: La longitud total de la respuesta JSON, convertida a texto, no debe exceder los 1980 caracteres. Para lograrlo, resume las descripciones y justificaciones, pero mantén la estructura completa del JSON solicitado.
"""
PROMPT_RECURSOS_CLAVE = """
Eres un planificador de negocios y estratega de recursos.
**Contexto:**
- Propuesta de Valor: {propuesta_de_valor}
- Actividades Clave: {actividades_clave}
**Tu Tarea:**
Genera un JSON con una clave "recursos_clave", que sea un objeto con 5 claves: "fisicos", "intelectuales", "humanos", "financieros" y "palancas_de_produccion". Para "palancas", define la "economia_de_escala" y la "economia_de_campo" del negocio.
IMPORTANTE: La longitud total de la respuesta JSON, convertida a texto, no debe exceder los 1980 caracteres. Para lograrlo, resume las descripciones y justificaciones, pero mantén la estructura completa del JSON solicitado.
"""
PROMPT_ESTRUCTURA_COSTES = """
Eres un Director Financiero (CFO).
**Contexto:**
- Actividades Clave: {actividades_clave}
- Recursos Clave: {recursos_clave}
**Tu Tarea:**
Genera un JSON con una clave "estructura_de_costes", que sea un objeto con 3 claves: "coste_mas_importante", "principales_costes_fijos", "principales_costes_variables". Identifica el coste principal y lista 2-3 ejemplos para los fijos y variables.
IMPORTANTE: La longitud total de la respuesta JSON, convertida a texto, no debe exceder los 1980 caracteres. Para lograrlo, resume las descripciones y justificaciones, pero mantén la estructura completa del JSON solicitado.
"""
PROMPT_STAKEHOLDERS = """
Eres un analista de estrategia corporativa y relaciones públicas.
**Contexto:**
- Idea de Negocio: {Answer2}
- Propósito y Valores: {Propósito} y {Valores}
- Actividades Clave: {actividades_clave}
**Tu Tarea:**
Genera un JSON con una clave "analisis_stakeholders", que sea una lista de 3 objetos. Cada objeto debe tener las claves "stakeholder" (el grupo de interés) e "interes_e_impacto" (por qué es importante).
IMPORTANTE: La longitud total de la respuesta JSON, convertida a texto, no debe exceder los 1980 caracteres. Para lograrlo, resume las descripciones y justificaciones, pero mantén la estructura completa del JSON solicitado.
"""
PROMPT_COMPETENCIA = """
Eres un analista de inteligencia competitiva.
**Contexto:**
- Idea de Negocio: {Answer2}
- Propuesta de Valor: {propuesta_de_valor}
- Cliente: {cliente_perfil}
**Tu Tarea:**
Genera un JSON con una clave "analisis_competencia", que sea un objeto con 2 claves: "competidores_directos" y "competidores_indirectos". Para cada uno, incluye "descripcion", "fortaleza_clave" y "debilidad_clave".
IMPORTANTE: La longitud total de la respuesta JSON, convertida a texto, no debe exceder los 1980 caracteres. Para lograrlo, resume las descripciones y justificaciones, pero mantén la estructura completa del JSON solicitado.
"""
PROMPT_DIFERENCIADOR = """
Eres un estratega de posicionamiento de marca de clase mundial.
**Contexto:**
- Propósito: {Propósito}
- Propuesta de Valor: {propuesta_de_valor}
- Competencia: {analisis_competencia}
- Innovación Clave: {innovacion_foco}
**Tu Tarea:**
Genera un JSON con dos claves: "diferenciador_clave" (una frase que describa la ventaja competitiva esencial) y "eslogan_posicionamiento" (un eslogan corto y memorable).
IMPORTANTE: La longitud total de la respuesta JSON, convertida a texto, no debe exceder los 1980 caracteres. Para lograrlo, resume las descripciones y justificaciones, pero mantén la estructura completa del JSON solicitado.
"""
# Reemplace esta sección completa en workflows.py

# --- PROMTS FASE 05: PMV (ROBUSTOS Y CON ESTRUCTURA CORRECTA) ---
PROMPT_SINTETIZAR_DIRECTIVA_PMV = """
Eres un Chief Product Officer (CPO) experto. Tu objetivo es sintetizar la estrategia de negocio en una directiva clara para el equipo.
**Contexto Estratégico:**
- Propuesta de Valor: {PROPUESTA DE VALOR}
- Cliente Ideal: {CLIENTE}
- Modelo de Ingresos Principal: {FUENTES DE INGRESOS}
- Propósito de la Marca: {Propósito}
**Tu Tarea:**
Analiza el contexto y genera un JSON con una única clave "directiva_pmv". El valor debe ser un párrafo conciso y accionable que guíe la creación del PMV, enfocándose en cómo validar la Propuesta de Valor con el Cliente y el Modelo de Ingresos.
IMPORTANTE: La longitud total de la respuesta JSON no debe exceder los 1980 caracteres. Resume si es necesario.
"""

PROMPT_GENERAR_PMV = """
Eres un estratega de producto experto en metodología Lean. Basándote en la siguiente directiva, define un Producto Mínimo Viable (PMV).
**Directiva Estratégica del PMV:**
{directiva_pmv}
**Tu Tarea:**
Genera un JSON con una clave "plan_producto_pmv", cuyo valor sea un objeto que contenga las siguientes claves: "nombre_producto_pmv", "descripcion_detallada_oferta" y "hipotesis_a_validar". La hipótesis debe enfocarse en validar el modelo de ingresos principal.
IMPORTANTE: La longitud total de la respuesta JSON no debe exceder los 1980 caracteres. Resume si es necesario.
"""

PROMPT_COSTOS_PMV = """
Eres un consultor financiero experto en startups. Basándote en el plan del PMV, desglosa los costos.
**Plan del PMV:**
{plan_producto_pmv}
**Tu Tarea:**
Genera un JSON con la clave "plan_costos_pmv", cuyo valor sea un objeto con dos claves: "costos_unicos" (lista de 2-3 costos iniciales) y "costos_recurrentes" (lista de 2-3 costos mensuales). Sé frugal.
IMPORTANTE: La longitud total de la respuesta JSON no debe exceder los 1980 caracteres. Resume si es necesario.
"""

PROMPT_ESTRATEGIA_LANZAMIENTO_PMV = """
Eres un experto en Marketing de Producto. Diseña una estrategia de lanzamiento para el PMV.
**Contexto:**
- Plan del PMV: {plan_producto_pmv}
- Cliente Ideal: {CLIENTE}
- Canales de Comunicación: {CANALES}
**Tu Tarea:**
Genera un JSON con la clave "estrategia_lanzamiento_pmv", cuyo valor sea un objeto con dos claves: "mensaje_clave_lanzamiento" y "tacticas_lanzamiento" (una lista de 3 a 5 pasos accionables para conseguir los primeros clientes).
IMPORTANTE: La longitud total de la respuesta JSON no debe exceder los 1980 caracteres. Resume si es necesario.
"""

PROMPT_DEFINIR_METRICAS_PMV = """
Eres un Growth Analyst. Define los KPIs para medir el éxito del PMV.
**Contexto:**
- Hipótesis a Validar: {hipotesis_a_validar}
- Estrategia de Lanzamiento: {estrategia_lanzamiento_pmv}
**Tu Tarea:**
Genera un JSON con la clave "plan_metricas_pmv", cuyo valor sea un objeto con dos claves: "metrica_principal" (la métrica más importante para validar la hipótesis) y "metricas_secundarias" (una lista de 2-3 métricas de apoyo del framework AARRR).
IMPORTANTE: La longitud total de la respuesta JSON no debe exceder los 1980 caracteres. Resume si es necesario.
"""

# --- PLANTILLA DE EMAIL ---
EMAIL_BODY_TEMPLATE = """
<div style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
  <div style="background-color: #f8f8f8; padding: 20px; text-align: center;">
    <img src="https://i.imgur.com/uP1ZkU6.png" alt="Vaitengewon Club Logo" style="max-width: 150px;">
  </div>
  <div style="padding: 20px;">
    <h2 style="color: #5A29E4;">¡Tu Vaitengewon Map está casi listo!</h2>
    <p>Hola <strong>{user_name}</strong>,</p>
    <p>¡Buenas noticias! Hemos recibido tu información y nuestro sistema ya está trabajando para generar tu <strong>Vaitengewon Map</strong>, el plan estratégico completo para tu negocio.</p>
    <p>En un plazo máximo de 24 horas, recibirás un segundo correo con un enlace a tu mapa personalizado en una plantilla de Notion. No te preocupes, ¡usar Notion es completamente gratis y te permitirá editar y adaptar tu plan como quieras!</p>
    <p>Ese correo también incluirá el enlace para que puedas agendar tu sesión de asesoría 1 a 1, donde revisaremos juntos la estrategia y resolveremos todas tus dudas.</p>
    <p>Si por alguna razón no recibes el correo en el plazo indicado, no dudes en contactarnos directamente a <strong>contacto@vaitengewon.club</strong>.</p>
    <p>¡Estamos emocionados de acompañarte en este siguiente paso!</p>
    <p>Saludos,<br>El equipo de Vaitengewon Club</p>
  </div>
  <div style="background-color: #5A29E4; color: white; text-align: center; padding: 10px; font-size: 12px;">
    © {current_year} Vaitengewon Club. Todos los derechos reservados.
  </div>
</div>
"""

def _create_notion_page_from_content(database_id: str, title: str, content: str, index_name: str = "ESENCIA"):
    return services.notion_create_page(database_id=database_id, title=title, content_text=content, index_name=index_name)

def run_f03_generate_esencia(user_id: str, db_id: str, idea_negocio: str):
    print(f"[{user_id}] - Iniciando Fase 03: Generación de Esencia.")
    proposito = services.openai_generate_text(PROMPT_PROPOSITO.format(idea_negocio=idea_negocio))
    if not proposito: return False
    mision = services.openai_generate_text(PROMPT_MISION.format(proposito=proposito, idea_negocio=idea_negocio))
    if not mision: return False
    vision = services.openai_generate_text(PROMPT_VISION.format(proposito=proposito, mision=mision))
    if not vision: return False
    valores = services.openai_generate_text(PROMPT_VALORES.format(proposito=proposito, mision=mision, vision=vision))
    if not valores: return False
    esencia_data = {"UserID": user_id, "dbID": db_id, "Propósito": proposito, "Misión": mision, "Visión ": vision, "Valores": valores, "LastUpdate": datetime.now().isoformat(), "Status_Esencia": "Completed"}
    services.gspread_append_row("ESENCIA", {"UserID": user_id})
    services.gspread_update_row("ESENCIA", user_id, esencia_data)
    _create_notion_page_from_content(db_id, "Propósito", proposito)
    _create_notion_page_from_content(db_id, "Misión", mision)
    _create_notion_page_from_content(db_id, "Visión", vision)
    _create_notion_page_from_content(db_id, "Valores", valores)
    print(f"[{user_id}] - Fase 03 completada.")
    return True

def run_f04_generate_business_model(user_id: str, db_id: str):
    print(f"[{user_id}] - Iniciando Fase 04: Generación del Modelo de Negocio.")
    inicio_data = services.gspread_get_row_by_userid("INICIO", user_id)
    esencia_data = services.gspread_get_row_by_userid("ESENCIA", user_id)
    if not inicio_data or not esencia_data: return False
    contexto_completo = {**inicio_data, **esencia_data}

    modelo_resultados = {}

    def generar_modulo(nombre_modulo, prompt_template, contexto_especifico={}):
        contexto_actualizado = {**contexto_completo, **modelo_resultados, **contexto_especifico}
        prompt_formateado = prompt_template.format(**contexto_actualizado)
        resultado_json = services.openai_generate_text(prompt_formateado, response_format="json_object")
        if not resultado_json:
            print(f"[{user_id}] - Fallo al generar el Módulo '{nombre_modulo}'. Abortando Fase 04.")
            return None
        modelo_resultados[nombre_modulo] = resultado_json
        print(f"[{user_id}] - Módulo '{nombre_modulo}' generado.")
        return resultado_json

    if not generar_modulo("CLIENTE", PROMPT_CLIENTE): return False
    contexto_prop = {"cliente_perfil": json.dumps(modelo_resultados["CLIENTE"].get("perfil_cliente")), "cliente_esfuerzos": json.dumps(modelo_resultados["CLIENTE"].get("mapa_empatia", {}).get("esfuerzos")), "cliente_resultados": json.dumps(modelo_resultados["CLIENTE"].get("mapa_empatia", {}).get("resultados"))}
    if not generar_modulo("PROPUESTA DE VALOR", PROMPT_PROPUESTA_VALOR, contexto_prop): return False
    if not generar_modulo("FUENTES DE INGRESOS", PROMPT_FUENTES_INGRESOS, {"propuesta_de_valor": json.dumps(modelo_resultados["PROPUESTA DE VALOR"]), "cliente_perfil": json.dumps(modelo_resultados["CLIENTE"].get("perfil_cliente"))}): return False
    if not generar_modulo("INNOVACIÓN", PROMPT_INNOVACION, {"propuesta_de_valor": json.dumps(modelo_resultados["PROPUESTA DE VALOR"]), "fuentes_ingresos_principal": json.dumps(modelo_resultados["FUENTES DE INGRESOS"].get("fuente_principal"))}): return False
    if not generar_modulo("CANALES", PROMPT_CANALES, {"propuesta_de_valor": json.dumps(modelo_resultados["PROPUESTA DE VALOR"]), "cliente_perfil": json.dumps(modelo_resultados["CLIENTE"].get("perfil_cliente"))}): return False
    if not generar_modulo("RELACIONES CON CLIENTES", PROMPT_RELACIONES_CLIENTES, {"cliente_perfil": json.dumps(modelo_resultados["CLIENTE"].get("perfil_cliente")), "canales_conocimiento": json.dumps(modelo_resultados["CANALES"].get("fases_del_canal", {}).get("conocimiento"))}): return False
    if not generar_modulo("ASOCIACIONES CLAVE", PROMPT_ASOCIACIONES_CLAVE, {"propuesta_de_valor": json.dumps(modelo_resultados["PROPUESTA DE VALOR"]), "cliente_perfil": json.dumps(modelo_resultados["CLIENTE"].get("perfil_cliente"))}): return False
    if not generar_modulo("ACTIVIDADES CLAVE", PROMPT_ACTIVIDADES_CLAVE, {"propuesta_de_valor": json.dumps(modelo_resultados["PROPUESTA DE VALOR"]), "canales_fases": json.dumps(modelo_resultados["CANALES"].get("fases_del_canal")), "relaciones_clientes": json.dumps(modelo_resultados["RELACIONES CON CLIENTES"]), "asociaciones_clave": json.dumps(modelo_resultados["ASOCIACIONES CLAVE"])}): return False
    if not generar_modulo("RECURSOS CLAVE", PROMPT_RECURSOS_CLAVE, {"propuesta_de_valor": json.dumps(modelo_resultados["PROPUESTA DE VALOR"]), "actividades_clave": json.dumps(modelo_resultados["ACTIVIDADES CLAVE"])}): return False
    if not generar_modulo("ESTRUCTURA DE COSTES", PROMPT_ESTRUCTURA_COSTES, {"actividades_clave": json.dumps(modelo_resultados["ACTIVIDADES CLAVE"]), "recursos_clave": json.dumps(modelo_resultados["RECURSOS CLAVE"])}): return False
    if not generar_modulo("STAKEHOLDERS", PROMPT_STAKEHOLDERS, {"actividades_clave": json.dumps(modelo_resultados["ACTIVIDADES CLAVE"])}): return False
    if not generar_modulo("COMPETENCIA", PROMPT_COMPETENCIA, {"propuesta_de_valor": json.dumps(modelo_resultados["PROPUESTA DE VALOR"]), "cliente_perfil": json.dumps(modelo_resultados["CLIENTE"].get("perfil_cliente"))}): return False
    if not generar_modulo("DIFERENCIADOR", PROMPT_DIFERENCIADOR, {"propuesta_de_valor": json.dumps(modelo_resultados["PROPUESTA DE VALOR"]), "analisis_competencia": json.dumps(modelo_resultados["COMPETENCIA"]), "innovacion_foco": json.dumps(modelo_resultados["INNOVACIÓN"])}): return False
    
    data_para_sheets = {k: json.dumps(v, ensure_ascii=False, indent=2) for k, v in modelo_resultados.items()}
    data_para_sheets.update({"UserID": user_id, "dbID": db_id, "STATUS_MODELO": "Completed"})
    
    services.gspread_append_row("MODELO DE NEGOCIO", {"UserID": user_id})
    services.gspread_update_row("MODELO DE NEGOCIO", user_id, data_para_sheets)
    print(f"[{user_id}] - Modelo de Negocio completo guardado en Sheets.")

    for modulo, resultado in modelo_resultados.items():
        contenido_texto = json.dumps(resultado, indent=2, ensure_ascii=False)
        services.notion_create_page(db_id, modulo, contenido_texto, "MODELO DE NEGOCIO")
    print(f"[{user_id}] - Todas las páginas del Modelo de Negocio creadas en Notion.")

    print(f"[{user_id}] - Fase 04 (Completa) finalizada.")
    return True


# Reemplace esta función completa en workflows.py

def run_f05_generate_pmv(user_id: str, db_id: str):
    print(f"[{user_id}] - Iniciando Fase 05: Generación de PMV.")
    
    inicio_data = services.gspread_get_row_by_userid("INICIO", user_id)
    esencia_data = services.gspread_get_row_by_userid("ESENCIA", user_id)
    modelo_data_raw = services.gspread_get_row_by_userid("MODELO DE NEGOCIO", user_id)
    if not inicio_data or not esencia_data or not modelo_data_raw: return False

    modelo_data_json = {}
    for key, value in modelo_data_raw.items():
        if isinstance(value, str) and value.startswith( ('{', '[') ):
            try: modelo_data_json[key] = json.loads(value)
            except json.JSONDecodeError: modelo_data_json[key] = value
        else: modelo_data_json[key] = value
    
    contexto_completo = {**inicio_data, **esencia_data, **modelo_data_json}
    pmv_resultados = {}

    def generar_modulo_pmv(nombre_modulo, prompt_template, contexto_extra={}):
        contexto_para_prompt = {**contexto_completo, **contexto_extra}
        prompt_formateado = prompt_template.format(**contexto_para_prompt)
        resultado_json = services.openai_generate_text(prompt_formateado, response_format="json_object")
        if not resultado_json: return None
        pmv_resultados[nombre_modulo] = resultado_json
        print(f"[{user_id}] - Módulo PMV '{nombre_modulo}' generado.")
        return resultado_json

    # Cadena de Prompts...
    if not generar_modulo_pmv("Directivas PMV", PROMPT_SINTETIZAR_DIRECTIVA_PMV): return False
    contexto_generar_pmv = {"directiva_pmv": json.dumps(pmv_resultados.get("Directivas PMV"))}
    if not generar_modulo_pmv("PMV Generado", PROMPT_GENERAR_PMV, contexto_generar_pmv): return False
    contexto_costos = {"plan_producto_pmv": json.dumps(pmv_resultados.get("PMV Generado"))}
    if not generar_modulo_pmv("Costos PMV", PROMPT_COSTOS_PMV, contexto_costos): return False
    contexto_lanzamiento = {"plan_producto_pmv": json.dumps(pmv_resultados.get("PMV Generado"))}
    if not generar_modulo_pmv("Estrategia Lanzamiento PMV", PROMPT_ESTRATEGIA_LANZAMIENTO_PMV, contexto_lanzamiento): return False
    contexto_metricas = {
        "hipotesis_a_validar": json.dumps(pmv_resultados.get("PMV Generado", {}).get("plan_producto_pmv", {}).get("hipotesis_a_validar")),
        "estrategia_lanzamiento_pmv": json.dumps(pmv_resultados.get("Estrategia Lanzamiento PMV"))
    }
    if not generar_modulo_pmv("Métricas Clave PMV", PROMPT_DEFINIR_METRICAS_PMV, contexto_metricas): return False

    # Guardado en Google Sheets (sin cambios)
    data_para_sheets = {k: json.dumps(v, ensure_ascii=False, indent=2) for k, v in pmv_resultados.items()}
    data_para_sheets.update({"UserID": user_id, "dbID": db_id, "Status_PMV": "Completed", "LastUpdate": datetime.now().isoformat()})
    services.gspread_append_row("PMV", data_para_sheets)
    print(f"[{user_id}] - Plan de PMV guardado en Sheets.")

    # Corrección: Crear una página de Notion para cada módulo del PMV
    for modulo, resultado in pmv_resultados.items():
        contenido_texto = json.dumps(resultado, indent=2, ensure_ascii=False)
        # Se crea una página por módulo, usando "PROYECTO" como Index
        services.notion_create_page(db_id, modulo, contenido_texto, "PROYECTO")
    print(f"[{user_id}] - Páginas de PMV creadas en Notion.")

    print(f"[{user_id}] - Fase 05 (PMV) completada.")
    return True

# --- NUEVA FUNCIÓN FASE 06 ---
def run_f06_send_notification(user_id: str):
    print(f"[{user_id}] - Iniciando Fase 06: Envío de Notificación.")
    
    user_data = services.gspread_get_row_by_userid("INICIO", user_id)
    if not user_data: return False
        
    user_name = user_data.get("Answer1", "emprendedor(a)")
    user_email = user_data.get("userEmail")

    if not user_email: return False
        
    current_year = datetime.now().year
    email_body = EMAIL_BODY_TEMPLATE.format(user_name=user_name, current_year=current_year)
    subject = f"Hola {user_name}, ¡Tu Vaitengewon Map está casi listo! ✨"
    
    services.send_email(to_address=user_email, subject=subject, html_body=email_body)
    
    admin_email_body = f"Se ha completado el flujo para UserID: {user_id}<br>Email: {user_email}"
    services.send_email(to_address="vaitengewon@gmail.com", subject=f"Notificación: Flujo Completado para {user_id}", html_body=admin_email_body)
    
    print(f"[{user_id}] - Fase 06 (Notificación) completada.")
    return True