
import streamlit as st
import requests
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="ClimaIA Brasil",
    page_icon="🌤️",
    layout="wide"
)


# ETAPA 38 - IDENTIDADE VISUAL

st.markdown("""
<style>

/* AJUSTES PARA CELULAR */
@media (max-width: 640px) {

    /* Margens da página */
    .block-container {
        padding: 1rem !important;
    }

    /* Títulos menores */
    h1, h2, h3 {
        font-size: 1.35rem !important;
        line-height: 1.3 !important;
        overflow-wrap: anywhere;
    }

    /* Cartões mais compactos */
    div[data-testid="stMetric"] {
        padding: 12px 16px !important;
        border-radius: 12px !important;
    }

    /* Números dos indicadores */
    div[data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
    }

    /* Textos dos indicadores */
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
    }

}

/* Fundo principal */
.stApp {
    background: linear-gradient(
        135deg, #F0F7FF, #FFFFFF
    );
}

/* Área principal */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Títulos */
h1, h2, h3 {
    color: #12345A;
    font-family: Arial, sans-serif;
}

h1 {
    font-weight: 800;
}

/* Indicadores */
div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #DCE8F5;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

/* Área de pesquisa */
div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #DCE8F5;
    border-radius: 14px;
    padding: 20px;
}

/* Botão de consulta */
div[data-testid="stFormSubmitButton"] button {
    background-color: #1769C2;
    color: white;
