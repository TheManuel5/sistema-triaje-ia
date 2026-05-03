"""
Página: Nuevo Triaje
Análisis con Gemini AI (GRATIS) o Sistema Experto
"""

import streamlit as st
from datetime import datetime
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.database import init_connection
from utils.config import NIVELES_URGENCIA
import requests
import json

def mostrar():
    """Renderiza la página de nuevo triaje"""
    
    st.title("➕ Nuevo Triaje")
    st.markdown("### Registro de Triaje con Análisis de IA")
    
    # Paso 1: Seleccionar paciente
    st.markdown("---")
    st.subheader("1️⃣ Seleccionar Paciente")
    
    conn = init_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id_paciente, numero_documento, nombres || ' ' || apellidos as nombre_completo,
               fecha_nacimiento, genero, alergias, enfermedades_cronicas, medicacion_actual
        FROM pacientes 
        WHERE activo = true
        ORDER BY nombres, apellidos
    """)
    pacientes = cursor.fetchall()
    
    if not pacientes:
        st.warning("⚠️ No hay pacientes. Ve a 'Pacientes' para registrar uno.")
        cursor.close()
        conn.close()
        return
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        paciente_seleccionado = st.selectbox(
            "Seleccionar paciente",
            options=[p for p in pacientes],
            format_func=lambda x: f"{x[2]} - {x[1]}"
        )
    
    with col2:
        if st.button("👥 Pacientes", use_container_width=True):
            st.switch_page("pages/pacientes.py")
    
    if paciente_seleccionado:
        id_paciente = paciente_seleccionado[0]
        datos_paciente = paciente_seleccionado
        
        st.info(f"""
        **Paciente:** {datos_paciente[2]}  
        **Documento:** {datos_paciente[1]}  
        **Edad:** {calcular_edad(datos_paciente[3])} años  
        **Género:** {datos_paciente[4]}  
        **Alergias:** {datos_paciente[5] or 'Ninguna'}
        """)
    
    # Paso 2: Signos Vitales
    st.markdown("---")
    st.subheader("2️⃣ Signos Vitales")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        presion_sistolica = st.number_input("PA Sistólica (mmHg)", 60, 250, 120)
        presion_diastolica = st.number_input("PA Diastólica (mmHg)", 40, 150, 80)
        temperatura = st.number_input("Temperatura (°C)", 35.0, 42.0, 37.0, 0.1)
    
    with col2:
        frecuencia_cardiaca = st.number_input("FC (lpm)", 40, 200, 80)
        frecuencia_respiratoria = st.number_input("FR (rpm)", 10, 40, 16)
        peso = st.number_input("Peso (kg)", 1.0, 300.0, 70.0, 0.1)
    
    with col3:
        saturacion_oxigeno = st.number_input("SatO2 (%)", 70, 100, 98)
        talla = st.number_input("Talla (cm)", 50.0, 250.0, 170.0, 0.1)
    
    # Paso 3: Información Clínica
    st.markdown("---")
    st.subheader("3️⃣ Información Clínica")
    
    motivo_consulta = st.text_area("Motivo de Consulta *", placeholder="Motivo principal...", height=100)
    
    col1, col2 = st.columns(2)
    
    with col1:
        sintomas_principales = st.text_area("Síntomas Principales", placeholder="Síntomas...", height=120)
        dolor_ubicacion = st.text_input("Ubicación del Dolor", placeholder="Ej: Tórax anterior...")
    
    with col2:
        tiempo_evolucion = st.text_input("Tiempo de Evolución", placeholder="Ej: 2 horas, 3 días...")
        dolor_escala = st.slider("Escala de Dolor (0-10)", 0, 10, 0)
        antecedentes_personales = st.text_area("Antecedentes Relevantes", placeholder="Cirugías, hospitalizaciones...", height=80)
    
    # Paso 4: Análisis
    st.markdown("---")
    st.subheader("4️⃣ Análisis Inteligente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        gemini_btn = st.button(
            "🤖 Gemini AI (GRATIS)", 
            use_container_width=True, 
            type="primary", 
            disabled=not motivo_consulta,
            help="Google Gemini - 100% GRATIS"
        )
    
    with col2:
        reglas_btn = st.button(
            "⚡ Sistema Experto", 
            use_container_width=True, 
            disabled=not motivo_consulta,
            help="Análisis basado en reglas médicas"
        )
    
    datos_dict = {
        'presion_sistolica': presion_sistolica,
        'presion_diastolica': presion_diastolica,
        'frecuencia_cardiaca': frecuencia_cardiaca,
        'frecuencia_respiratoria': frecuencia_respiratoria,
        'temperatura': temperatura,
        'saturacion_oxigeno': saturacion_oxigeno,
        'peso': peso,
        'talla': talla,
        'motivo_consulta': motivo_consulta,
        'sintomas_principales': sintomas_principales,
        'tiempo_evolucion': tiempo_evolucion,
        'dolor_escala': dolor_escala,
        'dolor_ubicacion': dolor_ubicacion,
        'antecedentes_personales': antecedentes_personales
    }
    
    # Análisis con Gemini
    if gemini_btn:
        with st.spinner("🤖 Analizando con Gemini AI..."):
            resultado = analizar_gemini(datos_paciente, datos_dict)
        
        if resultado['success']:
            mostrar_y_guardar(id_paciente, resultado, datos_dict)
        else:
            st.error(f"❌ Error Gemini: {resultado['error']}")
            st.info("💡 Usa 'Sistema Experto' que siempre funciona")
    
    # Análisis con Reglas
    if reglas_btn:
        with st.spinner("⚡ Analizando con Sistema Experto..."):
            resultado = analizar_reglas(datos_paciente, datos_dict)
        mostrar_y_guardar(id_paciente, resultado, datos_dict)
    
    cursor.close()
    conn.close()

def mostrar_y_guardar(id_paciente, resultado, datos):
    """Muestra resultado y GUARDA AUTOMÁTICAMENTE"""
    
    nivel = resultado['nivel_urgencia']
    config = NIVELES_URGENCIA[nivel]
    
    st.markdown(f"""
    <div class="urgencia-{nivel.lower()}">
        <h3>{config['icon']} Nivel de Urgencia: {nivel}</h3>
        <p><strong>Confianza:</strong> {resultado['score']:.0%} | <strong>Modelo:</strong> {resultado.get('modelo', 'Sistema Experto')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔍 Diagnósticos Diferenciales:**")
        st.write(resultado['diagnosticos_diferenciales'])
    
    with col2:
        st.markdown("**💡 Recomendaciones:**")
        st.write(resultado['recomendaciones'])
    
    st.markdown("**📋 Justificación:**")
    st.info(resultado['justificacion'])
    
    # GUARDAR AUTOMÁTICAMENTE (sin botón)
    st.markdown("---")
    st.markdown("### 💾 Guardando triaje...")
    
    guardar_triaje(id_paciente, datos, resultado)

def calcular_edad(fecha_nac):
    """Calcula edad del paciente"""
    from datetime import date
    hoy = date.today()
    return hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))

