import streamlit as st
import pandas as pd
import numpy as np
import os
import subprocess

GAM_PATH = "/home/angelocabrera/bin/gamadv-xtd3/"

st.set_page_config(
    page_title="Info Classroom"
)

st.title('GAM-Web')

id = st.text_input('Ingrese el ID de Classroom', max_chars=None, key="idClassroom")
st.subheader('1- Información de Classroom')
if st.button('Buscar', key="buscarC"):
    with st.spinner('Buscando Información...'):
        os.system(GAM_PATH + "gam print courses course "+ id +" show teachers > salida.csv")
        st.write("Datos Generales")
        data = pd.read_csv("salida.csv")
        data.rename(columns = {'name':'Nombre','courseState':'Estado','descriptionHeading':'Descripcion','alternateLink':'Link'}, inplace = True)
        tdf1 = data[['Nombre','Estado','Descripcion', 'Link']].transpose()
        tdf1 = tdf1.astype(str)
        st.dataframe(tdf1)

st.subheader('2 - Participantes de Classroom')
if st.button('Mostrar', key='participantes'):
    with st.spinner('Buscando Información...'):
        os.system(GAM_PATH + "gam print course-participants course "+ id +" > salida.csv")
        data = pd.read_csv("salida.csv")
        data.index += 1
        data.rename(columns = {'userRole':'Tipo', 'profile.emailAddress':'Correo', 'profile.name.fullName':'Nombre'}, inplace = True)
        st.dataframe(data[['Tipo','Correo', 'Nombre']])

st.subheader('3- Agregar profesor a Classroom')
profesor = st.text_input('Ingrese el correo del profesor',  max_chars=None, key="idClassroomAddT")
if profesor != "":
    try:
        with st.spinner('Realizando operacion...'):
            out = subprocess.check_output(GAM_PATH + "gam course "+id+" add teacher "+profesor, shell = True)
            st.success("Profesor agregado correctamente")
            st.info(out)
    except subprocess.CalledProcessError as e:
        st.warning("El correo ya pertenece al Classroom")
