import streamlit as st

st.set_page_config(
    page_title="Olist Analytics",
    page_icon="🛒",
    layout="wide"
)

# --- INJEÇÃO DE CSS PARA O INÍCIO / LANDING PAGE ---
st.markdown(
    """
    <style>
    [data-testid="stMarkdownContainer"] h1 {
        font-size: 32px !important;
        font-weight: 700 !important;
        color: #1F2937 !important;
        padding-bottom: 0px !important;
        margin-bottom: -10px !important;
    }
    [data-testid="stMarkdownContainer"] h3 {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #374151 !important;
        padding-bottom: 5px !important;
    }
    /* Estilização suave para os cards de navegação */
    div[data-testid="stAlert"] {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        color: #1E293B !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }
    div[data-testid="stAlert"] p {
        font-size: 13px !important;
        line-height: 1.5 !important;
    }
    [data-testid="stSidebar"] {
        min-width: 220px !important;
        max-width: 220px !important;
        width: 220px !important;
    }

    [data-testid="stSidebarNavLink"] span {
    font-size: 12px !important;
    font-weight: 500 !important;
    }
    </style>

    """,
    unsafe_allow_html=True,
)

# Header
st.title("🛒 Olist Analytics")
st.caption("Análise executiva de vendas, categorias, clientes e logística do e-commerce brasileiro.")

st.write("")
st.write("")

st.subheader("📌 Explore as Visões do Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        "**📊 Painel Executivo**\n\n"
        "Acompanhe os principais indicadores (KPIs) de faturamento, volume de pedidos, "
        "ticket médio e a saúde das operações em alto nível."
    )

with col2:
    st.info(
        "**🏆 Desempenho de Categorias**\n\n"
        "Explore a receita gerada por segmento, os produtos líderes de vendas, "
        "o ticket médio das categorias e a concentração de mercado."
    )

with col3:
    st.info(
        "**👥 Clientes e Pedidos**\n\n"
        "Entenda a distribuição geográfica da sua base, a expansão acumulada ao "
        "longo do tempo e o funil de status de entregas dos pedidos."
    )

st.divider()

st.subheader("ℹ️ Sobre a Base de Dados")

st.write(
    "Este dashboard analisa o conjunto de dados público da **Olist**, "
    "uma empresa brasileira de tecnologia voltada ao ecossistema de e-commerce. "
    "A base reúne dados de pedidos realizados entre **2016 e 2018**, "
    "permitindo analisar diferentes etapas da jornada de compra, desde o pedido "
    "até a entrega logística ao cliente."
)

st.caption("Olist Analytics • Visual Identity & Data Standard v2.0")