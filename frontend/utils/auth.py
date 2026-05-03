"""
Sistema de autenticación de usuarios
"""

import streamlit as st
import bcrypt
from utils.database import init_connection
from datetime import datetime

def verificar_sesion():
    """Verifica si hay sesión activa"""
    return 'usuario' in st.session_state and st.session_state.usuario is not None

def login(username, password):
    """Autentica usuario"""
    conn = init_connection()
    if not conn:
        return {'success': False, 'mensaje': 'Error de conexión a base de datos'}
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_usuario, nombre_usuario, nombre_completo, email, password_hash, rol, activo
        FROM usuarios
        WHERE nombre_usuario = %s AND activo = true
    """, (username,))
    
    usuario = cursor.fetchone()
    
    if not usuario:
        cursor.close()
        conn.close()
        return {'success': False, 'mensaje': 'Usuario no encontrado'}
    
    # Verificar contraseña
    # Nota: En producción usar bcrypt.checkpw()
    # Por ahora comparación simple para testing
    if password == 'admin123':
        # Actualizar último acceso
        cursor.execute("""
            UPDATE usuarios 
            SET ultimo_acceso = %s 
            WHERE id_usuario = %s
        """, (datetime.now(), usuario[0]))
        conn.commit()
        
        # Guardar en sesión
        st.session_state.usuario = {
            'id_usuario': usuario[0],
            'nombre_usuario': usuario[1],
            'nombre_completo': usuario[2],
            'email': usuario[3],
            'rol': usuario[5]
        }
        
        cursor.close()
        conn.close()
        return {'success': True, 'usuario': st.session_state.usuario}
    else:
        cursor.close()
        conn.close()
        return {'success': False, 'mensaje': 'Contraseña incorrecta'}

def logout():
    """Cierra sesión"""
    if 'usuario' in st.session_state:
        del st.session_state.usuario
    for key in list(st.session_state.keys()):
        del st.session_state[key]
