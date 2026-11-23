import sqlite3
import pandas as pd

# Conectando ao banco SQLite que acabamos de criar
conexao = sqlite3.connect("banco/port_alder.db")

print("=== ETAPA 3: CONSULTAS DE NEGÓCIO NO SQLITE ===\n")

# 1. Ranking dos hotéis por receita total em cada ano (usando weekly_performance ou daily_market)
query_receita = """
    SELECT 
        SUBSTR(week_start, 1, 4) AS ano,
        hotel_name,
        SUM(total_revenue) AS receita_total
    FROM weekly_performance
    GROUP BY ano, hotel_name
    ORDER BY ano DESC, receita_total DESC;
"""
df_receita = pd.read_sql_query(query_receita, conexao)
print("--- 1. Top Hotéis por Receita Total (por Ano) ---")
print(df_receita.head(10)) # Mostrando os 10 primeiros
print("\n" + "-"*60 + "\n")

# 2. Hotéis com mais de 30% de avaliações com 1 ou 2 estrelas
query_ruins = """
    SELECT 
        h.name AS hotel_name,
        COUNT(r.review_id) AS total_reviews,
        SUM(CASE WHEN r.rating <= 2 THEN 1 ELSE 0 END) AS reviews_ruins,
        ROUND((CAST(SUM(CASE WHEN r.rating <= 2 THEN 1 ELSE 0 END) AS REAL) / COUNT(r.review_id)) * 100, 2) AS pct_ruins
    FROM reviews r
    JOIN hotels h ON r.hotel_id = h.hotel_id
    GROUP BY h.name
    HAVING pct_ruins > 30
    ORDER BY pct_ruins DESC;
"""
df_ruins = pd.read_sql_query(query_ruins, conexao)
print("--- 2. Hotéis com mais de 30% de avaliações ruins (1 ou 2 estrelas) ---")
print(df_ruins)

# Fechando a conexão
conexao.close()