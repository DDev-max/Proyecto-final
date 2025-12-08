import streamlit as st
import pandas as pd
import io
import sys
import os
import matplotlib.pyplot as plt

RUTA_VIS = os.path.dirname(__file__)
RUTA_SRC = os.path.abspath(os.path.join(RUTA_VIS, ".."))

for ruta in (RUTA_SRC, RUTA_VIS):
    if ruta not in sys.path:
        sys.path.append(ruta)

from eda.EDA import ProcesadorEDA
from visualizacion import Visualizador




st.set_page_config(
    page_title="Proyecto Final - Consumo Eléctrico y Clima",
    page_icon="⚡",
    layout="wide"
)

SERVIDOR_SQL = "STEVEN\\SQLEXPRESS"
TABLA_SQL = "consumo"

# Manejo de páginas
if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

st.sidebar.title("Menú")

if st.sidebar.button("Inicio"):
    st.session_state.pagina = "Inicio"

if st.sidebar.button("Dataset"):
    st.session_state.pagina = "Dataset"

if st.sidebar.button("Gráficos"):
    st.session_state.pagina = "Gráficos"

# ===== Página: Inicio =====
if st.session_state.pagina == "Inicio":
    st.title("⚡ Proyecto Final – Consumo Eléctrico y Clima")
    st.markdown("""
    ### Curso: Programación II – Big Data  
    ### Estudiantes: Steven Vindas / Claudio Poveda
    ---
    En este proyecto se analiza una base de datos de **consumo eléctrico** combinada con 
    **variables climáticas** temperatura aparente, nubosidad, precipitación, viento, etc..  
    Los datos provienen de una tabla SQL llamada **`consumo`**, y la  conectamos a Python.
    """)


# ===== Página: Dataset =====
elif st.session_state.pagina == "Dataset":
    st.header("Dataset desde SQL")

    try:
        eda = ProcesadorEDA(SERVIDOR_SQL)
        eda.cargar_tabla(TABLA_SQL)

        tab1, tab2, tab3 = st.tabs([
            "Vista previa",
            "Información",
            "Estadísticas"
        ])

        with tab1:
            st.subheader("Vista previa")
            st.dataframe(eda.df)

        with tab2:
            st.subheader("Información del DataFrame")
            buffer = io.StringIO()
            eda.df.info(buf=buffer)
            st.text(buffer.getvalue())

        with tab3:
            st.subheader("Estadísticas descriptivas")
            st.dataframe(eda.estadisticas())

    except Exception as e:
        st.error(f"Error al cargar el dataset: {e}")


# ===== Página: Gráficos =====
elif st.session_state.pagina == "Gráficos":
    st.header("Visualización del Consumo y Clima")

    st.markdown("""
    A continuación se muestran algunos gráficos clave para entender el comportamiento
    del consumo eléctrico y su relación con variables climáticas:

    1. **Consumo promedio por hora del día**  
    2. **Consumo promedio por mes del año**  
    3. **Relación entre temperatura aparente y consumo eléctrico**  
    4. **Relación entre nubosidad y consumo eléctrico**  
    ---
    """)

    try:
        vis = Visualizador(SERVIDOR_SQL)
        vis.cargar_tabla(TABLA_SQL)

        tab1, tab2, tab3, tab4 = st.tabs([
            "Consumo por hora",
            "Consumo por mes",
            "Temperatura vs Consumo",
            "Nubosidad vs Consumo"
        ])

        with tab1:
            st.subheader("Consumo por hora del día")
            vis.grafico_mw_por_hora()
            st.pyplot(plt.gcf())
            plt.clf()

        with tab2:
            st.subheader("Consumo por mes del año")
            vis.grafico_mw_por_mes()
            st.pyplot(plt.gcf())
            plt.clf()

        with tab3:
            st.subheader("Temperatura vs Consumo")
            vis.grafico_mw_vs_temp()
            st.pyplot(plt.gcf())
            plt.clf()

        with tab4:
            st.subheader("Nubosidad vs Consumo")
            vis.grafico_mw_vs_nubes()
            st.pyplot(plt.gcf())
            plt.clf()

    except Exception as e:
        st.error(f"Error al generar los gráficos: {e}")
