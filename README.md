# 🌤️ ClimaIA Brasil

**Aplicação meteorológica experimental que reúne previsão de 7 dias e demonstração histórica de aprendizado de máquina para estudo de calor extremo.**

[**🌐 Acessar aplicativo**](https://climaia-brasil.streamlit.app/) · [**📊 Relatório de validação**](RELATORIO_VALIDACAO_CLIMAIA.md) · [**🧪 Código do backtesting**](validar_climaia.py)

> **Atenção:** a previsão para os próximos sete dias é fornecida pela API Open-Meteo. O modelo de IA exibido no aplicativo classifica **exemplos históricos de 2025 em Cataguases (MG)**; ele **não prevê o clima futuro** e **não emite alertas meteorológicos oficiais**.

## ✨ Funcionalidades

- Pesquisa de cidades brasileiras e seleção de município/estado.
- Previsão de temperatura máxima, mínima e precipitação para sete dias, obtida da **Open-Meteo**.
- Classificação **experimental** da temperatura máxima prevista: **normal** (abaixo de 30 °C), **atenção** (de 30 °C até menos de 35 °C) e **alerta** (35 °C ou mais).
- Indicadores de dias de atenção/alerta e gráfico de temperaturas.
- Layout responsivo para computadores e celulares.
- Demonstração de um **Random Forest pré-existente**, aplicado a observações históricas de Cataguases.

## 🧠 Experimento de ciência de dados

**Pergunta de pesquisa:** com as condições meteorológicas observadas até hoje, é possível identificar se **amanhã** terá temperatura máxima **≥ 35 °C**?

A base histórica contém **4.015 registros diários** (03/01/2015 a 30/12/2025). Após a preparação de variáveis e definição do alvo, há **4.012 exemplos elegíveis** e **67 eventos** de calor extremo. O script [`validar_climaia.py`](validar_climaia.py) executa **backtesting temporal anual**: para cada ano avaliado, treina os modelos apenas com anos anteriores.

### Avaliação agregada: 2020–2024

Foram avaliados **1.827 dias**, incluindo **27 eventos** (prevalência de aproximadamente **1,48%**). A PR-AUC apresentada corresponde à *average precision* agregada calculada sobre as pontuações de todos os anos de teste reunidos.

| Modelo | PR-AUC (AP) | Precisão @ 0,5 | Revocação @ 0,5 | Falsos alertas |
|:--|--:|--:|--:|--:|
| **Regressão Logística** | **0,3958** | 16,1% | **88,9%** | 125 |
| Extra Trees | 0,3494 | **32,2%** | 70,4% | 40 |
| Random Forest | 0,2864 | 26,7% | 29,6% | **22** |

A **Regressão Logística** teve a maior PR-AUC agregada e a maior capacidade de detecção ao limiar ilustrativo de 0,5, mas também produziu mais falsos alertas. **Isso não comprova que seja adequada para decisões operacionais.**

### Avaliação posterior: 2025

Nos **364 dias** avaliados em 2025 ocorreram **9 eventos**. Com limiar de 0,5, a Regressão Logística detectou **8 de 9** eventos e produziu **18 falsos alertas** (precisão de **30,8%** e revocação de **88,9%**).

> Os dados de 2025 já foram consultados durante o desenvolvimento; portanto, **não constituem um teste final completamente intocado**.

Leia a metodologia, os resultados anuais e todas as limitações em [**RELATORIO_VALIDACAO_CLIMAIA.md**](RELATORIO_VALIDACAO_CLIMAIA.md).

**Nota de consistência:** uma avaliação experimental anterior registrou PR-AUC de aproximadamente **0,316** para Random Forest em 2020–2024, enquanto o script publicado atualmente reproduz **0,2864** com seu próprio protocolo e hiperparâmetros. Esses resultados não devem ser confundidos. As métricas do backtesting referem-se a **novos modelos treinados pelo script**, não necessariamente ao arquivo `modelo_random_forest.pkl` carregado na interface.

## 🛠️ Tecnologias

**Python · pandas · NumPy · scikit-learn · Streamlit · Altair · Requests · Open-Meteo**

## 📂 Estrutura do projeto

```text
ClimaIA-Brasil/
├── app.py
├── requirements.txt
├── validar_climaia.py
├── RELATORIO_VALIDACAO_CLIMAIA.md
├── README.md
├── .streamlit/
│   └── config.toml
└── ClimaIA_Brasil/
    ├── config.json
    ├── historico_rf_cataguases.csv
    └── modelo_random_forest.pkl
```

## ▶️ Executar localmente

Na raiz do repositório, com Python instalado:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```powershell
.venv\Scripts\activate
```

Ou no Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências e execute o aplicativo:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Para reproduzir o backtesting:

```bash
python validar_climaia.py
```

O script cria `resultado_validacao_anual.csv` e `previsoes_validacao.csv`. A consulta da previsão depende de internet. Mantenha os arquivos da pasta `ClimaIA_Brasil/` nos caminhos originais.

## ⚠️ Limitações e próximos passos

- Os limiares de 30 °C e 35 °C são **experimentais** e não substituem alertas oficiais.
- A IA histórica foi estudada para **Cataguases (MG)**; o desempenho não pode ser generalizado para outras cidades.
- O modelo exibido no aplicativo é um **Random Forest salvo anteriormente**, sem auditoria integral do seu treinamento original. O script de backtesting treina modelos novos e não valida automaticamente esse arquivo.
- Pontuações da IA **não são probabilidades calibradas**; o limiar 0,5 é ilustrativo, não otimizado em validação independente.
- A ocorrência de eventos extremos é rara, especialmente em alguns anos. Avaliações adicionais e novos dados não utilizados no desenvolvimento são necessários.
- A **proveniência original** e eventuais transformações da base histórica ainda devem ser documentadas.
- Arquivos de modelos serializados (`.pkl`) devem ser carregados apenas de fontes confiáveis.

---

**ClimaIA Brasil é um projeto de portfólio e aprendizagem em Ciência de Dados. Não o utilize isoladamente para decisões de saúde, segurança ou defesa civil.**