def analizar_gemini(paciente, clinicos):
    """Análisis con Google Gemini AI (GRATIS)"""
    try:
        from google import genai
        from google.genai import types
        from utils.config import APP_CONFIG
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        key = os.getenv('GEMINI_API_KEY') or APP_CONFIG.get('GEMINI_API_KEY', '')
        
        if not key or key == '':
            return {
                'success': False,
                'error': 'Configura GEMINI_API_KEY en .env'
            }
        
        # Cliente con la API NUEVA
        client = genai.Client(api_key=key)
        
        prompt = f"""Eres un médico experto en triaje de emergencias. Analiza estos datos y responde SOLO con JSON válido (sin markdown, sin backticks):

DATOS DEL PACIENTE:
- Edad: {calcular_edad(paciente[3])} años
- Género: {paciente[4]}
- Alergias: {paciente[5] or 'Ninguna'}

SIGNOS VITALES:
- PA: {clinicos['presion_sistolica']}/{clinicos['presion_diastolica']} mmHg
- FC: {clinicos['frecuencia_cardiaca']} lpm
- FR: {clinicos['frecuencia_respiratoria']} rpm
- Temp: {clinicos['temperatura']}°C
- SatO2: {clinicos['saturacion_oxigeno']}%

CLÍNICA:
- Motivo: {clinicos['motivo_consulta']}
- Dolor: {clinicos['dolor_escala']}/10

Responde EXCLUSIVAMENTE con este JSON:
{{"nivel_urgencia":"Crítico|Alto|Moderado|Bajo","score":0.85,"diagnosticos_diferenciales":"dx1, dx2","recomendaciones":"recs","justificacion":"just"}}"""
        
        response = client.models.generate_content(
            model='models/gemini-2.5-flash',  # ← Agrega "models/" y usa 2.5
            contents=prompt
        )

        
        texto = response.text.strip()
        
        if '```' in texto:
            texto = texto.split('```')[1]
            if texto.startswith('json'):
                texto = texto[4:]
            texto = texto.strip()
        
        resultado = json.loads(texto)
        resultado['success'] = True
        resultado['modelo'] = 'Gemini 1.5 Flash'
        
        return resultado
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def analizar_reglas(paciente, c):
    """Sistema Experto basado en reglas médicas"""
    
    score = 0.0
    factores = []
    diagnosticos = []
    recomendaciones = []
    
    # Evaluar saturación de oxígeno
    if c['saturacion_oxigeno'] < 90:
        score += 0.4
        factores.append("Hipoxemia severa (SatO2 < 90%)")
        diagnosticos.append("Insuficiencia respiratoria")
        recomendaciones.append("Oxigenoterapia inmediata")
    elif c['saturacion_oxigeno'] < 94:
        score += 0.2
        factores.append("Hipoxemia leve (SatO2 < 94%)")
        recomendaciones.append("Monitorizar saturación")
    
    # Evaluar presión arterial
    if c['presion_sistolica'] > 180 or c['presion_diastolica'] > 110:
        score += 0.3
        factores.append("Crisis hipertensiva")
        diagnosticos.append("Emergencia hipertensiva")
        recomendaciones.append("Manejo antihipertensivo urgente")
    elif c['presion_sistolica'] < 90:
        score += 0.35
        factores.append("Hipotensión (PA < 90 mmHg)")
        diagnosticos.append("Estado de shock")
        recomendaciones.append("Reanimación con fluidos IV")
    
    # Evaluar frecuencia cardíaca
    if c['frecuencia_cardiaca'] > 120:
        score += 0.25
        factores.append("Taquicardia (FC > 120)")
        diagnosticos.append("Arritmia cardíaca")
        recomendaciones.append("ECG urgente y monitorización")
    elif c['frecuencia_cardiaca'] < 50:
        score += 0.25
        factores.append("Bradicardia (FC < 50)")
        diagnosticos.append("Bloqueo cardíaco")
        recomendaciones.append("Monitorización cardíaca continua")
    
    # Evaluar frecuencia respiratoria
    if c['frecuencia_respiratoria'] > 24:
        score += 0.2
        factores.append("Taquipnea (FR > 24)")
        recomendaciones.append("Evaluar vía aérea y función respiratoria")
    elif c['frecuencia_respiratoria'] < 12:
        score += 0.2
        factores.append("Bradipnea (FR < 12)")
        recomendaciones.append("Evaluar estado de consciencia")
    
    # Evaluar temperatura
    if c['temperatura'] > 39:
        score += 0.2
        factores.append("Fiebre alta (> 39°C)")
        diagnosticos.append("Proceso infeccioso")
        recomendaciones.append("Antipiréticos y búsqueda de foco infeccioso")
    elif c['temperatura'] < 36:
        score += 0.15
        factores.append("Hipotermia (< 36°C)")
        recomendaciones.append("Recalentamiento progresivo")
    
    # Evaluar dolor
    if c['dolor_escala'] >= 8:
        score += 0.3
        factores.append("Dolor severo (≥ 8/10)")
        recomendaciones.append("Analgesia inmediata")
    elif c['dolor_escala'] >= 5:
        score += 0.15
        factores.append("Dolor moderado (5-7/10)")
        recomendaciones.append("Analgesia según protocolo")
    
    # Análisis de palabras clave en síntomas
    texto_completo = (c['motivo_consulta'] + " " + (c.get('sintomas_principales') or '')).lower()
    
    palabras_criticas = {
        'dolor pecho': (0.4, "Síndrome coronario agudo", "ECG inmediato + troponinas"),
        'dolor torácico': (0.4, "Síndrome coronario agudo", "ECG inmediato + troponinas"),
        'dolor precordial': (0.4, "Síndrome coronario agudo", "ECG inmediato + troponinas"),
        'convulsión': (0.35, "Crisis convulsiva", "Protección y vía venosa"),
        'hemorragia': (0.3, "Hemorragia activa", "Control de hemorragia inmediato"),
        'sangrado': (0.3, "Hemorragia activa", "Hemostasia urgente"),
        'asfixia': (0.4, "Obstrucción de vía aérea", "Manejo avanzado de vía aérea"),
        'ahogo': (0.4, "Dificultad respiratoria severa", "Oxígeno y evaluación urgente"),
        'inconsciente': (0.3, "Alteración del estado de conciencia", "Evaluación neurológica urgente"),
        'desmayo': (0.25, "Síncope", "Descartar causas cardíacas"),
    }
    
    for palabra, (peso, dx, rec) in palabras_criticas.items():
        if palabra in texto_completo:
            score += peso
            if dx and dx not in diagnosticos:
                diagnosticos.append(dx)
            if rec and rec not in recomendaciones:
                recomendaciones.append(rec)
    
    # Determinar nivel de urgencia
    if score >= 0.7:
        nivel = "Crítico"
    elif score >= 0.5:
        nivel = "Alto"
    elif score >= 0.3:
        nivel = "Moderado"
    else:
        nivel = "Bajo"
    
    # Valores por defecto
    if not diagnosticos:
        diagnosticos.append("Evaluación clínica pendiente")
    if not recomendaciones:
        recomendaciones.append("Evaluación médica según programación")
    
    justificacion = f"Análisis basado en: {', '.join(factores)}" if factores else "Signos vitales dentro de parámetros normales"
    
    return {
        'success': True,
        'nivel_urgencia': nivel,
        'score': min(score, 1.0),
        'diagnosticos_diferenciales': ', '.join(diagnosticos),
        'recomendaciones': '. '.join(recomendaciones),
        'justificacion': justificacion,
        'modelo': 'Sistema Experto (Reglas)'
    }

