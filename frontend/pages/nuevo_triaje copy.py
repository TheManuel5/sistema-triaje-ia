
"""
Página: Nuevo Triaje
Permite registrar un nuevo triaje con análisis de IA
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
    
    # Paso 1: Seleccionar o registrar paciente
    st.markdown("---")
    st.subheader("1️⃣ Seleccionar Paciente")
    
    conn = init_connection()
    cursor = conn.cursor()
    
    # Obtener lista de pacientes
    cursor.execute("""
        SELECT id_paciente, numero_documento, nombres || ' ' || apellidos as nombre_completo,
               fecha_nacimiento, genero
        FROM pacientes 
        WHERE activo = true
        ORDER BY nombres, apellidos
    """)
    pacientes = cursor.fetchall()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        paciente_seleccionado = st.selectbox(
            "Seleccionar paciente existente",
            options=[(p[0], f"{p[2]} - {p[1]}") for p in pacientes],
            format_func=lambda x: x[1]
        )
    
    with col2:
        if st.button("➕ Nuevo Paciente", use_container_width=True):
            st.session_state.registrar_nuevo_paciente = True
    
    # Mostrar datos del paciente seleccionado
    if paciente_seleccionado:
        id_paciente = paciente_seleccionado[0]
        cursor.execute("""
            SELECT numero_documento, nombres, apellidos, fecha_nacimiento, genero,
                   alergias, enfermedades_cronicas, medicacion_actual
            FROM pacientes
            WHERE id_paciente = %s
        """, (id_paciente,))
        datos_paciente = cursor.fetchone()
        
        st.info(f"""
        **Paciente:** {datos_paciente[1]} {datos_paciente[2]}  
        **Documento:** {datos_paciente[0]}  
        **Edad:** {calcular_edad(datos_paciente[3])} años  
        **Género:** {datos_paciente[4]}  
        **Alergias:** {datos_paciente[5] or 'Ninguna conocida'}
        """)
    
    # Paso 2: Signos Vitales
    st.markdown("---")
    st.subheader("2️⃣ Signos Vitales")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        presion_sistolica = st.number_input("Presión Arterial Sistólica (mmHg)", 60, 250, 120)
        presion_diastolica = st.number_input("Presión Arterial Diastólica (mmHg)", 40, 150, 80)
        temperatura = st.number_input("Temperatura (°C)", 35.0, 42.0, 37.0, 0.1)
    
    with col2:
        frecuencia_cardiaca = st.number_input("Frecuencia Cardíaca (lpm)", 40, 200, 80)
        frecuencia_respiratoria = st.number_input("Frecuencia Respiratoria (rpm)", 10, 40, 16)
        peso = st.number_input("Peso (kg)", 1.0, 300.0, 70.0, 0.1)
    
    with col3:
        saturacion_oxigeno = st.number_input("Saturación de Oxígeno (%)", 70, 100, 98)
        talla = st.number_input("Talla (cm)", 50.0, 250.0, 170.0, 0.1)
    
    # Paso 3: Información Clínica
    st.markdown("---")
    st.subheader("3️⃣ Información Clínica")
    
    motivo_consulta = st.text_area(
        "Motivo de Consulta *",
        placeholder="Describe el motivo principal de la consulta...",
        height=100
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        sintomas_principales = st.text_area(
            "Síntomas Principales",
            placeholder="Lista los síntomas que presenta el paciente...",
            height=150
        )
        
        dolor_ubicacion = st.text_input(
            "Ubicación del Dolor (si aplica)",
            placeholder="Ej: Tórax anterior, abdomen, cabeza..."
        )
    
    with col2:
        tiempo_evolucion = st.text_input(
            "Tiempo de Evolución",
            placeholder="Ej: 2 horas, 3 días, 1 semana..."
        )
        
        dolor_escala = st.slider(
            "Escala de Dolor (0-10)",
            0, 10, 0
        )
        
        antecedentes_personales = st.text_area(
            "Antecedentes Personales Relevantes",
            placeholder="Cirugías recientes, hospitalizaciones, etc.",
            height=80
        )
    
    # Paso 4: Análisis con IA
    st.markdown("---")
    st.subheader("4️⃣ Análisis con Inteligencia Artificial")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        analizar_btn = st.button(
            "🤖 Analizar con IA",
            use_container_width=True,
            type="primary",
            disabled=not motivo_consulta
        )
    
    with col2:
        guardar_sin_ia = st.button(
            "💾 Guardar Sin IA",
            use_container_width=True,
            disabled=not motivo_consulta
        )
    
    # Análisis con IA
    if analizar_btn:
        if not st.session_state.get('openai_api_key'):
            from utils.config import APP_CONFIG
            api_key = APP_CONFIG.get('OPENAI_API_KEY')
            if not api_key or api_key == '':
                st.error("❌ No se ha configurado OPENAI_API_KEY en el archivo .env")
                return
        
        with st.spinner("🤖 Analizando datos con IA..."):
            resultado_ia = analizar_con_ia(
                datos_paciente,
                {
                    'presion_sistolica': presion_sistolica,
                    'presion_diastolica': presion_diastolica,
                    'frecuencia_cardiaca': frecuencia_cardiaca,
                    'frecuencia_respiratoria': frecuencia_respiratoria,
                    'temperatura': temperatura,
                    'saturacion_oxigeno': saturacion_oxigeno,
                    'motivo_consulta': motivo_consulta,
                    'sintomas': sintomas_principales,
                    'tiempo_evolucion': tiempo_evolucion,
                    'dolor_escala': dolor_escala,
                    'dolor_ubicacion': dolor_ubicacion
                }
            )
        
        if resultado_ia['success']:
            st.session_state.resultado_ia = resultado_ia
            
            # Mostrar resultado
            nivel = resultado_ia['nivel_urgencia']
            config_nivel = NIVELES_URGENCIA[nivel]
            
            st.markdown(f"""
            <div class="urgencia-{nivel.lower()}">
                <h3>{config_nivel['icon']} Nivel de Urgencia: {nivel}</h3>
                <p><strong>Confianza:</strong> {resultado_ia['score']:.0%}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🔍 Diagnósticos Diferenciales:**")
                st.write(resultado_ia['diagnosticos'])
            
            with col2:
                st.markdown("**💡 Recomendaciones:**")
                st.write(resultado_ia['recomendaciones'])
            
            st.markdown("**📋 Justificación:**")
            st.info(resultado_ia['justificacion'])
            
            # Botón para guardar
            if st.button("💾 Guardar Triaje", use_container_width=True, type="primary"):
                guardar_triaje(
                    id_paciente,
                    {
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
                    },
                    resultado_ia
                )
        else:
            st.error(f"❌ Error en el análisis: {resultado_ia.get('error')}")
    
    cursor.close()
    conn.close()

