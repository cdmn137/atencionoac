import streamlit as st
import pandas as pd
import altair as alt


st.set_page_config(
    page_title="Oficina de Atención Ciudadana CFG-FCI",
    page_icon="🏢",
    layout="wide",
)

st.write("# Bienvenidos a la OAC! ✨")

def load_data():
    # ----------> Leer Bases de Datos
    df = pd.read_excel("casos.xlsx")
    df["Transmisor/Nombre"] = df["Transmisor/Nombre"].astype(str)
    df =  df.loc[~df["Transmisor/Nombre"].str.contains("prueba"), ]
    df = df.dropna(subset=["Estatus"])
    df.loc[df["Asignado/Asignado/Nombre"].isna(), "Asignado/Asignado/Nombre"] = "Ninguno"
    df["Categoría/Nombre de categoría"] = df["Categoría/Nombre de categoría"].astype(str)
    df =  df.loc[~df["Categoría/Nombre de categoría"].str.contains("False"), ]
    #  Fin de leer Bases de Datos <--------------------------------------------------------

    # ----------> Traducir los estatus
    # estatus de asignacion
    d = {
        "assigned":"Asignado",
        "answered":"Respondido",
        "cancel":"Cancelado",
        "process":"Proceso",
        False:"False",

    }
    df["Asignado/Estatus"] = df["Asignado/Estatus"].replace(d)

    d2 = {
        'process':'A-En Proceso', 
        'confirm':'B-Confirmado', 
        'bound':'C-Vinculado', 
        'reply':'D-Respondido', 
        'waiting':'E-En Espera', 
        'unanswered':'F-Sin respuesta'
    }
    df["Estatus"] = df["Estatus"].replace(d2)
    # Fin de traduccion de estatus <-------------------------------------------------------
    return df

df = load_data()

def info_general():
        col1, col2 = st.columns([0.3, 0.7])
        with col2:
            # -- Grafico de categorias --
            st.subheader('Casos por Estado')
            st.text(f"{len(df)} Casos")
            categorias = df["Transmisor/Provincia/Nombre provincia"].value_counts()
            df_categorias = pd.DataFrame({"categoria":categorias.index, "valores":categorias})
            bar = alt.Chart(df_categorias).mark_bar().encode(
                x= alt.X("categoria", sort=None),
                y="valores"
            )
            st.altair_chart(
                (bar).interactive(),
                use_container_width=True
            )

        with col1:
            # -- Grafico de estatus --
            st.subheader('Casos por Categorias')
            valores = df["Categoría/Nombre de categoría"].value_counts()
            source = pd.DataFrame({"category": valores.index, "value": valores})
            ch = alt.Chart(source).mark_arc().encode(
                theta="value",
                color="category"
            )
            st.altair_chart(
                (ch).interactive(),
                use_container_width=True
            )

st.title('Informacion general de los casos atendidos a traves del Sistema SINCO')
info_general()
st.write('Información extraida de la B.D. del Sistema SINCO 2.0 correspondiente al periodo del 18/07/2022 hasta la fecha.')

st.write("## Sistema SINCO ")
acerca, app, help  = st.columns([0.25, 0.25, 0.50])
with acerca:
     st.write("### ¿Como Funciona?")
     st.link_button("Ingresa aqui! - SINCO", "https://www.sinco.gob.ve/acerca")

with app:
     st.write("### SINCO App")
     st.link_button("SINCO App - Descargala aqui!", "https://play.google.com/store/apps/details?id=org.alcaravan.sincoobpp")

with help:
     st.write("### Inconvenientes con el Registro!")
     st.write("Si por alguna razon no puedes ingresar al sistema, puedes escribir por este medio.")
     st.link_button("Contactenos!", "https://www.sinco.gob.ve/contactus")

st.write("## ¿Como funciona la OAC CFG-FCI? ")
st.markdown(
    """
    En la Oficina de Atención Ciudadana (OAC), del Consejo Federal de Gobierno (CFG) - Fondo de Compensación Interterritorial (FCI), 
    se atiende a los voceros del Poder Popular ya sea via presencial o a traves del Sistema de Integración y Comunicación (SINCO), dicha
    atención se realiza de la siguiente forma:
    - Atención al Poder Popular de forma presencial.
        * Atención en los espacios destinados para ello de los/las voceros(as) de las Organizaciones.
        * Verificación de su solicitud en el Sistema SINCO.
        * levantamiento de minuta de reunion y acuerdos con los voceros.
        * Envio de comunicación informativa y de agradecimiento por haber asistido a nuestras oficinas.
    - Atencion al Poder Popular a traves del sistema SINCO
        * Recepción y revisión de las solicitudes realizadas atraves del sistema SINCO.
        * Asignación a la dirección que le corresponda o al analista responsable de dar respuesta.
        * El analista asignado debe generar una respuesta para enviar a la organización.
        * El Responsable del caso debe aprobar la respuesta generada por el analista y enviar a la organización.
"""
)
