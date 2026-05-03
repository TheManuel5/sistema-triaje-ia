
"""Configuración del Sistema"""
import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.database import init_connection

def mostrar():
    st.title("⚙️ Configuración del Sistema")
    
    if st.session_state.usuario['rol'] != 'admin':
        st.warning("⚠️ Solo administradores pueden acceder a esta sección")
        return
    
    tabs = st.tabs(["Parámetros", "Usuarios", "Notificaciones"])
    
    with tabs[0]:
        st.subheader("Parámetros del Sistema")
        conn = init_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT clave, valor, descripcion FROM configuracion ORDER BY categoria, clave")
        configs = cursor.fetchall()
        
        for config in configs:
            st.text_input(config[2], value=config[1], key=config[0])
        
        cursor.close()
        conn.close()
    
    with tabs[1]:
        st.subheader("Gestión de Usuarios")
        st.info("Función de gestión de usuarios en desarrollo")
    
    with tabs[2]:
        st.subheader("Configuración de Notificaciones")
        st.info("Configuración de notificaciones en desarrollo")