def guardar_triaje(id_paciente, datos, resultado):
    """Guarda el triaje en la base de datos"""
    try:
        st.write("DEBUG: Iniciando guardado...")  # ← AGREGAR
        st.write(f"DEBUG: id_paciente = {id_paciente}")  # ← AGREGAR
        st.write(f"DEBUG: usuario = {st.session_state.get('usuario')}")  # ← AGREGAR
        conn = init_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO triajes (
                id_paciente, id_usuario_triaje, fecha_hora_registro,
                presion_arterial_sistolica, presion_arterial_diastolica,
                frecuencia_cardiaca, frecuencia_respiratoria,
                temperatura, saturacion_oxigeno, peso, talla,
                motivo_consulta, sintomas_principales, tiempo_evolucion,
                dolor_escala, dolor_ubicacion, antecedentes_personales,
                nivel_urgencia, nivel_urgencia_score,
                diagnosticos_diferenciales, recomendaciones_ia,
                justificacion_ia, modelo_ia_utilizado, estado_triaje
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id_triaje
        """, (
            id_paciente,
            st.session_state.usuario['id_usuario'],
            datetime.now(),
            datos['presion_sistolica'],
            datos['presion_diastolica'],
            datos['frecuencia_cardiaca'],
            datos['frecuencia_respiratoria'],
            datos['temperatura'],
            datos['saturacion_oxigeno'],
            datos.get('peso'),
            datos.get('talla'),
            datos['motivo_consulta'],
            datos.get('sintomas_principales'),
            datos.get('tiempo_evolucion'),
            datos.get('dolor_escala'),
            datos.get('dolor_ubicacion'),
            datos.get('antecedentes_personales'),
            resultado['nivel_urgencia'],
            resultado['score'],
            resultado['diagnosticos_diferenciales'],
            resultado['recomendaciones'],
            resultado['justificacion'],
            resultado.get('modelo', 'Sistema Experto'),
            'Pendiente'
        ))
        
        id_triaje = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        st.success(f"✅ Triaje #{id_triaje} guardado exitosamente")
        
        # Enviar notificación si es crítico o alto
        if resultado['nivel_urgencia'] in ['Crítico', 'Alto']:
            enviar_notificacion(id_triaje, resultado)
        
        st.balloons()
        
    except Exception as e:
        st.error(f"❌ Error al guardar el triaje: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

def enviar_notificacion(id_triaje, resultado):
    """Envía notificación vía n8n webhook"""
    try:
        from utils.config import APP_CONFIG
        
        webhook_url = APP_CONFIG.get('N8N_WEBHOOK_URL', '')
        if not webhook_url or webhook_url == '':
            return
        
        url_completa = f"{webhook_url}/triaje-critico"
        
        payload = {
            'id_triaje': id_triaje,
            'nivel_urgencia': resultado['nivel_urgencia'],
            'recomendaciones_ia': resultado['recomendaciones'],
            'timestamp': datetime.now().isoformat()
        }
        
        requests.post(url_completa, json=payload, timeout=5)
        
    except:
        pass  # Falla silenciosamente si n8n no está disponible
