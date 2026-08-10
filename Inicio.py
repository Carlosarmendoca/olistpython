

import streamlit as st

# Configuração inicial da página (se já não tiver)
st.set_page_config(page_title="Olist Dashboard", page_icon="🛒", layout="wide")

# Título e Introdução
st.title("🛒 Análise de Comércio Eletrônico Olist")
st.write("A Olist conecta pequenas empresas a grandes canais de e-commerce no Brasil. Explore os dados de vendas, logística e perfil de clientes através deste dashboard interativo.")

st.divider() # Cria uma linha separadora sutil

st.header("Bem-vindo ao Dashboard de Análise de Vendas")
st.write("Navegue pelas páginas no menu lateral para explorar os dados:")

# Criando 3 colunas para os "Cartões"
col1, col2, col3 = st.columns(3)

with col1:
    st.info("**📊 Painel Executivo**\n\nVisão geral de receita, pedidos e logística.")

with col2:
    st.info("**🏆 Desempenho de Categorias**\n\nAnálise detalhada por categoria de produto.")

with col3:
    st.info("**👥 Análise de Clientes**\n\nDistribuição geográfica e evolução da base.")

# Rodapé informativo
st.success("Conjunto de dados público da Olist — e-commerce brasileiro (2016–2018)")