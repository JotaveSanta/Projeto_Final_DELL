import os
import pandas as pd

# Caminho correto baseado na sua imagem
pasta_dados = "Recebidos/dados"

# Lista com os 7 arquivos do projeto Port Alder
arquivos = [
    "hotels.jsonl",
    "room_types.jsonl",
    "daily_market.jsonl",
    "weekly_performance.jsonl",
    "rate_decisions.jsonl",
    "reviews.jsonl",
    "review_scenarios.jsonl"
]

print("=== RESUMO GERAL DO DATASET DE PORT ALDER ===\n")

for arquivo in arquivos:
    caminho_completo = os.path.join(pasta_dados, arquivo)
    
    if os.path.exists(caminho_completo):
        df = pd.read_json(caminho_completo, lines=True)
        print(f"📁 Arquivo: {arquivo}")
        print(f"   • Linhas: {df.shape[0]}")
        print(f"   • Colunas: {df.shape[1]}")
        print(f"   • Nomes das colunas: {list(df.columns)}")
        print("-" * 50)
    else:
        print(f"⚠️ Arquivo não encontrado: {caminho_completo}")
        print("-" * 50)