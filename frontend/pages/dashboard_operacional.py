
"""
Dashboard Operacional - Métricas en Tiempo Real
"""

import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.database import init_connection
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def mostrar():
    st.title("📊 Dashboard Operacional")
    st.markdown("### Métricas en Tiempo Real")
    
    # Filtros
    col1, col2 = st.columns([3, 1])
    with col1:
        fecha_ref = st.date_input("Fecha", value=datetime.now().date())
    with col2:
        if st.button("🔄 Actualizar", use_container_width=True):
            st.rerun()
    
    conn = init_connection()
    cursor = conn.cursor()
    
    # KPIs principales
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cursor.execute("SELECT COUNT(*) FROM triajes WHERE DATE(fecha_hora_registro) = %s", (fecha_ref,))
        total_hoy = cursor.fetchone()[0]
        st.metric("Triajes Hoy", total_hoy, delta=None)
    
    with col2:
        cursor.execute("""
            SELECT COUNT(*) FROM triajes 
            WHERE DATE(fecha_hora_registro) = %s AND nivel_urgencia IN ('Crítico', 'Alto')
        """, (fecha_ref,))
        urgentes = cursor.fetchone()[0]
        st.metric("Casos Urgentes", urgentes, delta=f"{(urgentes/max(total_hoy,1)*100):.0f}%")
    
    with col3:
        cursor.execute("""
            SELECT COUNT(*) FROM triajes 
            WHERE DATE(fecha_hora_registro) = %s AND estado_triaje = 'Pendiente'
        """, (fecha_ref,))
        pendientes = cursor.fetchone()[0]
        st.metric("Pendientes", pendientes)
    
    with col4:
        cursor.execute("""
            SELECT COALESCE(AVG(tiempo_espera_minutos), 0)
            FROM triajes 
            WHERE DATE(fecha_hora_registro) = %s
        """, (fecha_ref,))
        promedio = cursor.fetchone()[0]
        st.metric("Espera Promedio", f"{promedio:.0f} min")
    
    # Gráficos
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribución por Nivel de Urgencia")
        cursor.execute("""
            SELECT nivel_urgencia, COUNT(*) as total
            FROM triajes
            WHERE DATE(fecha_hora_registro) = %s
            GROUP BY nivel_urgencia
        """, (fecha_ref,))
        data = cursor.fetchall()
        
        if data:
            df = pd.DataFrame(data, columns=['Nivel', 'Total'])
            fig = px.pie(df, values='Total', names='Nivel',
                        color='Nivel',
                        color_discrete_map={
                            'Crítico': '#D32F2F',
                            'Alto': '#F57C00',
                            'Moderado': '#FBC02D',
                            'Bajo': '#388E3C'
                        })
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos")
    
    with col2:
        st.subheader("Estados de Atención")
        cursor.execute("""
            SELECT estado_triaje, COUNT(*) as total
            FROM triajes
            WHERE DATE(fecha_hora_registro) = %s
            GROUP BY estado_triaje
        """, (fecha_ref,))
        data = cursor.fetchall()
        
        if data:
            df = pd.DataFrame(data, columns=['Estado', 'Total'])
            fig = px.bar(df, x='Estado', y='Total', color='Estado')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos")
    
    # Tabla de triajes del día
    st.markdown("---")
    st.subheader("Triajes del Día")
    
    cursor.execute("""
        SELECT 
            t.id_triaje,
            p.nombres || ' ' || p.apellidos as paciente,
            t.nivel_urgencia,
            t.motivo_consulta,
            t.estado_triaje,
            TO_CHAR(t.fecha_hora_registro, 'HH24:MI') as hora,
            COALESCE(t.tiempo_espera_minutos, 0) as espera
        FROM triajes t
        INNER JOIN pacientes p ON t.id_paciente = p.id_paciente
        WHERE DATE(t.fecha_hora_registro) = %s
        ORDER BY t.fecha_hora_registro DESC
    """, (fecha_ref,))
    
    triajes = cursor.fetchall()
    
    if triajes:
        df = pd.DataFrame(triajes, columns=['ID', 'Paciente', 'Urgencia', 'Motivo', 'Estado', 'Hora', 'Espera'])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No hay triajes registrados para esta fecha")
    
    cursor.close()
    conn.close()
