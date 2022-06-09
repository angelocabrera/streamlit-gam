import streamlit as st
import pandas as pd
import numpy as np
import os
import subprocess
import json

GAM_PATH = "/home/angelocabrera/bin/gamadv-xtd3/"

st.set_page_config(
    page_title="GAMlit - Info Usuarios"
)

st.title('GAM-Web')
st.subheader('1- Informacion de usuarios')
email = st.text_input('Ingrese el correo del usuario')
if email != "":
    with st.spinner('Buscando Información...'):
        os.system(GAM_PATH + "gam info user " + email + " formatjson > salida.json")
        writeFile =open('salida.json', 'r')
        data = writeFile.read()
        person_dict = json.loads(data)
        writeFile.close()
        
        rut = ''
        try:
            rut = str(person_dict['externalIds'][0]['value'])
        except:
            rut = '*No definido*'
        
        
        st.write(f'''
                | Campo | Valor |
                | ----------- | ----------- |
                | ID | {str(person_dict['id'])} |
                | Nombre | {str(person_dict['name']['fullName'])} |
                | Fecha Creacion | {str(person_dict['creationTime'])} |
                | Fecha Ultma Conexion | {str(person_dict['lastLoginTime'])} |
                | TOS Aceptado | {str(person_dict['agreedToTerms'])} |
                | RUT | {rut} |
                | Organización | {str(person_dict['orgUnitPath'])} |
                | Licencia | {str(person_dict['licenses'])} |
                | Suspendido | {str(person_dict['suspended'])} |
                ''')
        
        #st.json(data)
        #st.write(person_dict)
        
st.subheader('2- Suspender usuario')
if st.button('Suspender', key='suspender'):
    try:
        with st.spinner('Realizando operacion...'):
            out = subprocess.check_output(GAM_PATH + "gam update user " + email + " suspended on", shell = True)
            st.success("Usuario suspendido")
            st.info(out)
    except subprocess.CalledProcessError as e:
        st.warning("No se pudo suspender usuario")

st.subheader('3- Reactivar usuario')
if st.button('Reactivar', key='reactivar'):
    try:
        with st.spinner('Realizando operacion...'):
            out = subprocess.check_output(GAM_PATH + "gam update user " + email + " suspended off", shell = True)
            st.success("Usuario reactivado")
            st.info(out)
    except subprocess.CalledProcessError as e:
        st.warning("No se pudo reactivar usuario")
    