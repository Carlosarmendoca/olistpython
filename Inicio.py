

import streamlit as st

st.set_page_config(
    page_title="Olist Analytics",
    page_icon="🛒",
    layout="wide"
)

# Título
st.title("🛒 Olist Analytics")

st.markdown(
    "Análise de vendas, categorias, clientes e logística "
    "do e-commerce brasileiro através de dados públicos da Olist."
)

st.divider()

st.subheader("Explore o dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        "**📊 Painel Executivo**\n\n"
        "Visão geral de receita, pedidos, ticket médio, "
        "distribuição geográfica e logística."
    )

with col2:
    st.info(
        "**🏆 Desempenho das Categorias**\n\n"
        "Analise receita, volume de vendas, ticket médio "
        "e desempenho das principais categorias."
    )

with col3:
    st.info(
        "**👥 Clientes e Pedidos**\n\n"
        "Explore a distribuição dos clientes, "
        "evolução da base e status dos pedidos."
    )

st.divider()

st.subheader("Sobre os dados")

st.write(
    "Conjunto de dados público da Olist, contendo informações "
    "sobre pedidos, clientes, produtos, pagamentos e logística "
    "do e-commerce brasileiro no período de 2016 a 2018."
)

st.caption("Olist Analytics • Dashboard de Data Analytics")