# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
Sistema de Triaje Clínico Asistido por IA
Aplicación Principal - Streamlit

Autor: Sistema IA
Versión: 1.0.0
Fecha: 2025-01-01
"""

import streamlit as st

# ⭐ AGREGAR ESTO AQUÍ - ANTES DE CUALQUIER OTRA COSA ⭐
st.set_page_config(
    page_title="Sistema de Triaje IA",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)
import sys
from pathlib import Path

# Agregar directorio de utilidades al path
sys.path.append(str(Path(__file__).parent))

from utils.database import init_connection, verificar_conexion
from utils.auth import verificar_sesion, login, logout
from utils.config import configurar_pagina

# Configuración de la página
configurar_pagina()

def main():
    """Función principal de la aplicación"""
    
    # Verificar conexión a base de datos al inicio
    if 'db_checked' not in st.session_state:
        if verificar_conexion():
            st.session_state.db_checked = True
        else:
            st.error("❌ No se puede conectar a la base de datos. Por favor, verifica la configuración.")
            st.stop()
    
    # Verificar autenticación
    if not verificar_sesion():
        mostrar_login()
    else:
        mostrar_aplicacion()

def mostrar_login():
    """Muestra la pantalla de inicio de sesión"""
    
    # Centrar el formulario de login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🏥 Sistema de Triaje Clínico")
        st.markdown("### Asistido por Inteligencia Artificial")
        st.markdown("---")
        
        with st.form("login_form"):
            st.markdown("#### Iniciar Sesión")
            username = st.text_input("Usuario", placeholder="Ingrese su usuario")
            password = st.text_input("Password", type="password", placeholder="Ingrese su contraseña")
            submit = st.form_submit_button("Ingresar", use_container_width=True)
            
            if submit:
                if username and password:
                    resultado = login(username, password)
                    if resultado['success']:
                        st.success(f"✅ Bienvenido, {resultado['usuario']['nombre_completo']}")
                        st.rerun()
                    else:
                        st.error(f"❌ {resultado['mensaje']}")
                else:
                    st.warning("⚠️ Por favor complete todos los campos")
        
        st.markdown("---")
        st.markdown("""
        **Usuarios de prueba:**
        - Admin: `admin` / `admin123`
        - Médico: `dr.martinez` / `admin123`
        - Enfermera: `enf.garcia` / `admin123`
        - Triaje: `enf.lopez` / `admin123`
        """)
        
        st.markdown("---")
        st.caption("Versión 1.0.0 | © 2025 Sistema de Triaje IA")

def mostrar_aplicacion():
    """Muestra la aplicación principal después del login"""
    
    # Sidebar con navegación
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.usuario['nombre_completo']}")
        st.caption(f"Rol: {st.session_state.usuario['rol'].title()}")
        st.markdown("---")
        
        # Menú de navegación
        pagina = st.radio(
            "Navegación",
            [
                "🏠 Inicio",
                "➕ Nuevo Triaje",
                "👥 Pacientes",
                "📊 Dashboard Operacional",
                "📈 Dashboard de Gestión",
                "📋 Reportes",
                "⚙️ Configuración",
                "📚 Ayuda"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Botón de cerrar sesión
        if st.button("🚪 Cerrar Sesión", use_container_width=True):
            logout()
            st.rerun()
        
        st.markdown("---")
        st.caption("Sistema de Triaje v1.0")
    
    # Contenido principal según página seleccionada
    if pagina == "🏠 Inicio":
        mostrar_inicio()
    elif pagina == "➕ Nuevo Triaje":
        from pages import nuevo_triaje
        nuevo_triaje.mostrar()
    elif pagina == "👥 Pacientes":
        from pages import pacientes
        pacientes.mostrar()
    elif pagina == "📊 Dashboard Operacional":
        from pages import dashboard_operacional
        dashboard_operacional.mostrar()
    elif pagina == "📈 Dashboard de Gestión":
        from pages import dashboard_gestion
        dashboard_gestion.mostrar()
    elif pagina == "📋 Reportes":
        from pages import reportes
        reportes.mostrar()
    elif pagina == "⚙️ Configuración":
        from pages import configuracion
        configuracion.mostrar()
    elif pagina == "📚 Ayuda":
        from pages import ayuda
        ayuda.mostrar()

def mostrar_inicio():
    """Muestra la página de inicio con estadísticas generales"""
    
    st.title("🏥 Sistema de Triaje Clínico Asistido por IA")
    st.markdown("### Panel de Control General")
    
    # Obtener estadísticas del día
    conn = init_connection()
    cursor = conn.cursor()
    
    # Estadísticas de hoy
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cursor.execute("""
            SELECT COUNT(*) FROM triajes 
            WHERE DATE(fecha_hora_registro) = CURRENT_DATE
        """)
        total_hoy = cursor.fetchone()[0]
        st.metric("Triajes Hoy", total_hoy)
    
    with col2:
        cursor.execute("""
            SELECT COUNT(*) FROM triajes 
            WHERE DATE(fecha_hora_registro) = CURRENT_DATE 
            AND nivel_urgencia IN ('Crítico', 'Alto')
        """)
        urgentes_hoy = cursor.fetchone()[0]
        st.metric("Casos Urgentes", urgentes_hoy)
    
    with col3:
        cursor.execute("""
            SELECT COUNT(*) FROM triajes 
            WHERE DATE(fecha_hora_registro) = CURRENT_DATE 
            AND estado_triaje = 'Pendiente'
        """)
        pendientes = cursor.fetchone()[0]
        st.metric("Pendientes", pendientes)
    
    with col4:
        cursor.execute("""
            SELECT COALESCE(AVG(tiempo_espera_minutos), 0) 
            FROM triajes 
            WHERE DATE(fecha_hora_registro) = CURRENT_DATE
        """)
        promedio_espera = cursor.fetchone()[0]
        st.metric("Espera Promedio", f"{promedio_espera:.0f} min")
    
    st.markdown("---")
    
    # Gráfico de triajes por nivel de urgencia (últimos 7 días)
    st.markdown("### 📊 Triajes por Nivel de Urgencia (Últimos 7 Días)")
    
    cursor.execute("""
        SELECT 
            DATE(fecha_hora_registro) as fecha,
            nivel_urgencia,
            COUNT(*) as total
        FROM triajes
        WHERE fecha_hora_registro >= CURRENT_DATE - INTERVAL '7 days'
        GROUP BY fecha, nivel_urgencia
        ORDER BY fecha DESC, nivel_urgencia
    """)
    
    datos_urgencia = cursor.fetchall()
    
    if datos_urgencia:
        import pandas as pd
        import plotly.express as px
        
        df = pd.DataFrame(datos_urgencia, columns=['Fecha', 'Nivel Urgencia', 'Total'])
        
        fig = px.bar(
            df, 
            x='Fecha', 
            y='Total', 
            color='Nivel Urgencia',
            color_discrete_map={
                'Crítico': '#D32F2F',
                'Alto': '#F57C00',
                'Moderado': '#FBC02D',
                'Bajo': '#388E3C'
            },
            title="Distribución de Triajes por Nivel de Urgencia"
        )
        
        fig.update_layout(
            xaxis_title="Fecha",
            yaxis_title="Cantidad de Triajes",
            legend_title="Nivel de Urgencia",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos de triajes en los últimos 7 días")
    
    st.markdown("---")
    
    # Tabla de triajes recientes
    st.markdown("### 📋 Triajes Recientes")
    
    cursor.execute("""
        SELECT 
            t.id_triaje,
            p.nombres || ' ' || p.apellidos as paciente,
            p.numero_documento,
            t.nivel_urgencia,
            t.motivo_consulta,
            t.estado_triaje,
            TO_CHAR(t.fecha_hora_registro, 'DD/MM/YYYY HH24:MI') as fecha
        FROM triajes t
        INNER JOIN pacientes p ON t.id_paciente = p.id_paciente
        ORDER BY t.fecha_hora_registro DESC
        LIMIT 10
    """)
    
    triajes_recientes = cursor.fetchall()
    
    if triajes_recientes:
        import pandas as pd
        
        df_triajes = pd.DataFrame(
            triajes_recientes,
            columns=['ID', 'Paciente', 'Documento', 'Urgencia', 'Motivo', 'Estado', 'Fecha']
        )
        
        # Aplicar colores según nivel de urgencia - MEJORADO PARA DARK MODE
        def colorear_urgencia(val):
            # Usar rgba con alpha bajo para que funcione en dark/light mode
            color_map = {
                'Crítico': 'background-color: rgba(211, 47, 47, 0.3); font-weight: bold;',
                'Alto': 'background-color: rgba(245, 124, 0, 0.3); font-weight: bold;',
                'Moderado': 'background-color: rgba(251, 192, 45, 0.3);',
                'Bajo': 'background-color: rgba(56, 142, 60, 0.3);'
            }
            return color_map.get(val, '')
        
        st.dataframe(
            df_triajes.style.map(colorear_urgencia, subset=['Urgencia']),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No hay triajes registrados aún")
    
    cursor.close()
    conn.close()
    
  
if __name__ == "__main__":
    main()
