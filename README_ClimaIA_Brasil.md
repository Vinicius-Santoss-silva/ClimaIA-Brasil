# 🌤️ ClimaIA Brasil

**Aplicação meteorológica experimental que combina previsões de 7 dias e demonstração histórica de inteligência artificial para identificação de calor extremo.** Projeto de portfólio em Ciência de Dados, utilizando Python, Streamlit e scikit-learn.

> A previsão futura é fornecida pela API Open-Meteo. O modelo de IA apresenta exemplos históricos de 2025 para Cataguases (MG), **não** previsões futuras produzidas pela IA nem alertas oficiais.

## Funcionalidades

- Busca de cidades brasileiras e consulta de previsão meteorológica para os próximos 7 dias.
- Temperaturas máximas, mínimas e precipitação prevista pela [Open-Meteo](https://open-meteo.com/).
- Classificação experimental por máxima prevista: normal (<30 °C), atenção (30 a <35 °C), alerta (≥35 °C).
- Indicadores, gráfico de temperaturas e interface responsiva para celular/computador.
- Demonstração do modelo Random Forest usando exemplos históricos de 2025 de Cataguases.

## Modelos e resultados experimentais

Na avaliação registrada em 05/11/2026, o backtesting informado para 2020–2024 apresentou:

| Modelo | PR-AUC |
| --- | ---: |
| Regressão Logística | 0,396 |
| Extra Trees | 0,349 |
| Random Forest | 0,316 |

O conjunto de teste informado contou com **1.827 registros**, **27 eventos** de temperatura máxima ≥35 °C e prevalência aproximada de **1,5%**. A base elegível informada tinha 4.012 registros e 67 eventos. Estes números provêm da avaliação experimental realizada durante o desenvolvimento e **não são reproduzidos automaticamente pelo código publicado atualmente**. A PR-AUC mede a qualidade de ordenação para a classe rara, mas não assegura adequação para alertas operacionais.

## Estrutura do repositório

```text
app.py
requirements.txt
.streamlit/config.toml
ClimaIA_Brasil/
    config.json
    historico_rf_cataguases.csv
    modelo_random_forest.pkl
```

## Rodar localmente

A partir da raiz do repositório, com Python instalado:

```bash
python -m venv .venv
```

Ative o ambiente no Windows:

```powershell
.venv\Scripts\activate
```

Ou no Linux/macOS:

```bash
source .venv/bin/activate
```

Em seguida:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Mantenha os arquivos da pasta `ClimaIA_Brasil/` nos caminhos originais. A previsão depende de conexão com a internet.

## Como funciona a IA histórica

O modelo Random Forest salvo em `modelo_random_forest.pkl` é carregado com `joblib`. O aplicativo calcula atributos derivados de temperaturas máximas e mínimas, chuva, médias móveis e sazonalidade. O evento-alvo é temperatura máxima **≥35 °C no dia seguinte**. A aplicação mostra os últimos sete exemplos elegíveis de 2025, **sem inferência para os sete dias futuros**. As pontuações do modelo não estão calibradas para representar probabilidades confiáveis.

## Limitações e cautelas

1. Os limiares de 30 °C e 35 °C são definições experimentais e **não substituem avisos oficiais de defesa civil ou meteorologia**.
2. A IA histórica foi desenvolvida para Cataguases (MG); não há validação que autorize generalizar seu desempenho a todas as cidades brasileiras.
3. Os resultados de comparação ainda requerem publicação de um pipeline reprodutível de preparação, treino e backtesting, com períodos e sementes documentados.
4. Antes de uso mais amplo, é essencial verificar duplicatas e lacunas nas datas, construir defasagens apenas entre dias efetivamente consecutivos, separar treino/validação/teste temporalmente e escolher limiares sem consultar dados de teste.
5. Como os eventos ≥35 °C são raros, devem ser reportados também precisão, revocação, falsos positivos, calibração e análise de incerteza, preferencialmente por ano.
6. Arquivos `.pkl` devem ser carregados somente de fontes confiáveis.

## Próximos passos científicos

- Disponibilizar script/notebook para reproduzir métricas e escolhas dos modelos.
- Testar em intervalo posterior que não tenha orientado ajustes nem seleção de modelo.
- Validar execução do aplicativo publicado em computador e celular.
- Documentar as fontes originais dos dados históricos, sua cobertura e lacunas.

## Tecnologias

Python · pandas · NumPy · scikit-learn · Streamlit · Altair · Requests · Open-Meteo

---

**Projeto experimental de portfólio em Ciência de Dados. Não utilizar isoladamente para decisões de saúde, segurança ou defesa civil.**
