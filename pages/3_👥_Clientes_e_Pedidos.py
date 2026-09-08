import pandas as pd
import plotly.express as px
import streamlit as st
import textwrap

from views.vw_clientes_regiao import get_vw_clientes_regiao


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Análise de Clientes",
    layout="wide"
)


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

def formatar_contagem(valor):

    if valor >= 1_000_000:
        return f"{valor / 1_000_000:.2f} mi"

    elif valor >= 1_000:
        return f"{valor / 1_000:.3f} mil"

    else:
        return (
            f"{valor:,.0f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )


def formata_qtd_barra(valor):

    if valor >= 1_000_000:
        return f"{valor / 1_000_000:.1f} mi"

    elif valor >= 1_000:
        return f"{valor / 1_000:.1f} mil"

    return (
        f"{valor:,.0f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formata_qtd(valor):

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

    clientes = pd.read_csv(
        "dados/clientes_limpo.csv"
    )

    return pedidos, clientes


pedidos, clientes = carregar_dados()


# ============================================================
# PREPARAÇÃO DA BASE ANALÍTICA
# ============================================================

df_view = get_vw_clientes_regiao(pedidos, clientes)
df_view["customer_city"] = (df_view["customer_city"].str.title())


# ============================================================
# CABEÇALHO
# ============================================================

st.title("👥 Clientes e Pedidos")

st.caption("Distribuição geográfica de clientes, evolução da base e status dos pedidos.")


# ============================================================
# FILTROS GLOBAIS
# ============================================================

anos_disponiveis = sorted(
    df_view["ano"]
    .dropna()
    .unique()
)

estados_disponiveis = sorted(
    df_view["customer_state"]
    .dropna()
    .unique()
)


with st.expander("⚙️ Abrir Filtros da Página", expanded=False):

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
    df_view = df_view[df_view["ano"].isin(ano_selecionado)]


if estado_selecionado:
    df_view = df_view[df_view["customer_state"].isin(estado_selecionado)]


# ============================================================
# BASE ÚNICA DE CLIENTES + PEDIDOS
# ============================================================

# Relaciona pedidos ao customer_unique_id para permitir a
# identificação correta de clientes únicos, mesmo quando o
# mesmo cliente possui múltiplos pedidos.
#
# customer_id identifica o registro do cliente em um pedido,
# enquanto customer_unique_id representa o cliente consolidado.

df_clientes_base = (
    pedidos
    .merge(
        clientes[
            [
                "customer_id",
                "customer_unique_id",
                "customer_city",
                "customer_state"
            ]
        ],
        on="customer_id",
        how="left"
    )
    .dropna(
        subset=["customer_unique_id"]
    )
)


# ============================================================
# INDICADORES GERAIS
# ============================================================

st.write("")
st.write("")

st.subheader("Indicadores Gerais")

col1, col2, col3, col4 = st.columns(4)


df_clientes_kpi = df_clientes_base.copy()


# ============================================================
# FILTROS DOS KPIs
# ============================================================

if ano_selecionado:

    df_clientes_kpi = df_clientes_kpi[
        df_clientes_kpi[
            "order_purchase_timestamp"
        ]
        .dt.year
        .isin(ano_selecionado)
    ]


if estado_selecionado:

    df_clientes_kpi = df_clientes_kpi[
        df_clientes_kpi[
            "customer_state"
        ].isin(estado_selecionado)
    ]


# ============================================================
# CÁLCULO DOS CLIENTES ÚNICOS
# ============================================================

total_clientes = (
    df_clientes_kpi[
        "customer_unique_id"
    ]
    .nunique()
)


total_entregues = (
    df_clientes_kpi[
        df_clientes_kpi["order_status"] == "delivered"
    ]["customer_unique_id"]
    .nunique()
)


total_cancelados = (
    df_clientes_kpi[
        df_clientes_kpi["order_status"] == "canceled"
    ]["customer_unique_id"]
    .nunique()
)


total_faturados = (
    df_clientes_kpi[
        df_clientes_kpi["order_status"] == "invoiced"
    ]["customer_unique_id"]
    .nunique()
)


# ============================================================
# EXIBIÇÃO DOS KPIs
# ============================================================

col1.metric("Total de Clientes", formatar_contagem(total_clientes))

col2.metric("Clientes com Pedidos Entregues", formatar_contagem(total_entregues))

col3.metric("Clientes com Pedidos Cancelados", formatar_contagem(total_cancelados))

col4.metric("Clientes com Pedidos Faturados", formatar_contagem(total_faturados))


st.write("")
st.write("")

st.divider()

# ============================================================
# GRÁFICOS — ESTADOS E CIDADES
# ============================================================

col_estado, col_cidade = st.columns(2)


# ============================================================
# TOP 10 ESTADOS POR CLIENTES
# ============================================================

with col_estado:

    st.subheader("Top 10 Estados por Clientes com Pedidos Entregues")

    df_estado_clientes = df_clientes_base.copy()

    if ano_selecionado:

        df_estado_clientes = df_estado_clientes[
            df_estado_clientes[
                "order_purchase_timestamp"
            ]
            .dt.year
            .isin(ano_selecionado)
        ]

    if estado_selecionado:

        df_estado_clientes = df_estado_clientes[
            df_estado_clientes[
                "customer_state"
            ].isin(estado_selecionado)
        ]


    df_estado_total = (
        df_estado_clientes
        .groupby("customer_state")[
            "customer_unique_id"
        ]
        .nunique()
        .reset_index(
            name="Total de Clientes"
        )
    )

    df_estado_entregues = (
        df_estado_clientes[
            df_estado_clientes["order_status"] == "delivered"
        ]
        .groupby("customer_state")[
            "customer_unique_id"
        ]
        .nunique()
        .reset_index(
            name="Clientes com Pedidos Entregues"
        )
    )


    df_estado_top = (
        df_estado_total
        .merge(
            df_estado_entregues,
            on="customer_state",
            how="left"
        )
        .fillna(0)
        .sort_values(
            "Total de Clientes",
            ascending=False
        )
        .head(10)
    )


    df_estado_melt = df_estado_top.melt(
        id_vars="customer_state",
        value_vars=[
            "Total de Clientes",
            "Clientes com Pedidos Entregues"
        ],
        var_name="Métrica",
        value_name="Quantidade"
    )


    df_estado_melt["Texto"] = (
        df_estado_melt["Quantidade"]
        .apply(
            lambda x:
            f"{x:,.0f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    )


    fig_estado = px.bar(
        df_estado_melt,
        x="customer_state",
        y="Quantidade",
        color="Métrica",
        text="Texto",
        barmode="group",
        labels={
            "customer_state": "Estado",
            "Quantidade": "Quantidade de Clientes",
            "Métrica": "Métrica"
        },
        color_discrete_map={
            "Total de Clientes": "#1F3B73",
            "Clientes com Pedidos Entregues": "#75A8D3"
        }
    )


    fig_estado.update_traces(
        textposition="outside",
        textfont_size=10,
        textangle=-90,
        cliponaxis=False
    )


    max_y_estado = (df_estado_top["Total de Clientes"].max())


    fig_estado.update_layout(
        uniformtext_minsize=12,
        uniformtext_mode="show",
        height=450,
        xaxis_title=None,
        yaxis=dict(
            title=None,
            showgrid=False,
            showticklabels=False,
            range=[0, max_y_estado * 1.40]
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5,
            title_text=""
        ),
        margin=dict(l=10, r=10, t=70, b=90)
    )


    fig_estado.update_xaxes(
        automargin=False
    )

    fig_estado.update_yaxes(
        automargin=False
    )


    st.plotly_chart(
        fig_estado,
        use_container_width=True
    )

    st.divider()


# ============================================================
# TOP 10 CIDADES POR CLIENTES
# ============================================================

with col_cidade:

    st.subheader("Top 10 Cidades por Número de Clientes")

    df_cidade_clientes = df_clientes_base.copy()

    if ano_selecionado:

        df_cidade_clientes = df_cidade_clientes[
            df_cidade_clientes[
                "order_purchase_timestamp"
            ]
            .dt.year
            .isin(ano_selecionado)
        ]

    if estado_selecionado:

        df_cidade_clientes = df_cidade_clientes[
            df_cidade_clientes[
                "customer_state"
            ].isin(estado_selecionado)
        ]

    df_cidade_top = (
        df_cidade_clientes
        .groupby("customer_city")[
            "customer_unique_id"
        ]
        .nunique()
        .reset_index(
            name="Total de Clientes"
        )
        .sort_values(
            "Total de Clientes",
            ascending=False
        )
        .head(10)
    )

    df_cidade_top["customer_city"] = (
        df_cidade_top["customer_city"]
        .str.title()
        .apply(
            lambda x:
            "<br>".join(
                textwrap.wrap(
                    x,
                    width=12
                )
            )
        )
    )


    df_cidade_top["Texto"] = (
        df_cidade_top["Total de Clientes"]
        .apply(
            lambda x:
            f"{x:,.0f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    )


    fig_cidade = px.bar(
        df_cidade_top,
        x="customer_city",
        y="Total de Clientes",
        text="Texto",
        labels={
            "customer_city": "Cidade",
            "Total de Clientes": "Total de Clientes"
        },
        color_discrete_sequence=["#1F3B73"]
    )


    fig_cidade.update_traces(
        textposition="outside",
        cliponaxis=False
    )


    max_y_cidade = (df_cidade_top["Total de Clientes"].max())


    fig_cidade.update_layout(
        height=450,
        xaxis=dict(
            title=None,
            tickangle=-45,
            type="category",
            tickfont=dict(size=9)
        ),
        yaxis=dict(
            title=None,
            showgrid=False,
            showticklabels=False,
            range=[0, max_y_cidade * 1.25]
        ),
        margin=dict(l=10, r=10, t=70, b=90)
    )


    fig_cidade.update_xaxes(
        automargin=False
    )

    fig_cidade.update_yaxes(
        automargin=False
    )


    st.plotly_chart(
        fig_cidade,
        use_container_width=True
    )


    st.divider()


# ============================================================
# EVOLUÇÃO ACUMULADA DA BASE DE CLIENTES
# ============================================================

st.subheader("Evolução Acumulada da Base de Clientes")

st.caption("Crescimento acumulado de clientes únicos nos últimos 12 meses do período selecionado.")


df_clientes_evolucao = df_clientes_base.copy()


if ano_selecionado:

    df_clientes_evolucao = df_clientes_evolucao[
        df_clientes_evolucao[
            "order_purchase_timestamp"
        ]
        .dt.year
        .isin(ano_selecionado)
    ]


if estado_selecionado:

    df_clientes_evolucao = df_clientes_evolucao[
        df_clientes_evolucao[
            "customer_state"
        ].isin(estado_selecionado)
    ]


if not df_clientes_evolucao.empty:

    # Primeiro identifica a data do primeiro pedido de cada cliente.
    # Depois contabiliza os novos clientes por mês e calcula o
    # crescimento acumulado da base.

    df_primeiro_pedido = (
        df_clientes_evolucao
        .groupby("customer_unique_id",as_index=False)["order_purchase_timestamp"].min()
    )


    df_primeiro_pedido["data_mes"] = (
        df_primeiro_pedido[
            "order_purchase_timestamp"
        ]
        .dt.to_period("M")
        .astype(str)
    )


    df_evolucao = (
        df_primeiro_pedido
        .groupby("data_mes")
        .size()
        .reset_index(
            name="novos_clientes"
        )
        .sort_values("data_mes")
    )


    df_evolucao["total_acumulado"] = (df_evolucao["novos_clientes"].cumsum())


    df_evolucao["Texto"] = (df_evolucao["total_acumulado"].apply(formata_qtd_barra))


    # Mantém os 20 meses atualmente utilizados pela visualização.
    df_evolucao_12m = (df_evolucao.tail(20))


    fig_evolucao = px.line(
        df_evolucao_12m,
        x="data_mes",
        y="total_acumulado",
        markers=True,
        text="Texto",
        labels={
            "data_mes": "Mês",
            "total_acumulado": "Clientes Acumulados"
        }
    )


    fig_evolucao.update_traces(
        textposition="top center",
        cliponaxis=False,
        textfont=dict(size=9)
    )


    max_y_evolucao = (df_evolucao_12m["total_acumulado"].max())

    min_y_evolucao = (df_evolucao_12m["total_acumulado"].min())


    fig_evolucao.update_layout(
        height=280,
        xaxis_tickangle=-45,
        xaxis_title=None,
        yaxis=dict(
            title=None,
            showgrid=False,
            showticklabels=False,
            range=[
                min_y_evolucao * 0.90,
                max_y_evolucao * 1.15
            ]
        ),
        margin={"r": 20, "t": 30, "l": 10, "b": 10}
    )


    st.plotly_chart(fig_evolucao, use_container_width=True)


else:
    st.warning("Não há histórico de clientes para os filtros selecionados.")

st.divider()


# ============================================================
# CLIENTES POR STATUS DOS PEDIDOS
# ============================================================

st.subheader(
    "Clientes por Status dos Pedidos"
)

st.caption(
    "Quantidade de clientes únicos associados a cada status de pedido."
)


df_clientes_status = df_clientes_base.copy()


if ano_selecionado:

    df_clientes_status = df_clientes_status[
        df_clientes_status[
            "order_purchase_timestamp"
        ]
        .dt.year
        .isin(ano_selecionado)
    ]


if estado_selecionado:

    df_clientes_status = df_clientes_status[
        df_clientes_status[
            "customer_state"
        ].isin(estado_selecionado)]


status_traducao = {
    "delivered": "Entregue",
    "shipped": "Em Transporte",
    "canceled": "Cancelado",
    "unavailable": "Indisponível",
    "invoiced": "Faturado",
    "processing": "Em Processamento",
    "created": "Criado",
    "approved": "Aprovado"
}


df_clientes_status["status_pt"] = (
    df_clientes_status["order_status"]
    .map(status_traducao)
    .fillna("Outros")
)


df_status_tab = (
    df_clientes_status
    .groupby("status_pt")[
        "customer_unique_id"
    ]
    .nunique()
    .reset_index(
        name="Total de Clientes"
    )
    .sort_values(
        "Total de Clientes",
        ascending=False
    )
    .rename(
        columns={
            "status_pt": "Status"
        }
    )
)


# Cada status é calculado utilizando clientes únicos.
# Um mesmo cliente pode aparecer em mais de um status caso
# tenha realizado pedidos com situações diferentes.

total_row = pd.DataFrame(
    [
        {
            "Status": "Total Geral",
            "Total de Clientes": (
                df_clientes_status[
                    "customer_unique_id"
                ].nunique()
            )
        }
    ]
)


df_exibir = pd.concat(
    [
        df_status_tab,
        total_row
    ],ignore_index=True
)


# ============================================================
# EXIBIÇÃO DA TABELA
# ============================================================

st.dataframe(
    df_exibir.style
    .background_gradient(
        subset=["Total de Clientes"],
        cmap="Blues"
    )
    .format(
        {
            "Total de Clientes":
                formata_qtd
        }
    ),
    use_container_width=True,
    hide_index=True
)


st.divider()