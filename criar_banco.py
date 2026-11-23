import os
import sqlite3
import json
import pandas as pd

# Nome do arquivo do banco de dados SQLite
nome_banco = "banco/port_alder.db"

# Garante que a pasta 'banco' existe
os.makedirs("banco", exist_ok=True)

# Conectando ao SQLite
conexao = sqlite3.connect(nome_banco)

tabelas = {
    "hotels": "Recebidos/dados/hotels.jsonl",
    "room_types": "Recebidos/dados/room_types.jsonl",
    "daily_market": "Recebidos/dados/daily_market.jsonl",
    "weekly_performance": "Recebidos/dados/weekly_performance.jsonl",
    "rate_decisions": "Recebidos/dados/rate_decisions.jsonl",
    "reviews": "Recebidos/dados/reviews.jsonl",
    "review_scenarios": "Recebidos/dados/review_scenarios.jsonl"
}

print("=== CRIANDO O BANCO DE DADOS SQLITE PARA PORT ALDER ===\n")

for nome_tabela, caminho_arquivo in tabelas.items():
    if os.path.exists(caminho_arquivo):
        # Lê o arquivo JSONL
        df = pd.read_json(caminho_arquivo, lines=True)
        
        # Converte colunas que contêm listas ou dicionários para string JSON
        # (Isso evita o erro do SQLite de tipo 'list' não suportado)
        for coluna in df.columns:
            # Verifica se há algum elemento do tipo list ou dict na coluna
            if df[coluna].apply(lambda x: isinstance(x, (list, dict))).any():
                df[coluna] = df[coluna].apply(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)
        
        # Salva a tabela no SQLite
        df.to_sql(nome_tabela, conexao, if_exists='replace', index=False)
        
        print(f"✅ Tabela criada com sucesso: '{nome_tabela}' ({df.shape[0]} registros)")
    else:
        print(f"⚠️ Arquivo não encontrado para a tabela {nome_tabela}: {caminho_arquivo}")

# Fechando a conexão
conexao.close()

print(f"\n🎉 Banco de dados gerado com sucesso em: '{nome_banco}'!")