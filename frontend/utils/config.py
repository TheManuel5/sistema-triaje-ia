"""
Configuración general de la aplicación
"""

import streamlit as st
import os
from pathlib import Path

# Cargar variables del .env
from dotenv import load_dotenv

# Buscar el .env en la raíz del proyecto
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

def configurar_pagina():
    """Configura los parámetros de la página de Streamlit"""
    st.set_page_config(
        page_title="Sistema de Triaje IA",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://docs.triaje-ia.com',
            'Report a bug': 'https://github.com/tu-usuario/triaje-ia/issues',
            'About': """
            # Sistema de Triaje Clínico Asistido por IA
            
            Versión 1.0.0
            
            Sistema completo de triaje clínico con integración de IA para clasificación
            de pacientes según nivel de urgencia.
            
            © 2025 - Todos los derechos reservados
            """
        }
    )
    
    # Estilos CSS personalizados
    st.markdown("""
        <style>
        /* Estilos globales */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Tarjetas de métricas - adaptable a tema */
        div[data-testid="metric-container"] {
            background-color: var(--background-color);
            border: 1px solid var(--secondary-background-color);
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        }
        
        /* Botones */
        .stButton>button {
            border-radius: 8px;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Alertas de urgencia - con contraste para dark mode */
        .urgencia-critico {
                background-color: rgba(211, 47, 47, 0.2);  /* Rojo más visible */
                border-left: 5px solid #D32F2F;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
                color: inherit;  /* Hereda el color del texto del tema */
            }
            
            .urgencia-alto {
                background-color: rgba(245, 124, 0, 0.2);  /* Naranja más visible */
                border-left: 5px solid #F57C00;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
                color: inherit;
            }
            
            .urgencia-moderado {
                background-color: rgba(251, 192, 45, 0.2);  /* Amarillo más visible */
                border-left: 5px solid #FBC02D;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
                color: inherit;
            }
            
            .urgencia-bajo {
                background-color: rgba(56, 142, 60, 0.2);  /* Verde más visible */
                border-left: 5px solid #388E3C;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
                color: inherit;
            }
        
        /* Tablas */
        .dataframe {
            font-size: 14px;
        }
        
        /* Sidebar - sin color de fondo fijo */
        section[data-testid="stSidebar"] {
            /* Usa el color por defecto del tema */
        }
        
        /* Títulos - adaptables */
        h1 {
            color: #1E88E5;
        }
        
        h2, h3 {
            /* Usa el color por defecto del tema */
        }
        </style>
    """, unsafe_allow_html=True)

def get_config(key, default=None):
    """Obtiene una configuración del ambiente o retorna valor por defecto"""
    return os.getenv(key, default)
# Configuraciones de la aplicación
APP_CONFIG = {
    'DB_HOST': get_config('DB_HOST', 'localhost'),
    'DB_PORT': get_config('DB_PORT', '5432'),
    'DB_NAME': get_config('DB_NAME', 'triaje_db'),
    'DB_USER': get_config('DB_USER', 'triaje_user'),
    'DB_PASSWORD': get_config('DB_PASSWORD', 'triaje_pass_2024'),
    'OPENAI_API_KEY': get_config('OPENAI_API_KEY', ''),
    'OPENAI_MODEL': get_config('OPENAI_MODEL', 'gpt-4-turbo-preview'),
    'OPENAI_MAX_TOKENS': int(get_config('OPENAI_MAX_TOKENS', '2000')),
    'OPENAI_TEMPERATURE': float(get_config('OPENAI_TEMPERATURE', '0.3')),
        'GEMINI_API_KEY': get_config('GEMINI_API_KEY', ''),  # ← AGREGAR ESTA LÍNEA

    'HCE_API_URL': get_config('HCE_API_URL', 'http://localhost:8000'),
    'N8N_WEBHOOK_URL': get_config('N8N_WEBHOOK_URL', 'http://localhost:5678/webhook'),
}

# Niveles de urgencia con colores
NIVELES_URGENCIA = {
    'Crítico': {'color': '#D32F2F', 'icon': '🔴', 'tiempo_max': 5},
    'Alto': {'color': '#F57C00', 'icon': '🟠', 'tiempo_max': 15},
    'Moderado': {'color': '#FBC02D', 'icon': '🟡', 'tiempo_max': 60},
    'Bajo': {'color': '#388E3C', 'icon': '🟢', 'tiempo_max': 120}
}

# Estados de triaje
ESTADOS_TRIAJE = ['Pendiente', 'En Atención', 'Atendido', 'Derivado', 'Alta']

# Tipos de documento
TIPOS_DOCUMENTO = ['DNI', 'CE', 'PASAPORTE', 'OTRO']

# Géneros
GENEROS = ['Masculino', 'Femenino', 'Otro', 'Prefiero no decir']

# Grupos sanguíneos
GRUPOS_SANGUINEOS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
