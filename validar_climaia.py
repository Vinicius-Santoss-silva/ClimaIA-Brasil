"""Backtesting temporal reproduzível do ClimaIA Brasil.

Executar na raiz do repositório: python validar_climaia.py
Não modifica app.py nem o arquivo de modelo publicado.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, confusion_matrix, precision_score, recall_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'ClimaIA_Brasil' / 'historico_rf_cataguases.csv'
CFG = ROOT / 'ClimaIA_Brasil' / 'config.json'


def preparar():
    base = pd.read_csv(BASE, parse_dates=['Data']).sort_values('Data').reset_index(drop=True)
    if base['Data'].duplicated().any():
        raise ValueError('Datas duplicadas na base')
    if not base['Data'].diff().iloc[1:].eq(pd.Timedelta(days=1)).all():
        raise ValueError('Há lacunas temporais: shift/rolling não garantem dias consecutivos')
    config = json.loads(CFG.read_text(encoding='utf-8'))
    base['Maxima_Ontem'] = base['Temperatura_Maxima'].shift(1)
    base['Maxima_Anteontem'] = base['Temperatura_Maxima'].shift(2)
    base['Media_Maxima_3_Dias'] = base['Temperatura_Maxima'].rolling(3).mean()
    base['Amplitude_Termica'] = base['Temperatura_Maxima'] - base['Temperatura_Minima']
    base['Chuva_3_Dias'] = base['Chuva_mm'].rolling(3).sum()
    base['Data_Alvo'] = base['Data'] + pd.Timedelta(days=1)
    base['Maxima_Amanha'] = base['Temperatura_Maxima'].shift(-1)
    mes = base['Data_Alvo'].dt.month
    base['Mes_seno'] = np.sin(2 * np.pi * mes / 12)
    base['Mes_cosseno'] = np.cos(2 * np.pi * mes / 12)
    colunas = config['variaveis_random_forest']
    base = base.dropna(subset=colunas + ['Maxima_Amanha']).copy()
    base['Evento'] = (base['Maxima_Amanha'] >= 35).astype(int)
    return base, colunas


def novos_modelos():
    return {
        'Regressao Logistica': make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, class_weight='balanced', random_state=42)),
        'Extra Trees': ExtraTreesClassifier(n_estimators=300, min_samples_leaf=3, class_weight='balanced', random_state=42, n_jobs=-1),
        'Random Forest': RandomForestClassifier(n_estimators=300, min_samples_leaf=3, class_weight='balanced', random_state=42, n_jobs=-1),
    }


def avaliar():
    dados, features = preparar()
    print(f'Registros elegiveis: {len(dados)} | eventos >=35 C: {dados.Evento.sum()}')
    resultados = []
    previsoes = []
    # Treina sempre somente em anos anteriores ao ano avaliado.
    for nome in novos_modelos():
        for ano in range(2020, 2026):
            treino = dados[dados.Data_Alvo.dt.year < ano]
            teste = dados[dados.Data_Alvo.dt.year == ano]
            if teste.empty or treino['Evento'].nunique() < 2:
                continue
            modelo = novos_modelos()[nome]
            modelo.fit(treino[features], treino['Evento'])
            score = modelo.predict_proba(teste[features])[:, 1]
            pred = (score >= .5).astype(int)  # Limiar ilustrativo, nao otimizado.
            tn, fp, fn, tp = confusion_matrix(teste['Evento'], pred, labels=[0, 1]).ravel()
            resultados.append({
                'Modelo': nome, 'Ano': ano, 'N_teste': len(teste), 'Eventos': int(teste.Evento.sum()),
                'PR_AUC': round(float(average_precision_score(teste.Evento, score)), 5),
                'Precisao_0_5': round(float(precision_score(teste.Evento, pred, zero_division=0)), 5),
                'Revocacao_0_5': round(float(recall_score(teste.Evento, pred, zero_division=0)), 5),
                'VP': int(tp), 'FP': int(fp), 'FN': int(fn), 'VN': int(tn),
            })
            previsoes.extend({'Modelo': nome, 'Data_Alvo': d.strftime('%Y-%m-%d'), 'Observado': int(y), 'Pontuacao': float(s)}
                            for d, y, s in zip(teste.Data_Alvo, teste.Evento, score))
    r = pd.DataFrame(resultados)
    p = pd.DataFrame(previsoes)
    r.to_csv(ROOT / 'resultado_validacao_anual.csv', index=False)
    p.to_csv(ROOT / 'previsoes_validacao.csv', index=False)
    print('\nMETRICAS ANUAIS (PR-AUC por ano nao equivale a PR-AUC agregado):')
    print(r.to_string(index=False))
    print('\nPR-AUC AGREGADO 2020-2024 (todos os eventos e scores juntos):')
    for nome, grupo in p[p.Data_Alvo.str[:4].isin(map(str, range(2020, 2025)))].groupby('Modelo'):
        print(f'{nome}: {average_precision_score(grupo.Observado, grupo.Pontuacao):.4f}')
    print('\nAtenção: 2025 é uma análise temporal posterior, mas não deve ser chamado de teste intocado se seus dados já foram consultados para ajustar modelos.')
    print('Arquivos salvos: resultado_validacao_anual.csv e previsoes_validacao.csv')


if __name__ == '__main__':
    avaliar()
