
"""Ayuda y Documentación"""
import streamlit as st

def mostrar():
    st.title("📚 Ayuda y Documentación")
    
    st.markdown("""
    ## 🏥 Sistema de Triaje Clínico Asistido por IA
    
    ### Módulos del Sistema
    
    #### 1️⃣ Nuevo Triaje
    Permite registrar un nuevo triaje con análisis de IA:
    - Seleccionar paciente existente
    - Ingresar signos vitales
    - Describir síntomas
    - Obtener análisis de IA
    - Guardar triaje
    
    #### 2️⃣ Pacientes
    Gestión completa de pacientes:
    - Buscar pacientes
    - Registrar nuevos pacientes
    - Ver historial de triajes
    
    #### 3️⃣ Dashboard Operacional
    Métricas en tiempo real:
    - Triajes del día
    - Casos urgentes
    - Tiempos de espera
    - Distribución por urgencia
    
    #### 4️⃣ Dashboard de Gestión
    Estadísticas agregadas:
    - Tendencias mensuales
    - Análisis por profesional
    - Métricas de calidad
    
    ### Niveles de Urgencia
    
    - 🔴 **Crítico**: Atención inmediata (< 5 min)
    - 🟠 **Alto**: Atención prioritaria (< 15 min)
    - 🟡 **Moderado**: Atención en 1 hora
    - 🟢 **Bajo**: Atención en 2 horas
    
    ### Soporte
    
    Para más información:
    - 📧 Email: soporte@triaje-ia.com
    - 📖 Documentación: Ver carpeta `docs/`
    """)
