
"""Dashboard de Gestión - Estadísticas Agregadas"""
import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.database import init_connection
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def mostrar():
    st.title("📈 Dashboard de Gestión")
    
    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Desde", value=datetime.now().date() - timedelta(days=30))
    with col2:
        fecha_fin = st.date_input("Hasta", value=datetime.now().date())
    
    conn = init_connection()
    cursor = conn.cursor()
    
    # Estadísticas generales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cursor.execute("SELECT COUNT(*) FROM triajes WHERE DATE(fecha_hora_registro) BETWEEN %s AND %s", (fecha_inicio, fecha_fin))
        st.metric("Total Triajes", cursor.fetchone()[0])
    
    with col2:
        cursor.execute("SELECT COUNT(DISTINCT id_paciente) FROM triajes WHERE DATE(fecha_hora_registro) BETWEEN %s AND %s", (fecha_inicio, fecha_fin))
        st.metric("Pacientes Únicos", cursor.fetchone()[0])
    
    with col3:
        cursor.execute("SELECT AVG(tiempo_atencion_minutos) FROM triajes WHERE DATE(fecha_hora_registro) BETWEEN %s AND %s", (fecha_inicio, fecha_fin))
        promedio = cursor.fetchone()[0] or 0
        st.metric("Tiempo Atención Prom.", f"{promedio:.0f} min")
    
    # Gráfico de tendencia
    st.markdown("---")
    st.subheader("Tendencia de Triajes")
    
    cursor.execute("""
        SELECT DATE(fecha_hora_registro) as fecha, COUNT(*) as total
        FROM triajes
        WHERE DATE(fecha_hora_registro) BETWEEN %s AND %s
        GROUP BY DATE(fecha_hora_registro)
        ORDER BY fecha
    """, (fecha_inicio, fecha_fin))
    
    data = cursor.fetchall()
    if data:
        df = pd.DataFrame(data, columns=['Fecha', 'Total'])
        fig = px.line(df, x='Fecha', y='Total', markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    cursor.close()
    conn.close()
