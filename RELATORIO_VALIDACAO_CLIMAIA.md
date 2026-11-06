# ClimaIA Brasil — Relatório de validação temporal

**Data do registro:** 06/11/2026  
**Recorte geográfico:** Cataguases, Minas Gerais  
**Tarefa de classificação:** identificar se a temperatura máxima observada no dia seguinte será **≥ 35 °C**  
**Status:** estudo experimental de portfólio; não é um sistema de alerta oficial.

## 1. Objetivo

Avaliar a capacidade de três modelos de distinguir dias com e sem calor extremo, com separação temporal entre treinamento e teste. O script `validar_climaia.py` treina cada modelo com os anos **anteriores** ao ano avaliado, evitando misturar observações futuras na amostra de treino de cada avaliação anual.

A análise usa os atributos meteorológicos disponíveis até o dia atual (temperaturas, precipitação, médias móveis e informações sazonais) para estimar a ocorrência de um evento no dia seguinte. Essa avaliação **não** comprova que a mesma qualidade será obtida com entradas de previsão meteorológica em vez de observações históricas.

## 2. Base e protocolo

- Base histórica original: **4.015 registros diários** (03/01/2015 a 30/12/2025).
- Após preparar defasagens e alvo: **4.012 registros elegíveis**, dos quais **67 eventos** ≥ 35 °C.
- **2020–2024:** 1.827 observações e 27 eventos (prevalência **1,48%**).
- **2025:** 364 observações e 9 eventos (prevalência **2,47%**).
- Datas na base: sem duplicatas ou lacunas na sequência; não foram encontrados valores numéricos inválidos nas quatro colunas.
- Modelos: Regressão Logística (com `StandardScaler` dentro do pipeline), Extra Trees e Random Forest.
- Separação temporal: para cada ano de teste de 2020 a 2025, treinamento em anos anteriores, como definido em `validar_climaia.py`.
- Limiar de classificação dos resultados abaixo: **0,5**, escolhido como referência ilustrativa, **não otimizado**.
- PR-AUC apresentada = **average precision (AP)** do scikit-learn, que é uma medida da curva precisão-revocação; não é necessariamente igual à área calculada pela regra trapezoidal.

## 3. Comparação agregada — 2020 a 2024

| Modelo | AP / PR-AUC agregada | Verdadeiros positivos | Falsos positivos | Falsos negativos | Precisão @ 0,5 | Revocação @ 0,5 |
|:--|--:|--:|--:|--:|--:|--:|
| **Regressão Logística** | **0,3958** | 24 | 125 | 3 | 16,1% | 88,9% |
| Extra Trees | 0,3494 | 19 | 40 | 8 | 32,2% | 70,4% |
| Random Forest | 0,2864 | 8 | 22 | 19 | 26,7% | 29,6% |

Os 27 eventos reais correspondem a apenas **1,48%** dos dias de teste. A Regressão Logística apresenta maior AP agregada e alta revocação, porém emite **125 falsos positivos** no recorte de cinco anos ao limiar 0,5. Extra Trees gera menos falsos positivos, à custa de deixar passar mais eventos. A escolha depende do custo relativo desses erros e não pode ser decidida apenas pela AP.

### AP por ano

| Modelo | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|:--|--:|--:|--:|--:|--:|--:|
| Regressão Logística | 0,44739 | 0,27624 | 0,04167 | 0,58085 | 0,22549 | 0,42729 |
| Extra Trees | 0,64145 | 0,22941 | 0,10000 | 0,58206 | 0,12500 | 0,32308 |
| Random Forest | 0,53111 | 0,27679 | 0,07692 | 0,48693 | 0,21014 | 0,33510 |

**Nota:** médias aritméticas dos valores de AP por ano não substituem a AP calculada sobre todas as observações e pontuações do período, que é a métrica agregada apresentada acima. Alguns anos têm apenas 1 ou 2 eventos; as métricas por ano são especialmente instáveis nesses casos.

