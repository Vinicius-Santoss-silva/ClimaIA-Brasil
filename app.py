
import streamlit as st
import requests
import pandas as pd

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
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background-color: #0B4C91;
    color: white;
}

</style>
""", unsafe_allow_html=True)



# ETAPA 40 - CABECALHO CORRIGIDO
st.html("""
<div style="background:linear-gradient(120deg,#123B73,#1675C5);
border-radius:18px;padding:32px;color:white;margin-bottom:24px;">
<div style="font-size:13px;color:#CDE9FF;">
PLATAFORMA METEOROLÓGICA EXPERIMENTAL
</div>
<div style="font-size:38px;font-weight:800;color:white;">
🌤️ ClimaIA Brasil
</div>
<div style="font-size:16px;color:#E2F1FF;margin-top:10px;">
Dados meteorológicos e monitoramento de calor no Brasil.
</div>
</div>
""")

st.subheader("Previsão Meteorológica e Análise de Calor")

st.write(
    "Pesquise sua cidade e consulte as temperaturas "
    "previstas para os próximos 7 dias."
)

# Guardar consultas por 1 hora para reduzir
# solicitações repetidas à API.
@st.cache_data(ttl=3600)
def buscar_cidade(nome):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    resposta = requests.get(
        url,
        params={
            "name": nome,
            "count": 10,
            "language": "pt",
            "countryCode": "BR"
        },
        timeout=20
    )

    resposta.raise_for_status()
    return resposta.json().get("results", [])


@st.cache_data(ttl=3600)
def consultar_previsao(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    resposta = requests.get(
        url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum"
            ],
            "timezone": "auto",
            "forecast_days": 7
        },
        timeout=30
    )

    resposta.raise_for_status()
    return resposta.json()["daily"]


# Campo de pesquisa
with st.form("pesquisa"):
    cidade = st.text_input(
        "📍 Digite sua cidade:",
        placeholder="Exemplo: Cataguases, MG"
    )

    consultar = st.form_submit_button(
        "Consultar previsão"
    )


if consultar:
    st.session_state["cidade_pesquisada"] = cidade.strip()
    st.session_state.pop("cidade_local_escolhida", None)

if st.session_state.get("cidade_pesquisada"):
    cidade = st.session_state["cidade_pesquisada"]
    if len(cidade.strip()) < 2:
        st.warning("Digite o nome de uma cidade.")
    else:
        try:
            locais = buscar_cidade(cidade.strip())

            if not locais:
                st.warning("Cidade não encontrada.")
            else:
                # Selecionar o primeiro resultado brasileiro
                indice = st.selectbox(
                    "Selecione a cidade e o estado:",
                    options=list(range(len(locais))),
                    format_func=lambda i: (
                        f"{locais[i]['name']} - "
                        f"{locais[i].get('admin1', 'Brasil')}"
                    ),
                    key="cidade_local_escolhida"
                )

                local = locais[indice]

                st.success(
                    f"Cidade encontrada: {local['name']} "
                    f"- {local.get('admin1', 'Brasil')}"
                )

                dados = consultar_previsao(
                    local["latitude"],
                    local["longitude"]
                )

                tabela = pd.DataFrame({
                    "Data": dados["time"],
                    "Máxima (°C)": dados["temperature_2m_max"],
                    "Mínima (°C)": dados["temperature_2m_min"],
                    "Chuva (mm)": dados["precipitation_sum"]
                })

                # ETAPA 36 - Classificacao diaria
                def nivel_calor(temperatura):
                    if temperatura >= 35:
                        return "🔴 Alerta"
                    elif temperatura >= 30:
                        return "🟠 Atenção"
                    return "🟢 Normal"

                tabela["Nível de calor"] = (
                    tabela["Máxima (°C)"].apply(nivel_calor)
                )

                st.subheader("📊 Previsão dos próximos 7 dias")
                st.dataframe(tabela, hide_index=True)

                # ETAPA 34 - ALERTAS DE CALOR
                st.subheader("🚨 Monitoramento de calor")

                maxima = tabela["Máxima (°C)"].max()
                dias_atencao = (
                    (tabela["Máxima (°C)"] >= 30) &
                    (tabela["Máxima (°C)"] < 35)
                ).sum()
                dias_alerta = (
                    tabela["Máxima (°C)"] >= 35
                ).sum()

                c1, c2, c3 = st.columns(3)

                c1.metric("Maior máxima", f"{maxima:.1f} °C")
                c2.metric("Dias de atenção", int(dias_atencao))
                c3.metric("Dias em alerta", int(dias_alerta))

                if dias_alerta > 0:
                    st.error("Alerta experimental de calor elevado.")
                elif dias_atencao > 0:
                    st.warning("Atenção: dias quentes previstos.")
                else:
                    st.success("Temperaturas abaixo de 30 °C.")

                st.caption(
                    "Limites experimentais, não alertas oficiais."
                )

                st.subheader("🌡️ Gráfico de temperaturas")

                st.line_chart(
                    tabela.set_index("Data")[
                        ["Máxima (°C)", "Mínima (°C)"]
                    ]
                )

        except requests.exceptions.HTTPError as erro:
            if erro.response.status_code == 429:
                st.warning(
                    "A API atingiu seu limite de consultas. "
                    "Tente novamente mais tarde."
                )
            else:
                st.error(f"Erro na API: {erro}")

        except requests.exceptions.RequestException:
            st.error("Não foi possível consultar o clima.")

st.divider()


# ETAPA 45 - IA HISTORICA
st.divider()
st.subheader("🤖 Inteligência Artificial - ClimaIA")

st.info(
    "Modelo experimental treinado para Cataguases - MG. "
    "A demonstração abaixo utiliza dados históricos, "
    "não previsões meteorológicas futuras."
)

from pathlib import Path
import joblib
import json
import numpy as np

pasta_ia = Path("ClimaIA_Brasil")
caminho_modelo = pasta_ia / "modelo_random_forest.pkl"
caminho_base = pasta_ia / "historico_rf_cataguases.csv"
caminho_config = pasta_ia / "config.json"

if all(p.exists() for p in [
    caminho_modelo, caminho_base, caminho_config
]):
    @st.cache_resource
    def carregar_ia():
        return joblib.load(caminho_modelo)

    modelo = carregar_ia()
    config = json.loads(
        caminho_config.read_text(encoding="utf-8")
    )

    historico_ia = pd.read_csv(
        caminho_base, parse_dates=["Data"]
    ).sort_values("Data")

    h = historico_ia.copy()

    h["Maxima_Ontem"] = h["Temperatura_Maxima"].shift(1)
    h["Maxima_Anteontem"] = h["Temperatura_Maxima"].shift(2)

    h["Media_Maxima_3_Dias"] = (
        h["Temperatura_Maxima"].rolling(3).mean()
    )

    h["Amplitude_Termica"] = (
        h["Temperatura_Maxima"] - h["Temperatura_Minima"]
    )

    h["Chuva_3_Dias"] = h["Chuva_mm"].rolling(3).sum()

    h["Data_Alvo"] = h["Data"] + pd.Timedelta(days=1)
    h["Maxima_Amanha"] = h["Temperatura_Maxima"].shift(-1)

    mes = h["Data_Alvo"].dt.month
    h["Mes_seno"] = np.sin(2 * np.pi * mes / 12)
    h["Mes_cosseno"] = np.cos(2 * np.pi * mes / 12)

    colunas = config["variaveis_random_forest"]

    exemplos = h.dropna(
        subset=colunas + ["Maxima_Amanha"]
    )

    exemplos = exemplos[
        exemplos["Data_Alvo"].dt.year == 2025
    ].tail(7).copy()

    if not exemplos.empty:
        pontuacoes = modelo.predict_proba(
            exemplos[colunas]
        )[:, 1]

        resultado_ia = pd.DataFrame({
            "Data": exemplos["Data_Alvo"].dt.strftime("%d/%m/%Y"),
            "Máxima observada (°C)": exemplos["Maxima_Amanha"].values,
            "Pontuação da IA (%)": np.round(
                pontuacoes * 100, 1
            ),
            "Classificação da IA": [
                "Alerta" if p >= 0.6 else "Normal"
                for p in pontuacoes
            ]
        })

        st.success("Modelo Random Forest carregado!")
        st.write("Exemplos históricos de 2025:")
        st.dataframe(resultado_ia, hide_index=True)

        st.caption(
            "Pontuações não calibradas. "
            "O modelo ainda não é um sistema oficial "
            "de alerta e precisa de validação adicional."
        )

else:
    st.warning(
        "Arquivos da IA não encontrados no ambiente."
    )


st.caption(
    "ClimaIA Brasil | Projeto experimental de Ciência de Dados"
)
