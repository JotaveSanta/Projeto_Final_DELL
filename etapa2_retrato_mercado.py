import pandas as pd

# 1. Carregando os dados diários de operação e mercado
caminho = "Recebidos/dados/daily_market.jsonl"
df_daily = pd.read_json(caminho, lines=True)

print("=== ETAPA 2: RETRATO DO MERCADO POR TIER ===\n")

# 2. Calculando Média e Mediana da Ocupação por Tier
# (A comparação entre média e mediana mostra se há assimetria ou dias extremos afetando a média)
estatisticas_ocupacao = df_daily.groupby('tier')['occupancy'].agg(
    Media_Ocupacao='mean',
    Mediana_Ocupacao='median',
    Desvio_Padrao_Ocupacao='std'
).round(4)

print("--- 1. Ocupação Típica por Tier (Valores em proporção, ex: 0.75 = 75%) ---")
print(estatisticas_ocupacao)
print("\n" + "-"*60 + "\n")

# 3. Calculando Média, Mediana e Desvio Padrão da Diária (ADR) por Tier
# (O desvio padrão e o coeficiente de variação mostram qual tier varia mais ao longo do ano)
estatisticas_adr = df_daily.groupby('tier')['adr'].agg(
    Media_ADR='mean',
    Mediana_ADR='median',
    Desvio_Padrao_ADR='std',
    Minimo_ADR='min',
    Maximo_ADR='max'
).round(2)

# Adicionando o Coeficiente de Variação (CV = Desvio Padrão / Média) para uma comparação justa entre preços altos e baixos
estatisticas_adr['Coef_Variacao_%'] = ((estatisticas_adr['Desvio_Padrao_ADR'] / estatisticas_adr['Media_ADR']) * 100).round(2)

print("--- 2. Variabilidade da Diária (ADR) por Tier ---")
print(estatisticas_adr)