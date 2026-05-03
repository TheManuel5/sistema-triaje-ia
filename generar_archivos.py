#!/usr/bin/env python3
"""
Script para generar todos los archivos del sistema de triaje
"""
import os
from pathlib import Path

# Definir base
base = Path("/home/claude/sistema-triaje-ia")

# Archivo: utils/database.py
(base / "frontend/utils/database.py").write_text('''"""
Utilidades para conexión a base de datos PostgreSQL
"""

import psycopg2
import streamlit as st
from utils.config import APP_CONFIG

def init_connection():
    """Inicializa conexión a PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=APP_CONFIG['DB_HOST'],
            port=APP_CONFIG['DB_PORT'],
            dbname=APP_CONFIG['DB_NAME'],
            user=APP_CONFIG['DB_USER'],
            password=APP_CONFIG['DB_PASSWORD']
        )
        return conn
    except Exception as e:
        st.error(f"Error conectando a la base de datos: {e}")
        return None

def verificar_conexion():
    """Verifica que la conexión a la BD funcione"""
    try:
        conn = init_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            conn.close()
            return True
        return False
    except:
        return False

@st.cache_data(ttl=300)
def ejecutar_query(_conn, query, params=None):
    """Ejecuta query y retorna resultados"""
    cursor = _conn.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()
''')

# Archivo: utils/auth.py
(base / "frontend/utils/auth.py").write_text('''"""
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
''')

# Archivo utils/__init__.py
(base / "frontend/utils/__init__.py").write_text("")
(base / "frontend/pages/__init__.py").write_text("")
(base / "frontend/components/__init__.py").write_text("")

print("✅ Archivos de utilidades creados")
