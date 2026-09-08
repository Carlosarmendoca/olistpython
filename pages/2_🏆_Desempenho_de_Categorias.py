import pandas as pd
import plotly.express as px
import streamlit as st

from views.vw_top_categorias import get_top_categorias


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(page_title="Desempenho das Categorias",layout="wide")


# ============================================================
# ESTILIZAÇÃO GLOBAL
# ============================================================

st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #1F2937 !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #6B7280 !important;
    }

    [data-testid="stMarkdownContainer"] h3 {
        font-size: 18px !important;
        font-weight: 600 !important;
        padding-bottom: 0px !important;
        margin-bottom: -15px !important;
    }

    [data-testid="stTable"],
    [data-testid="stDataFrame"] {
        font-size: 12px !important;
    }

    [data-testid="stMarkdownContainer"] h1 {
        font-size: 28px !important;
        padding-bottom: 0px !important;
        margin-bottom: -15px !important;
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


# ============================================================
# FUNÇÕES DE FORMATAÇÃO
# ============================================================

def formatar_moeda_card(valor):

    if valor >= 1_000_000:
        return f"R$ {valor / 1_000_000:.2f} mi"

    elif valor >= 1_000:
        return f"R$ {valor / 1_000:.1f} mil"

    else:
        texto = f"R$ {valor:,.2f}"

        return (
            texto
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )


def formatar_contagem(valor):

    return (
        f"{valor:,.0f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_barra(valor):

    if valor >= 1_000_000:
        return f"R$ {valor / 1_000_000:.1f} mi"

    elif valor >= 1_000:
        return f"R$ {valor / 1_000:.1f} mil"

    return f"R$ {valor:,.2f}"


def formatar_br(valor):

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_quantidade(valor):

    return (
        f"{valor:,.0f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

@st.cache_data
def carregar_dados():

    pedidos = pd.read_csv(
        "dados/pedidos_limpo.csv",
        parse_dates=[
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    )

    itens = pd.read_csv(
        "dados/itens_limpo.csv",
        parse_dates=["shipping_limit_date"]
    )

    produtos = pd.read_csv("dados/produtos_limpo.csv")

    clientes = pd.read_csv("dados/clientes_limpo.csv")

    return pedidos, itens, produtos, clientes


pedidos, itens, produtos, clientes = carregar_dados()


# ============================================================
# PREPARAÇÃO DA BASE ANALÍTICA
# ============================================================

df_categorias = get_top_categorias(
    pedidos,
    itens,
    produtos,
    clientes
)


# ============================================================
# CABEÇALHO
# ============================================================

st.title("📊 Desempenho de Categorias")

st.caption("Análise de receita, volume de vendas e ticket médio por categoria.")


# ============================================================
# FILTROS GLOBAIS
# ============================================================

anos_disponiveis = sorted(
    pedidos["order_purchase_timestamp"]
    .dt.year
    .dropna()
    .unique()
)

estados_disponiveis = sorted(
    clientes["customer_state"]
    .dropna()
    .unique()
)


with st.expander("⚙️ Abrir Filtros da Página",expanded=False):

    col_f1, col_f2 = st.columns(2)

    with col_f1:

        ano_selecionado = st.multiselect(
            "📅 Selecione o Ano",
            options=anos_disponiveis,
            default=anos_disponiveis
        )

    with col_f2:

        estado_selecionado = st.multiselect(
            "📍 Selecione o Estado",
            options=estados_disponiveis,
            default=estados_disponiveis
        )


# ============================================================
# APLICAÇÃO DOS FILTROS
# ============================================================

if ano_selecionado:
    df_categorias = df_categorias[df_categorias["ano"].isin(ano_selecionado)]


if estado_selecionado:
    df_categorias = df_categorias[df_categorias["customer_state"].isin(estado_selecionado)]


# ============================================================
# TRATAMENTO DE TEXTO
# ============================================================

df_categorias["product_category_name"] = (
    df_categorias["product_category_name"]
    .str.replace("_", " ")
    .str.title()
)


# ============================================================
# INDICADORES DE CATEGORIAS
# ============================================================

st.subheader("Indicadores de Categorias")

col1, col2, col3, col4 = st.columns(4)


# ============================================================
# CÁLCULO DOS KPIs
# ============================================================

receita_total = round(df_categorias["receita_total"].sum(),2)

total_pedidos = df_categorias["total_pedidos"].sum()

total_itens = df_categorias["total_itens"].sum()


if total_pedidos > 0:

    ticket_medio = round(receita_total / total_pedidos,2)
else:
    ticket_medio = 0

if total_itens > 0:

    # O preço médio do item considera receita total,
    # incluindo o frete, conforme a regra atual da página.
    preco_medio_item = round(receita_total / total_itens,2)

else:
    preco_medio_item = 0


# ============================================================
# EXIBIÇÃO DOS KPIs
# ============================================================

col1.metric("Faturamento Total", formatar_moeda_card(receita_total))

col2.metric("Ticket Médio por Pedido", formatar_moeda_card(ticket_medio))

col3.metric("Itens Vendidos", formatar_contagem(total_itens))

col4.metric("Preço Médio por Item", formatar_moeda_card(preco_medio_item))


st.divider()

# ============================================================
# TOP 10 CATEGORIAS POR FATURAMENTO
# ============================================================

st.subheader("Top 10 Categorias por Faturamento")


df_cat = (
    df_categorias
    .groupby("product_category_name")
    .agg(
        receita_produtos=("receita_produtos", "sum"),
        receita_total=("receita_total", "sum"),
        total_pedidos=("total_pedidos", "sum"),
        total_itens=("total_itens", "sum")
    )
    .reset_index()
    .sort_values(
        "receita_total",
        ascending=False
    ).head(10)
)


df_cat["ticket_medio"] = (df_cat["receita_total"] / df_cat["total_pedidos"]).round(2)


# O preço médio por item considera somente o valor dos produtos.
df_cat["preco_medio_item"] = (df_cat["receita_produtos"] / df_cat["total_itens"]).round(2)


df_cat["texto_faturamento"] = (df_cat["receita_total"].apply(formatar_barra))


fig_cat = px.bar(
    df_cat,
    x="receita_total",
    y="product_category_name",
    orientation="h",
    text="texto_faturamento",
    color_discrete_sequence=["#1F3B73"],
    hover_data=[
        "total_pedidos",
        "ticket_medio"
    ],
    labels={
        "receita_total": "Receita Total (R$)",
        "product_category_name": "Categoria"
    }
)


fig_cat.update_traces(
    textposition="outside",
    textfont_size=12,
    cliponaxis=False
)


fig_cat.update_layout(
    height=300,
    bargap=0.45,
    font=dict(size=12),
    xaxis=dict(
        title=None,
        showgrid=False,
        showticklabels=False
    ),
    yaxis=dict(
        title=None,
        categoryorder="total ascending"
    ),
    margin=dict(r=70, l=10, t=10, b=10)
)


st.plotly_chart(
    fig_cat,
    use_container_width=True
)

st.divider()

# ============================================================
# EVOLUÇÃO MENSAL DO TICKET MÉDIO
# ============================================================

st.subheader("Evolução Mensal do Ticket Médio")


df_ticket = (
    df_categorias
    .groupby(["data_mes", "ano"])
    .agg(
        receita_total=("receita_total", "sum"),
        total_pedidos=("total_pedidos", "sum")
    )
    .reset_index()
)


df_ticket["ticket_medio"] = (df_ticket["receita_total"] / df_ticket["total_pedidos"]).round(2)


df_ticket = df_ticket.sort_values(["ano", "data_mes"])


df_ticket["ticket_texto"] = (df_ticket["ticket_medio"].apply(formatar_br))


# Mantém somente os últimos 12 meses para preservar
# a leitura compacta da visualização.
df_ticket_12m = df_ticket.tail(12)


fig_ticket = px.line(
    df_ticket_12m,
    x="data_mes",
    y="ticket_medio",
    text="ticket_texto"
)


max_y_ticket = df_ticket_12m["ticket_medio"].max()

min_y_ticket = df_ticket_12m["ticket_medio"].min()

fig_ticket.update_traces(
    textposition="top center",
    cliponaxis=False,
    textfont=dict(size=10)
)

fig_ticket.update_layout(
    height=220,
    xaxis_tickangle=-45,
    xaxis_title=None,
    yaxis=dict(
        title=None,
        showgrid=False,
        showticklabels=False,
        range=[
            min_y_ticket * 0.98,
            max_y_ticket * 1.05
        ]
    ),
    margin=dict(r=20, l=10, t=0, b=10)
)


st.plotly_chart(fig_ticket,use_container_width=True)


st.divider()

# ============================================================
# RESUMO POR CATEGORIA
# ============================================================

st.subheader("Resumo por Categoria")

st.caption("Comparativo de faturamento, pedidos, itens e valores médios por categoria.")


df_tabela = (
    df_categorias
    .groupby("product_category_name")
    .agg(
        receita_produtos=("receita_produtos", "sum"),
        receita_total=("receita_total", "sum"),
        total_pedidos=("total_pedidos", "sum"),
        total_itens=("total_itens", "sum")
    )
    .reset_index()
    .sort_values(
        "receita_total",
        ascending=False
    )
)

df_tabela["ticket_medio"] = (df_tabela["receita_total"] / df_tabela["total_pedidos"]).round(2)

# O preço médio do item considera somente o valor dos produtos.
df_tabela["preco_medio_item"] = (df_tabela["receita_produtos"] / df_tabela["total_itens"]).round(2)

# O valor médio por item com frete considera produtos + frete.
df_tabela["valor_medio_item_com_frete"] = (df_tabela["receita_total"] / df_tabela["total_itens"]).round(2)


df_tabela_exibicao = (
    df_tabela
    .rename(
        columns={
            "product_category_name": "Categoria",
            "receita_total": "Faturamento",
            "total_pedidos": "Total de Pedidos",
            "total_itens": "Total de Itens",
            "ticket_medio": "Ticket Médio",
            "preco_medio_item": "Preço Médio por Item",
            "valor_medio_item_com_frete": "Valor Médio c/ Frete"
        }
    )
    .drop(
        columns=["receita_produtos"]
    )
)


# ============================================================
# ESTILIZAÇÃO DA TABELA
# ============================================================

df_tabela_estilo = (
    df_tabela_exibicao.style
    .background_gradient(
        subset=["Faturamento"],
        cmap="Blues"
    )
    .set_properties(
        **{
            "text-align": "right"
        }
    )
    .format(
        {
            "Faturamento": formatar_br,
            "Total de Pedidos": formatar_quantidade,
            "Total de Itens": formatar_quantidade,
            "Ticket Médio": formatar_br,
            "Preço Médio por Item": formatar_br,
            "Valor Médio c/ Frete": formatar_br
        }
    )
)


# ============================================================
# EXIBIÇÃO DA TABELA
# ============================================================

st.dataframe(
    df_tabela_estilo,
    use_container_width=True,
    height=550,
    hide_index=True
)


st.divider()