## 4. Avaliação posterior — 2025

| Modelo | AP / PR-AUC | Verdadeiros positivos | Falsos positivos | Falsos negativos | Verdadeiros negativos | Precisão @ 0,5 | Revocação @ 0,5 |
|:--|--:|--:|--:|--:|--:|--:|--:|
| **Regressão Logística** | **0,42729** | 8 | 18 | 1 | 337 | 30,8% | 88,9% |
| Extra Trees | 0,32308 | 4 | 8 | 5 | 347 | 33,3% | 44,4% |
| Random Forest | 0,33510 | 1 | 5 | 8 | 350 | 16,7% | 11,1% |

Em 2025, a Regressão Logística detectou **8 dos 9** eventos, com **18 falsos alertas**. Isso representa uma revocação de 88,9%, **não** uma precisão de 88,9%: quando o modelo sinalizou um evento, 8 de 26 alertas corresponderam a eventos verdadeiros (30,8% de precisão).

**Atenção:** os dados de 2025 já foram consultados durante o desenvolvimento, portanto não devem ser descritos como um teste final totalmente intocado.

## 5. Limitações e risco de interpretação

1. **Modelo no app diferente do melhor candidato no backtesting:** a demonstração histórica atualmente carrega um arquivo Random Forest pré-existente. Os números deste relatório resultam de novos treinamentos no script de avaliação. Eles não devem ser atribuídos automaticamente ao arquivo `.pkl` já publicado.
2. **Diferença em relação a resultados experimentais anteriores:** houve um valor de Random Forest ≈ **0,316** reportado em avaliação anterior, enquanto o script atualmente reproduz **0,2864** no agregado 2020–2024. Não são medições intercambiáveis; a diferença deve ser investigada comparando hiperparâmetros, recortes, pré-processamento e procedimento de validação.
3. **Limiar não otimizado:** 0,5 é apenas referência. Não foi feita escolha de limiar com validação temporal interna independente de cada teste anual.
4. **Sem calibração de probabilidades:** pontuações não devem ser lidas como probabilidades confiáveis de ocorrência.
5. **Eventos raros:** 27 ocorrências no recorte 2020–2024 e nove em 2025. A amostra positiva é pequena e os resultados podem mudar em outros períodos.
6. **Fonte de dados históricos:** a proveniência, eventuais transformações, metadados e política de atualização da base precisam ser documentados separadamente.
7. **Aplicação meteorológica:** a previsão de sete dias vem da Open-Meteo; não é produzida pelos modelos de classificação deste relatório.
8. **Uso operacional:** não usar o sistema para decisões de segurança, saúde ou alertas meteorológicos oficiais.

## 6. Conclusão

**Principal candidata para estudos futuros: Regressão Logística**, por apresentar a maior AP agregada e a maior revocação em 2025 no protocolo realizado. Isso **não significa** que a solução esteja validada para emitir alertas em produção. O compromisso de detectar mais eventos gera falsos alertas, e ainda é necessário definir um procedimento de escolha de limiar sem contaminação do conjunto de teste.

A apresentação correta do ClimaIA Brasil neste estágio é: **aplicação meteorológica com consulta de previsão por API e experimento de inteligência artificial demonstrado sobre dados históricos**, acompanhada de backtesting reproduzível.

## 7. Reproduzir a avaliação

Na raiz do repositório, com as dependências instaladas:

```bash
python validar_climaia.py
```

O script lê `ClimaIA_Brasil/historico_rf_cataguases.csv` e `ClimaIA_Brasil/config.json` e gera `resultado_validacao_anual.csv` e `previsoes_validacao.csv` com os resultados da execução. Não altera o aplicativo Streamlit nem o modelo serializado em produção.

---
*Relatório baseado nos resultados do script `validar_climaia.py` apresentados em 06/11/2026. As métricas não foram recalculadas independentemente neste documento.*
