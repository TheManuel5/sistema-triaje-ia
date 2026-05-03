
"""
Pagina: Gestion de Pacientes
CRUD completo de pacientes
"""

import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.database import init_connection
from utils.config import TIPOS_DOCUMENTO, GENEROS, GRUPOS_SANGUINEOS
from datetime import date

def mostrar():
    st.title("Gestion de Pacientes")
    
    tabs = st.tabs(["Buscar", "Nuevo Paciente", "Lista Completa"])
    
    with tabs[0]:
        buscar_paciente()
    
    with tabs[1]:
        nuevo_paciente()
    
    with tabs[2]:
        lista_pacientes()

def buscar_paciente():
    st.subheader("Buscar Paciente")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        termino = st.text_input("Buscar por nombre o documento", placeholder="Ingrese nombre o numero de documento")
    
    with col2:
        buscar = st.button("Buscar", use_container_width=True)
    
    if buscar and termino:
        conn = init_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id_paciente, numero_documento, nombres, apellidos,
                   fecha_nacimiento, genero, telefono, email
            FROM pacientes
            WHERE LOWER(nombres || ' ' || apellidos) LIKE LOWER(%s)
               OR numero_documento LIKE %s
            ORDER BY nombres, apellidos
            LIMIT 20
        """, (f'%{termino}%', f'%{termino}%'))
        
        resultados = cursor.fetchall()
        
        if resultados:
            st.success(f"Encontrados: {len(resultados)} paciente(s)")
            
            for pac in resultados:
                with st.expander(f"{pac[2]} {pac[3]} - {pac[1]}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**ID:** {pac[0]}")
                        st.write(f"**Nombre:** {pac[2]} {pac[3]}")
                        st.write(f"**Documento:** {pac[1]}")
                    with col2:
                        st.write(f"**Fecha Nac:** {pac[4]}")
                        st.write(f"**Genero:** {pac[5]}")
                        st.write(f"**Telefono:** {pac[6] or 'N/A'}")
        else:
            st.info("No se encontraron pacientes")
        
        cursor.close()
        conn.close()

def nuevo_paciente():
    st.subheader("Registrar Nuevo Paciente")
    
    with st.form("form_nuevo_paciente"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Informacion Personal**")
            tipo_doc = st.selectbox("Tipo Documento", TIPOS_DOCUMENTO)
            numero_doc = st.text_input("Numero Documento")
            nombres = st.text_input("Nombres")
            apellidos = st.text_input("Apellidos")
            fecha_nac = st.date_input("Fecha Nacimiento", max_value=date.today())
            genero = st.selectbox("Genero", GENEROS)
        
        with col2:
            st.markdown("**Informacion de Contacto**")
            telefono = st.text_input("Telefono")
            email = st.text_input("Email")
            direccion = st.text_input("Direccion")
            distrito = st.text_input("Distrito")
            
        st.markdown("**Informacion Medica**")
        col3, col4 = st.columns(2)
        
        with col3:
            grupo_sang = st.selectbox("Grupo Sanguineo", [''] + GRUPOS_SANGUINEOS)
            alergias = st.text_area("Alergias Conocidas", height=80)
        
        with col4:
            enfermedades = st.text_area("Enfermedades Cronicas", height=80)
            medicacion = st.text_area("Medicacion Actual", height=80)
        
        submit = st.form_submit_button("Guardar Paciente", use_container_width=True)
        
        if submit:
            if not numero_doc or not nombres or not apellidos:
                st.error("Complete los campos obligatorios")
            else:
                guardar_paciente_bd(locals())

def guardar_paciente_bd(datos):
    try:
        conn = init_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO pacientes (
                tipo_documento, numero_documento, nombres, apellidos,
                fecha_nacimiento, genero, telefono, email, direccion, distrito,
                grupo_sanguineo, alergias, enfermedades_cronicas, medicacion_actual
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_paciente
        """, (
            datos['tipo_doc'], datos['numero_doc'], datos['nombres'], datos['apellidos'],
            datos['fecha_nac'], datos['genero'], datos['telefono'] or None,
            datos['email'] or None, datos['direccion'] or None, datos['distrito'] or None,
            datos['grupo_sang'] or None, datos['alergias'] or None,
            datos['enfermedades'] or None, datos['medicacion'] or None
        ))
        
        id_paciente = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        st.success(f"Paciente #{id_paciente} registrado exitosamente")
        st.balloons()
    except Exception as e:
        st.error(f"Error: {e}")

def lista_pacientes():
    st.subheader("Lista Completa de Pacientes")
    
    conn = init_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id_paciente, numero_documento, nombres || ' ' || apellidos as nombre,
               genero, fecha_nacimiento, telefono
        FROM pacientes
        WHERE activo = true
        ORDER BY id_paciente DESC
        LIMIT 50
    """)
    
    pacientes = cursor.fetchall()
    
    if pacientes:
        import pandas as pd
        df = pd.DataFrame(pacientes, columns=['ID', 'Documento', 'Nombre', 'Genero', 'Fecha Nac.', 'Telefono'])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Mostrando ultimos 50 pacientes")
    else:
        st.info("No hay pacientes registrados")
    
    cursor.close()
    conn.close()