def calcular_edad(fecha_nacimiento):
    """Calcula edad a partir de fecha de nacimiento"""
    from datetime import date
    hoy = date.today()
    return hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

def analizar_con_ia(datos_paciente, datos_clinicos):
    """Analiza los datos clínicos usando OpenAI"""
    try:
        from utils.config import APP_CONFIG
        from openai import OpenAI
        
        client = OpenAI(api_key=APP_CONFIG['OPENAI_API_KEY'])
        
        # Construir prompt
        prompt = f"""
Eres un asistente médico especializado en triaje de emergencias. Analiza los siguientes datos:

PACIENTE:
- Edad: {calcular_edad(datos_paciente[3])} años
- Género: {datos_paciente[4]}
- Alergias: {datos_paciente[5] or 'Ninguna'}
- Enfermedades crónicas: {datos_paciente[6] or 'Ninguna'}
- Medicación actual: {datos_paciente[7] or 'Ninguna'}

SIGNOS VITALES:
- Presión Arterial: {datos_clinicos['presion_sistolica']}/{datos_clinicos['presion_diastolica']} mmHg
- Frecuencia Cardíaca: {datos_clinicos['frecuencia_cardiaca']} lpm
- Frecuencia Respiratoria: {datos_clinicos['frecuencia_respiratoria']} rpm
- Temperatura: {datos_clinicos['temperatura']}°C
- Saturación O2: {datos_clinicos['saturacion_oxigeno']}%

INFORMACIÓN CLÍNICA:
- Motivo: {datos_clinicos['motivo_consulta']}
- Síntomas: {datos_clinicos['sintomas']}
- Tiempo evolución: {datos_clinicos['tiempo_evolucion']}
- Dolor (0-10): {datos_clinicos['dolor_escala']}
- Ubicación: {datos_clinicos['dolor_ubicacion']}

Proporciona en formato JSON:
{{
  "nivel_urgencia": "Crítico|Alto|Moderado|Bajo",
  "score": 0.0-1.0,
  "diagnosticos_diferenciales": "lista separada por comas",
  "recomendaciones": "recomendaciones de manejo",
  "justificacion": "explicación breve del nivel asignado"
}}
"""
        
        response = client.chat.completions.create(
            model=APP_CONFIG['OPENAI_MODEL'],
            messages=[
                {"role": "system", "content": "Eres un experto en triaje médico. Responde SOLO con JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=APP_CONFIG['OPENAI_TEMPERATURE'],
            max_tokens=APP_CONFIG['OPENAI_MAX_TOKENS']
        )
        
        resultado_texto = response.choices[0].message.content.strip()
        
        # Limpiar respuesta si tiene markdown
        if resultado_texto.startswith('```'):
            resultado_texto = resultado_texto.split('```')[1]
            if resultado_texto.startswith('json'):
                resultado_texto = resultado_texto[4:]
            resultado_texto = resultado_texto.strip()
        
        import json
        resultado = json.loads(resultado_texto)
        resultado['success'] = True
        resultado['modelo'] = APP_CONFIG['OPENAI_MODEL']
        
        return resultado
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def guardar_triaje(id_paciente, datos_clinicos, resultado_ia):
    """Guarda el triaje en la base de datos"""
    try:
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
                justificacion_ia, modelo_ia_utilizado,
                estado_triaje
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id_triaje
        """, (
            id_paciente,
            st.session_state.usuario['id_usuario'],
            datetime.now(),
            datos_clinicos['presion_sistolica'],
            datos_clinicos['presion_diastolica'],
            datos_clinicos['frecuencia_cardiaca'],
            datos_clinicos['frecuencia_respiratoria'],
            datos_clinicos['temperatura'],
            datos_clinicos['saturacion_oxigeno'],
            datos_clinicos.get('peso'),
            datos_clinicos.get('talla'),
            datos_clinicos['motivo_consulta'],
            datos_clinicos.get('sintomas_principales'),
            datos_clinicos.get('tiempo_evolucion'),
            datos_clinicos.get('dolor_escala'),
            datos_clinicos.get('dolor_ubicacion'),
            datos_clinicos.get('antecedentes_personales'),
            resultado_ia['nivel_urgencia'],
            resultado_ia['score'],
            resultado_ia['diagnosticos_diferenciales'],
            resultado_ia['recomendaciones'],
            resultado_ia['justificacion'],
            resultado_ia.get('modelo'),
            'Pendiente'
        ))
        
        id_triaje = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        st.success(f"✅ Triaje #{id_triaje} guardado exitosamente")
        
        # Enviar notificación si es crítico o alto
        if resultado_ia['nivel_urgencia'] in ['Crítico', 'Alto']:
            enviar_notificacion(id_triaje, resultado_ia)
        
        st.balloons()
        
    except Exception as e:
        st.error(f"❌ Error al guardar: {e}")

def enviar_notificacion(id_triaje, resultado_ia):
    """Envía notificación via n8n webhook"""
    try:
        from utils.config import APP_CONFIG
        webhook_url = f"{APP_CONFIG['N8N_WEBHOOK_URL']}/triaje-critico"
        
        payload = {
            'id_triaje': id_triaje,
            'nivel_urgencia': resultado_ia['nivel_urgencia'],
            'recomendaciones_ia': resultado_ia['recomendaciones']
        }
        
        requests.post(webhook_url, json=payload, timeout=5)
    except:
        pass  # Fallar silenciosamente si n8n no está disponible
