"""
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
