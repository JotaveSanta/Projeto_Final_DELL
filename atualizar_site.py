import sqlite3
import pandas as pd
import json

# 1. Conecta ao seu banco real e puxa os dados dos hotéis
conn = sqlite3.connect("banco/port_alder.db")
df = pd.read_sql_query("SELECT * FROM weekly_performance", conn)
conn.close()

# Garante que a ocupação esteja na escala 0-100%
if df['occupancy'].max() <= 1.0:
    df['occupancy'] = df['occupancy'] * 100

total_rev = float(df['total_revenue'].sum())
city_occ = float(df['occupancy'].mean())
city_adr = float(df['adr'].mean())

# 2. Agrupa os dados por Tier (Categorias reais do banco)
tiers_unique = list(df['tier'].unique())
palette = ['#38bdf8', '#2dd4bf', '#a78bfa', '#f59e0b']
tiers_list = []
tier_map = {}

for idx, t_name in enumerate(tiers_unique):
    sub = df[df['tier'] == t_name]
    tier_map[t_name] = idx
    tiers_list.append({
        'n': str(t_name).capitalize(),
        'c': palette[idx % len(palette)],
        'share': round(float(sub['total_revenue'].sum() / total_rev), 4),
        'occ': round(float(sub['occupancy'].mean()), 1),
        'adr': round(float(sub['adr'].mean()), 2)
    })

# 3. Agrupa os dados reais de cada um dos 14 hotéis
hotels_df = df.groupby(['hotel_name', 'tier']).agg(
    occ=('occupancy', 'mean'),
    adr=('adr', 'mean'),
    rev=('total_revenue', 'sum')
).reset_index()

hotels_list = []
for _, row in hotels_df.iterrows():
    item = {
        'n': row['hotel_name'],
        't': tier_map[row['tier']],
        'occ': round(float(row['occ']), 1),
        'adr': round(float(row['adr']), 2)
    }
    if 'Marisol' in row['hotel_name']:
        item['hi'] = 'good'
    elif 'Northgate' in row['hotel_name']:
        item['hi'] = 'bad'
    hotels_list.append(item)

# 4. Lê o seu HTML (ajuste o nome se você salvou como index_2.html ou index.html)
arquivo_entrada = "index_2.html" # mude para "index.html" se já renomeou
with open(arquivo_entrada, "r", encoding="utf-8") as f:
    html = f.read()

# Remove as tarjas amarelas de "Valores ilustrativos"
html = html.replace('<span class="note">Valores ilustrativos: substitua pelos dados reais no objeto DATA, no início do script.</span>', '')
html = html.replace('<span class="note">Pontos ilustrativos, exceto as médias da cidade.</span>', '')

# Atualiza o texto do resumo de Tiers caso existam 2 ou mais categorias
if len(tiers_list) >= 2:
    tiers_sorted = sorted(tiers_list, key=lambda x: x['adr'], reverse=True)
    L, E = tiers_sorted[0], tiers_sorted[-1]
    html = html.replace(
        "const [L, E] = DATA.tiers;",
        f"const L = {json.dumps(L, ensure_ascii=False)}, E = {json.dumps(E, ensure_ascii=False)};"
    )
    html = html.replace(
        "`O luxo cobra ${fmt(L.adr / E.adr, 1).replace(',', ',')} vezes a diária do econômico e ainda ocupa ${fmt(L.occ - E.occ, 1)} pontos percentuais a mais.`",
        "`A categoria ${L.n} cobra ${fmt(L.adr / E.adr, 1)} vezes a diária da ${E.n} e mantém ${fmt(L.occ, 1)}% de ocupação média.`"
    )

# Monta o novo bloco DATA 100% real
novo_data = f"""const DATA = {{
    total: {round(total_rev, 2)},
    tiers: {json.dumps(tiers_list, ensure_ascii=False)},
    hotels: {json.dumps(hotels_list, ensure_ascii=False)},
    cityOcc: {round(city_occ, 1)}, cityAdr: {round(city_adr, 2)},"""

inicio = html.index("const DATA = {")
fim = html.index("probs: [")
html_final = html[:inicio] + novo_data + "\n    " + html[fim:]

# Salva como index.html pronto para publicação
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_final)

print("✅ Sucesso! O arquivo index.html foi gerado com todos os dados reais do seu banco!")