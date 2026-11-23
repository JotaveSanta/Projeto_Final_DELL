import pandas as pd

# Carregando o cadastro de hotéis
df_hotels = pd.read_json("Recebidos/dados/hotels.jsonl", lines=True)

print("=== INSPEÇÃO DA COLUNA AMENITIES (Comodidades) ===")
# Mostra as primeiras linhas da coluna amenities para entender o formato
print(df_hotels[['name', 'tier', 'amenities']].head(3))

# Descobrindo quais são todas as comodidades únicas existentes nos hotéis de Port Alder
# Como 'amenities' é uma lista, usamos .explode() para separar cada item em uma linha nova
df_explodido = df_hotels.explode('amenities')

print("\n=== TODAS AS COMODIDADES ÚNICAS ENCONTRADAS ===")
print(df_explodido['amenities'].unique())

print("\n=== QUANTOS HOTÉIS TÊM CADA COMODIDADE? ===")
print(df_explodido['amenities'].value_counts())