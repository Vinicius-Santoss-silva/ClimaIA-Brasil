
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
/* ClimaIA Brasil — identidade visual unificada e responsiva */
:root { color-scheme: light; }
.stApp { background: linear-gradient(135deg, #F0F7FF 0%, #FFFFFF 100%); }
.block-container {
    max-width: 1100px;
    padding-top: 1.4rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #12345A;
    font-family: Arial, sans-serif;
    overflow-wrap: anywhere;
}
.climaia-hero {
    background: linear-gradient(120deg, #123B73, #1675C5);
    border-radius: 18px;
    padding: 25px 29px;
    color: #FFFFFF;
    margin-bottom: 18px;
}
.climaia-hero-eyebrow {
    font-size: .76rem;
    letter-spacing: .09em;
    color: #D8EAFF;
    font-weight: 600;
}
.climaia-hero-title {
    font-size: clamp(1.75rem, 4vw, 2.45rem);
    line-height: 1.18;
    margin: 11px 0;
    font-weight: 800;
    color: #FFFFFF;
    overflow-wrap: anywhere;
}
.climaia-hero-subtitle { color: #E2F1FF; font-size: .98rem; line-height: 1.5; }

div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #DCE8F5;
    box-shadow: 0 4px 12px rgba(0,0,0,0.04);
}
div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #DCE8F5;
    border-radius: 14px;
    padding: 15px;
}
div[data-testid="stFormSubmitButton"] button {
    background-color: #1769C2;
    color: #FFFFFF;
    border-radius: 10px;
    border: none;
    font-weight: 700;
}
div[data-testid="stFormSubmitButton"] button:hover { background-color: #0B4C91; color: #FFFFFF; }

/* Desktop mostra tabelas e indicadores nativos do Streamlit. */
.climaia-mobile-cards, .climaia-mobile-kpis { display: none; }

/* Layout compacto para smartphones. */
@media (max-width: 640px) {
    .block-container { padding: .65rem .8rem 2rem !important; }
    h1, h2, h3 {
        font-size: 1.23rem !important;
        line-height: 1.35 !important;
        overflow-wrap: anywhere;
    }
    .climaia-hero { padding: 19px 17px; border-radius: 14px; margin-bottom: 14px; }
    .climaia-hero-title { font-size: 1.9rem !important; }
    .climaia-hero-subtitle { font-size: .88rem; }
    .climaia-hero-eyebrow { font-size: .67rem; }
    div[data-testid="stForm"] { padding: 10px; }

    /* Não reservar espaço para as versões desktop. */
    .st-key-climaia-desktop-previsao,
    .st-key-climaia-desktop-ia,
    .st-key-climaia-kpis-desktop { display: none !important; }

    .climaia-mobile-cards {
        display: grid !important;
        grid-template-columns: 1fr;
        gap: 9px;
        margin: 0 0 12px;
    }
    .climaia-mobile-card {
        background: #FFFFFF;
        border: 1px solid #DCE8F5;
        border-radius: 12px;
        padding: 10px 12px;
        box-shadow: 0 2px 8px rgba(18, 52, 90, 0.04);
        color: #12345A;
    }
    .climaia-card-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 9px;
        font-weight: 700;
        font-size: .85rem;
    }
    .climaia-card-date { color: #12345A; font-variant-numeric: tabular-nums; }
    .climaia-card-tag {
        font-size: .72rem;
        font-weight: 700;
        padding: 4px 8px;
        border-radius: 999px;
        background: #EAF3FC;
        color: #12345A;
    }
    .climaia-card-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 5px;
    }
    .climaia-card-grid-ia { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .climaia-card-cell { min-width: 0; }
    .climaia-card-label {
        color: #536B83;
        font-size: .7rem;
        line-height: 1.3;
    }
    .climaia-card-value {
        color: #12345A;
        font-size: .95rem;
        font-weight: 700;
        margin-top: 3px;
        overflow-wrap: anywhere;
        font-variant-numeric: tabular-nums;
    }
    .climaia-mobile-kpis {
        display: grid !important;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 7px;
        margin: 4px 0 13px;
    }
    .climaia-kpi {
        background: #FFFFFF;
        border: 1px solid #DCE8F5;
        border-radius: 12px;
        padding: 11px 8px;
        text-align: center;
        min-width: 0;
    }
    .climaia-kpi-label {
        font-size: .7rem;
        color: #536B83;
        line-height: 1.2;
        min-height: 2.4em;
    }
    .climaia-kpi-value {
        font-size: 1.2rem;
        font-weight: 800;
        color: #12345A;
        line-height: 1.3;
        margin-top: 4px;
        font-variant-numeric: tabular-nums;
    }
}
</style>
""", unsafe_allow_html=True)



# ETAPA 40 - CABECALHO CORRIGIDO
st.html("""
<section class="climaia-hero">
    <div class="climaia-hero-eyebrow">PLATAFORMA METEOROLÓGICA EXPERIMENTAL</div>
    <div class="climaia-hero-title">🌤️ ClimaIA Brasil</div>
    <div class="climaia-hero-subtitle">Dados meteorológicos e monitoramento de calor no Brasil.</div>
</section>
""")

st.subheader("Previsão Meteorológica e Análise de Calor")

st.write(
    "Pesquise sua cidade e consulte as temperaturas "
    "previstas para os próximos 7 dias."
)


# Mostrar tabela completa no computador e cartões legíveis no celular.
# O CSS oculta a versão que não corresponde ao tamanho da tela.
def mostrar_tabela_responsiva(dados_tabela, tipo):
    from html import escape

    with st.container(key=f"climaia-desktop-{tipo}"):
        st.dataframe(dados_tabela, hide_index=True, width="stretch")

    def formato_numero(valor, unidade=""):
        return f"{float(valor):.1f}".replace(".", ",") + unidade

    def celula(rotulo, valor):
        return (
            '<div class="climaia-card-cell">'
            f'<div class="climaia-card-label">{escape(rotulo)}</div>'
            f'<div class="climaia-card-value">{escape(str(valor))}</div>'
            '</div>'
        )

    cartoes = []
    for _, linha in dados_tabela.iterrows():
        if tipo == "previsao":
            data = pd.to_datetime(linha["Data"]).strftime("%d/%m/%Y")
            nivel = str(linha["Nível de calor"])
            conteudo = (
                celula("Máxima", formato_numero(linha["Máxima (°C)"], " °C"))
                + celula("Mínima", formato_numero(linha["Mínima (°C)"], " °C"))
                + celula("Chuva", formato_numero(linha["Chuva (mm)"], " mm"))
            )
            marcador = nivel
        elif tipo == "ia":
            data = str(linha["Data"])
            marcador = str(linha["Classificação da IA"])
            conteudo = (
                celula("Máxima observada", formato_numero(linha["Máxima observada (°C)"], " °C"))
                + celula("Pontuação da IA", formato_numero(linha["Pontuação da IA (%)"], "%"))
            )
        else:
            raise ValueError("Tipo de tabela desconhecido")

        cartoes.append(
            '<div class="climaia-mobile-card">'
            '<div class="climaia-card-head">'
            f'<span class="climaia-card-date">{escape(data)}</span>'
            f'<span class="climaia-card-tag">{escape(marcador)}</span>'
            '</div>'
            f'<div class="climaia-card-grid{(" climaia-card-grid-ia" if tipo == "ia" else "")}">{conteudo}</div>'
            '</div>'
        )

    st.html('<div class="climaia-mobile-cards">' + ''.join(cartoes) + '</div>')


# Guardar consultas por 1 hora para reduzir
# solicitações repetidas à API.
@st.cache_data(ttl=3600)
def buscar_cidade(nome):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    resposta = requests.get(
        url,
        params={
            "name": nome.split(",", 1)[0].strip(),
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
        placeholder="Ex.: Cataguases"
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
                mostrar_tabela_responsiva(tabela, "previsao")

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

                with st.container(key="climaia-kpis-desktop"):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Maior máxima", f"{maxima:.1f} °C")
                    c2.metric("Dias de atenção", int(dias_atencao))
                    c3.metric("Dias em alerta", int(dias_alerta))

                # Mesmos indicadores em formato compacto apenas no celular.
                maxima_texto = f"{maxima:.1f}".replace(".", ",")
                st.html(f"""
                <div class="climaia-mobile-kpis">
                    <div class="climaia-kpi">
                        <div class="climaia-kpi-label">Maior máxima</div>
                        <div class="climaia-kpi-value">{maxima_texto}°C</div>
                    </div>
                    <div class="climaia-kpi">
                        <div class="climaia-kpi-label">Dias de atenção</div>
                        <div class="climaia-kpi-value">{int(dias_atencao)}</div>
                    </div>
                    <div class="climaia-kpi">
                        <div class="climaia-kpi-label">Dias em alerta</div>
                        <div class="climaia-kpi-value">{int(dias_alerta)}</div>
                    </div>
                </div>
                """)

                if dias_alerta > 0:
                    st.error("Alerta experimental de calor elevado.")
                elif dias_atencao > 0:
                    st.warning("Atenção: dias quentes previstos.")
                else:
                    st.success("Temperaturas abaixo de 30 °C.")

                st.caption(
                    "Classificação experimental por temperatura máxima: "
                    "30–34,9 °C (atenção) e 35 °C ou mais (alerta). "
                    "Não substitui alertas oficiais."
                )

                st.subheader("🌡️ Gráfico de temperaturas")

                # Gráfico sem balão flutuante (tooltip) ao tocar na tela.
                dados_grafico = tabela.melt(
                    id_vars="Data",
                    value_vars=["Máxima (°C)", "Mínima (°C)"],
                    var_name="Tipo",
                    value_name="Temperatura"
                )
                dados_grafico["Data"] = pd.to_datetime(dados_grafico["Data"])

                grafico = (
                    alt.Chart(dados_grafico)
                    .mark_line(strokeWidth=3, tooltip=False)
                    .encode(
                        x=alt.X("Data:T", title=None, axis=alt.Axis(format="%d/%m", labelAngle=0)),
                        y=alt.Y("Temperatura:Q", title="Temperatura (°C)", scale=alt.Scale(zero=False)),
                        color=alt.Color("Tipo:N", title=None)
                    )
                    .properties(height=280)
                )
                st.altair_chart(
                    grafico,
                    width="stretch",
                    alt="Temperaturas máxima e mínima previstas para os próximos sete dias",
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
        limite_ia = float(config.get("limite_random_forest", 0.6))
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
                "Alerta" if p >= limite_ia else "Normal"
                for p in pontuacoes
            ]
        })

        st.success("Modelo Random Forest carregado!")
        st.write("Exemplos históricos de 2025:")
        mostrar_tabela_responsiva(resultado_ia, "ia")

        st.caption(
            "Exemplos de 2025, não previsões futuras. "
            "Pontuações não calibradas; o Random Forest precisa de "
            "avaliação temporal antes de ser usado para decisões. "
            "Este projeto não emite alertas oficiais."
        )

else:
    st.warning(
        "Arquivos da IA não encontrados no ambiente."
    )


st.caption(
    "ClimaIA Brasil | Projeto experimental de Ciência de Dados"
)
