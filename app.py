import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

# Configuração da página do dashboard
st.set_page_config(
    page_title="Dashboard Port Alder",
    page_icon="🏨",
    layout="wide"
)

st.title("🏨 Inteligência de Receita — Hotéis de Port Alder")
st.markdown("Painel gerencial interativo para análise de ocupação, receitas e desempenho dos hotéis.")

# Verificando se o banco de dados existe antes de carregar
caminho_banco = "banco/port_alder.db"
if not os.path.exists(caminho_banco):
    st.error(f"⚠️ O banco de dados não foi encontrado no caminho: `{caminho_banco}`. Verifique se a pasta `banco` existe na raiz do projeto.")
else:
    # Conectando ao banco SQLite para puxar os dados
    @st.cache_data
    def carregar_dados():
        conexao = sqlite3.connect(caminho_banco)
        df = pd.read_sql_query("SELECT * FROM weekly_performance", conexao)
        conexao.close()
        return df

    df = carregar_dados()

    if df.empty:
        st.warning("⚠️ A tabela de dados está vazia.")
    else:
        # --- BARRA LATERAL (Filtros) ---
        st.sidebar.header("Filtros do Painel")
        tier_selecionado = st.sidebar.selectbox(
            "Selecione a Categoria (Tier):",
            options=["Todos"] + list(df['tier'].unique())
        )

        # Aplicando o filtro na base de dados
        df_filtrado = df if tier_selecionado == "Todos" else df[df['tier'] == tier_selecionado]

        # --- SEÇÃO DE KPIs (Indicadores Principais) ---
        st.subheader("📊 Indicadores Chave de Desempenho (KPIs)")

        col1, col2, col3 = st.columns(3)
        receita_total = df_filtrado['total_revenue'].sum()
        ocupacao_media = df_filtrado['occupancy'].mean() * 100
        diaria_media = df_filtrado['adr'].mean()

        col1.metric("Receita Consolidada", f"R$ {receita_total:,.2f}")
        col2.metric("Ocupação Média", f"{ocupacao_media:.1f}%")
        col3.metric("Diária Média (ADR)", f"R$ {diaria_media:.2f}")

        st.markdown("---")

        # --- GRÁFICOS ---
        st.subheader("📈 Análise Gráfica")

        receita_por_hotel = df_filtrado.groupby('hotel_name')['total_revenue'].sum().reset_index()
        fig_bar = px.bar(
            receita_por_hotel,
            x='total_revenue',
            y='hotel_name',
            orientation='h',
            title="Receita Total por Hotel",
            labels={'total_revenue': 'Receita (R$)', 'hotel_name': 'Hotel'}
        )
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})

        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")
        st.markdown("*⚠️ Nota: Dataset sintético desenvolvido para fins educacionais (Port Alder).*")