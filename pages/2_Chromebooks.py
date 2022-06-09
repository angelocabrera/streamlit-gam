import streamlit as st
import pandas as pd
import numpy as np
import os
import subprocess

GAM_PATH = "/home/angelocabrera/bin/gamadv-xtd3/"

st.set_page_config(
    page_title="Info Chromebooks"
)

st.title('GAM-Web')

st.subheader('1- Información de Chromebook')
option = st.selectbox(
     'Campo de Busqueda',
     ('Usuario', 'Serie', 'Colegio'))
id = st.text_input('Ingrese el valor de búsqueda', max_chars=None, key="idcros")
if id != "":
    with st.spinner('Buscando...'):
        if option == "Usuario":
            os.system(GAM_PATH + 'gam print cros query "user:'+ id + '" basic > salida.csv')
        elif option == "Colegio":
            os.system(GAM_PATH + 'gam print cros query "location:'+ id + '" basic > salida.csv')
        else:
            os.system(GAM_PATH + 'gam print cros query "id:'+ id + '" basic > salida.csv')
        data = pd.read_csv("salida.csv")
        st.dataframe(data)
 
st.subheader('2 - Mover de Organización')
moveid = st.text_input('Ingrese el nro de serie', max_chars=None, key="moveid")
moveorg = st.text_input('Ingrese la organizacion', max_chars=None, key="moveorg")
if moveid != "":
    if moveorg != "":
        try:
            with st.spinner('Realizando operacion...'):
                out = subprocess.check_output(GAM_PATH + "gam update cros cros_sn "+moveid+" ou "+moveorg+" quickcrosmove", shell = True)
                st.success("Profesor agregado correctamente")
                st.info(out)
        except subprocess.CalledProcessError as e:
            st.warning("No se pudo mover el Chromebook")
