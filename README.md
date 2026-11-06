
🌤️ ClimaIA Brasil
Aplicação meteorológica experimental que combina previsões de 7 dias e demonstração histórica de inteligência artificial para identificação de calor extremo. Projeto de portfólio em Ciência de Dados com Python, Streamlit e scikit-learn.

A previsão futura é fornecida pela API Open-Meteo. O modelo de IA na interface apresenta exemplos históricos de 2025 para Cataguases (MG), não previsões futuras produzidas pela IA nem alertas oficiais.

Funcionalidades
Busca de cidades brasileiras e consulta de previsão meteorológica para os próximos 7 dias.
Temperaturas máximas, mínimas e precipitação previstas pela Open-Meteo.
Classificação experimental baseada na máxima prevista: normal (<30 °C), atenção (30 a <35 °C), alerta (≥35 °C).
Indicadores, gráfico de temperaturas e interface responsiva para celular e computador.
Demonstração de um modelo Random Forest preexistente usando exemplos históricos de 2025 de Cataguases.
Validação temporal reproduzível
O script `validar_climaia.py` executa backtesting anual, treinando cada modelo apenas com anos anteriores ao ano avaliado. A base histórica contém 4.015 observações diárias de 03/01/2015 a 30/12/2025; após a engenharia de atributos e a definição do alvo, restam 4.012 exemplos elegíveis e 67 eventos de temperatura máxima ≥35 °C.

Métricas agregadas — 2020–2024
O conjunto de avaliação contém 1.827 dias e 27 eventos (prevalência de aproximadamente 1,48%). PR-AUC abaixo corresponde à average precision calculada sobre todas as previsões anuais reunidas.

Modelo	AP / PR-AUC	Precisão @ 0,5	Revocação @ 0,5	Falsos alertas
Regressão Logística	0,3958	16,1%	88,9%	125
Extra Trees	0,3494	32,2%	70,4%	40
Random Forest	0,2864	26,7%	29,6%	22
A Regressão Logística teve a maior AP, mas produziu mais falsos alertas no limiar ilustrativo de 0,5. Não há comprovação de adequação operacional.

Avaliação posterior — 2025
Foram avaliados 364 dias e 9 eventos. No limiar de 0,5, a Regressão Logística identificou 8 de 9 eventos, com 18 falsos positivos (precisão de 30,8% e revocação de 88,9%). O período não deve ser descrito como teste completamente intocado, pois seus dados já foram examinados durante o desenvolvimento.

Importante: um resultado experimental anterior indicava AP de aproximadamente 0,316 para Random Forest em 2020–2024. O script atual reproduz 0,2864 com seu próprio protocolo e hiperparâmetros; essas medições não devem ser confundidas. Além disso, a avaliação treina novos modelos e não valida automaticamente o arquivo modelo_random_forest.pkl usado no aplicativo.

Para todas as métricas, tabelas por ano, metodologia e limitações, leia o Relatório de validação temporal.

Estrutura do repositório
app.py
requirements.txt
validar_climaia.py
RELATORIO_VALIDACAO_CLIMAIA.md
README.md
.streamlit/config.toml
ClimaIA_Brasil/
    config.json
    historico_rf_cataguases.csv
    modelo_random_forest.pkl
Executar localmente
Na pasta raiz do repositório, com Python instalado:

python -m venv .venv
Ative o ambiente no Windows:

.venv\Scripts\activate
Ou no Linux/macOS:

source .venv/bin/activate
Depois, instale e execute:

pip install -r requirements.txt
streamlit run app.py
Para reproduzir o backtesting (gera resultado_validacao_anual.csv e previsoes_validacao.csv):

python validar_climaia.py
A previsão meteorológica depende de conexão com a internet; os arquivos de ClimaIA_Brasil/ devem permanecer nos caminhos previstos.

Como funciona a demonstração histórica de IA
O aplicativo carrega o arquivo modelo_random_forest.pkl com joblib e calcula variáveis derivadas de temperaturas, chuva, médias móveis e sazonalidade. A demonstração classifica exemplos históricos de temperatura máxima ≥35 °C no dia seguinte, mas não emite previsões futuras produzidas pela IA. As pontuações do modelo não foram calibradas como probabilidades confiáveis.

Limitações e próximos passos
Os limiares de 30 °C e 35 °C são experimentais e não substituem avisos oficiais.
A IA histórica foi desenvolvida para Cataguases, sem validação para generalização a outras cidades.
Eventos extremos são raros; os resultados por ano variam bastante e exigem interpretação cuidadosa.
O limiar 0,5 é ilustrativo. Uma futura seleção de limiares deve ocorrer sem consultar os dados de teste.
Ainda falta documentar a proveniência original da base histórica e avaliar calibração, incerteza e desempenho em dados posteriores não consultados durante o desenvolvimento.
Arquivos .pkl só devem ser carregados de fontes confiáveis. O modelo usado na interface não deve receber, sem auditoria adicional, as métricas de novos modelos treinados no backtesting.
Falta testar a implantação pública em desktop e smartphone.
Tecnologias
Python · pandas · NumPy · scikit-learn · Streamlit · Altair · Requests · Open-Meteo

ClimaIA Brasil é um experimento de portfólio em Ciência de Dados, não um serviço oficial de previsão de riscos. Não usar isoladamente para decisões de saúde, segurança ou defesa civil.

0
