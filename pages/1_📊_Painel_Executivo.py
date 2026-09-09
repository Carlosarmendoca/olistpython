import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

from views.vw_receita_mensal import get_receita_mensal
from views.vw_top_categorias import get_top_categorias
from views.vw_receita_por_estado import get_receita_por_estado


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config( page_title="Painel Executivo", layout="wide")

# ============================================================
# ESTILIZAÇÃO GLOBAL
# ============================================================

# Ajusta tamanhos de fonte e dimensões dos componentes para
# manter uma apresentação compacta e adequada ao dashboard.
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
    """Formata valores monetários para exibição nos KPIs."""

    # Formato compacto para valores grandes, evitando números
    # extensos nos cards de indicador (ex: R$ 1,50 mi em vez
    # de R$ 1.500.000,00).
    if valor >= 1_000_000:
        return f"R$ {valor / 1_000_000:.2f} mi"

    if valor >= 1_000:
        return f"R$ {valor / 1_000:.1f} mil"

    texto = f"R$ {valor:,.2f}"

    # Python formata número com vírgula de milhar e ponto decimal
    # (padrão americano). Troca-se "," por "X" temporariamente
    # para não confundir os símbolos ao inverter para o padrão
    # brasileiro (ponto de milhar, vírgula decimal).
    return (
        texto
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_contagem(valor):
    """Formata quantidades inteiras no padrão brasileiro."""

    texto = f"{valor:,.0f}"

    # Mesma troca temporária por "X" explicada em formatar_moeda_card,
    # aqui aplicada a números inteiros (sem casas decimais).
    return (
        texto
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_quantidade_compacta(valor):
    """Formata quantidades para rótulos compactos dos gráficos."""

    # Mantém os rótulos curtos dentro dos gráficos, já que números
    # completos poluiriam a visualização (ex: barras e linhas).
    if valor >= 1_000_000:
        return f"{valor / 1_000_000:.1f} mi"

    if valor >= 1_000:
        return f"{valor / 1_000:.1f} mil"

    return (
        f"{valor:,.0f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_receita_compacta(valor):
    """Formata valores de receita para rótulos dos gráficos."""

    # Mesma lógica de formatar_quantidade_compacta, mas com o
    # prefixo "R$" para valores monetários exibidos em gráficos.
    if valor >= 1_000_000:
        return f"R$ {valor / 1_000_000:.1f} mi"

    if valor >= 1_000:
        return f"R$ {valor / 1_000:.1f} mil"

    return (
        f"R$ {valor:,.0f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_br(valor):
    """Formata valores monetários no padrão brasileiro."""

    # Trata valores ausentes (NaN) que podem aparecer em células
    # de tabela sem dado correspondente, evitando exibir "R$ nan".
    if pd.isna(valor):
        return "-"

    return (
        f"R$ {valor:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def formatar_pct(valor):
    """Formata percentuais no padrão brasileiro."""

    # Ex: linhas do MoM sem mês anterior para comparação
    # (primeiro mês da série) resultam em NaN.
    if pd.isna(valor):
        return "-"

    # Percentual não precisa da troca de "," por "X" porque não
    # existe separador de milhar em valores dessa faixa — só a
    # vírgula decimal precisa ser ajustada.
    return f"{valor:.2f}%".replace(".", ",")

# ============================================================
# CARREGAMENTO DOS DADOS
# ============================================================

# O cache evita a releitura dos arquivos CSV a cada rerun
# provocado por filtros ou interações com o dashboard.
@st.cache_data
def carregar_dados():

    # As colunas de data já vêm como texto no CSV, então
    # parse_dates converte para datetime na leitura, evitando
    # ter que fazer essa conversão depois em cada página.
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

    clientes = pd.read_csv("dados/clientes_limpo.csv")

    itens = pd.read_csv("dados/itens_limpo.csv", parse_dates=["shipping_limit_date"])

    pagamentos = pd.read_csv("dados/pagamentos_limpo.csv")

    produtos = pd.read_csv("dados/produtos_limpo.csv")

    # Retorna todas as bases de uma vez, já que as páginas
    # precisam relacioná-las entre si (merge/groupby) para
    # montar as views analíticas.
    return (
        pedidos,
        clientes,
        itens,
        pagamentos,
        produtos
    )

pedidos, clientes, itens, pagamentos, produtos = carregar_dados()
# ============================================================
# PREPARAÇÃO DAS BASES ANALÍTICAS
# ============================================================

# As views concentram as regras de transformação e agregação.
# A página utiliza essas bases para construir os indicadores
# e gráficos sem duplicar regras de negócio na interface.
df_estado = get_receita_por_estado(pedidos, clientes, pagamentos)

df_receita = get_receita_mensal(pedidos, pagamentos, clientes)

df_categorias = get_top_categorias(pedidos, itens, produtos, clientes)

# ============================================================
# CABEÇALHO
# ============================================================

st.title("🛒 Painel Executivo de Vendas")

st.caption("Visão geral de receita, pedidos, desempenho regional e logística.")


# ============================================================
# 1. FILTRO GLOBAL DE TEMPO
# ============================================================

# dropna() remove eventuais datas ausentes antes de extrair os
# anos, evitando um valor "NaN" aparecer como opção de filtro.
anos_disponiveis = sorted(pedidos["order_purchase_timestamp"].dt.year.dropna().unique())

# O expander mantém os filtros escondidos por padrão, deixando
# os indicadores e gráficos visíveis assim que a página carrega.
with st.expander("⚙️ Abrir Filtros da Página", expanded=False):

    ano_selecionado = st.multiselect("📅 Selecione o Ano", options=anos_disponiveis, default=anos_disponiveis)


# Aplica o filtro temporal às três bases analíticas.
# O "if" evita erro caso o usuário desmarque todos os anos:
# sem filtro aplicado, os dataframes originais são mantidos
# em vez de retornar vazios.
if ano_selecionado:

    df_estado = df_estado[df_estado["ano"].isin(ano_selecionado)]

    df_receita = df_receita[df_receita["ano"].isin(ano_selecionado)]

    df_categorias = df_categorias[df_categorias["ano"].isin(ano_selecionado)]


# ============================================================
# 2. SELEÇÃO DE ESTADO NO MAPA
# ============================================================

estado_selecionado_mapa = None

# O Plotly armazena a seleção no session_state.
# Como o Streamlit executa a página novamente após a interação,
# a seleção precisa ser recuperada antes da construção dos KPIs.
if "meu_mapa_interativo" in st.session_state:

    selecao = st.session_state["meu_mapa_interativo"].get("selection", {})

    # "points" só existe quando o usuário efetivamente clicou
    # em algum estado do mapa; sem clique, a seleção vem vazia.
    if selecao and selecao.get("points"):

        estado_selecionado_mapa = (selecao["points"][0]["location"])


# ============================================================
# 3. KPIs
# ============================================================

# Cria a base utilizada pelos indicadores.
# Com estado selecionado, representa somente aquele estado.
# Sem seleção, representa o Brasil inteiro.
if estado_selecionado_mapa:

    df_kpi = df_estado[df_estado["customer_state"] == estado_selecionado_mapa]

else:

    df_kpi = df_estado


st.write("")
st.write("")

st.subheader("Indicadores Gerais")

col1, col2, col3, col4 = st.columns(4)

# ------------------------------------------------------------
# Cálculo dos indicadores
# ------------------------------------------------------------

receita_total = df_kpi["receita_total"].sum()

total_pedidos = df_kpi["total_pedidos"].sum()


# Evita divisão por zero quando o filtro (ano ou estado) não
# retorna nenhum pedido.
if total_pedidos > 0:

    ticket_medio = (receita_total / total_pedidos)

    # soma_dias_total já vem pré-calculada na view como a soma
    # dos dias de entrega de todos os pedidos, permitindo obter
    # a média sem reprocessar os dados brutos aqui na página.
    prazo_medio = (df_kpi["soma_dias_total"].sum() / df_kpi["total_pedidos"].sum())

else:
    ticket_medio = 0
    prazo_medio = 0


# ------------------------------------------------------------
# Exibição dos indicadores
# ------------------------------------------------------------

col1.metric("Faturamento Total", formatar_moeda_card(receita_total))

col2.metric("Total de Pedidos", formatar_contagem(total_pedidos))

col3.metric("Ticket Médio", formatar_moeda_card(ticket_medio))

texto_prazo = (f"{prazo_medio:.1f} dias".replace(".", ","))

col4.metric("Prazo Médio de Entrega", texto_prazo)

st.write("")

st.divider()

# ============================================================
# 4. MAPA DO BRASIL
# ============================================================

st.subheader("Faturamento por Estado")

st.caption("Clique em um estado para filtrar os indicadores e análises abaixo.")

# O mapa utiliza a base filtrada apenas pelo ano.
# df_kpi não é utilizado porque pode estar restrito a um estado.
# Assim, todos os estados permanecem disponíveis para seleção.
df_mapa = (
    df_estado
    .groupby("customer_state")
    .agg(receita_total=("receita_total", "sum"),total_pedidos=("total_pedidos", "sum")
    )
    .reset_index()
)

df_mapa["ticket_medio"] = (df_mapa["receita_total"] / df_mapa["total_pedidos"]).round(2)


# O geojson traz os contornos geográficos dos estados brasileiros,
# necessários para o Plotly desenhar o mapa (a base de dados em si
# só tem a sigla do estado, sem coordenadas).
fig_mapa = px.choropleth(
    df_mapa,
    geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
    locations="customer_state",
    featureidkey="properties.sigla",
    color="receita_total",
    hover_data=["total_pedidos", "ticket_medio"],
    color_continuous_scale="Blues",
    labels={
        "customer_state": "Estado",
        "receita_total": "Receita Total",
        "total_pedidos": "Total de Pedidos",
        "ticket_medio": "Ticket Médio"
    }
)

# fitbounds ajusta o zoom para enquadrar só o território
# brasileiro; visible=False remove países vizinhos do fundo.
fig_mapa.update_geos(fitbounds="locations", visible=False)

fig_mapa.update_layout(margin={"r": 0, "t": 10, "l": 0, "b": 10})


# A key identifica o gráfico no session_state e permite
# recuperar a seleção após o rerun provocado pelo clique.
st.plotly_chart(
    fig_mapa,
    use_container_width=True,
    on_select="rerun",
    key="meu_mapa_interativo"
)

# ============================================================
# 5. CROSS-FILTERING
# ============================================================

# A seleção do mapa também restringe as análises abaixo,
# permitindo navegar da visão nacional para um estado específico.
if estado_selecionado_mapa:

    st.info(
        f"📍 Estado selecionado: **{estado_selecionado_mapa}**. "
        "Clique novamente no estado para retornar à visão nacional.")

    df_categorias = df_categorias[df_categorias["customer_state"] == estado_selecionado_mapa]

    df_receita = df_receita[df_receita["customer_state"] == estado_selecionado_mapa]

st.divider()

# ============================================================
# 6. TOP 10 CATEGORIAS POR PEDIDOS
# ============================================================

st.subheader("Top 10 Categorias por Pedidos")


# Consolida as categorias e mantém somente as dez com
# maior quantidade de pedidos para facilitar a comparação.
df_cat = (
    df_categorias
    .groupby("product_category_name")
    .agg(
        receita_total=("receita_total", "sum"),
        total_pedidos=("total_pedidos", "sum"),
        total_itens=("total_itens", "sum")
    )
    .reset_index()
    .sort_values("total_pedidos", ascending=False).head(10)
)


# df_cat pode ficar vazio quando o cross-filtering do mapa
# seleciona um estado sem pedidos de categoria registrados;
# o "if" evita erro de divisão por zero nos cálculos abaixo.
if not df_cat.empty:

    df_cat["ticket_medio"] = (df_cat["receita_total"] / df_cat["total_pedidos"]).round(2)

    df_cat["preco_medio_item"] = (df_cat["receita_total"] / df_cat["total_itens"]).round(2)

    # Categorias vêm do dataset original em snake_case
    # (ex: "moveis_decoracao"); aqui viram texto legível
    # para exibição ("Moveis Decoracao").
    df_cat["product_category_name"] = (
        df_cat["product_category_name"].str.replace("_", " ").str.title()
    )

    df_cat["texto_pedidos"] = (df_cat["total_pedidos"].apply(formatar_quantidade_compacta))

    fig_cat = px.bar(
        df_cat,
        x="total_pedidos",
        y="product_category_name",
        orientation="h",
        text="texto_pedidos",
        color_discrete_sequence=["#1F3B73"],
        hover_data=[
            "total_pedidos",
            "ticket_medio"
        ],
        labels={
            "total_pedidos": "Total de Pedidos",
            "product_category_name": "Categoria"
        }
    )

    fig_cat.update_traces(
        textposition="outside",
        textfont_size=12,
        cliponaxis=False)

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
            # "total ascending" ordena as barras pelo valor,
            # deixando a maior categoria no topo do gráfico.
            title=None,
            categoryorder="total ascending"
        ),
        margin=dict(r=70, l=10, t=10, b=10)
    )

    st.plotly_chart(fig_cat, use_container_width=True)

else:

    st.warning("Não há dados de categorias para o estado selecionado.")

st.divider()

# ============================================================
# 7. EVOLUÇÃO MENSAL DO FATURAMENTO
# ============================================================

st.subheader("📈 Evolução Mensal do Faturamento")


if not df_receita.empty:

    df_linha = (
        df_receita
        .groupby(
            ["ano", "mes", "ano_mes"]
        ).agg(receita_total=("receita_total", "sum")
        )
        .reset_index()
        .sort_values(["ano", "mes"])
    )

    df_linha["texto_receita"] = (df_linha["receita_total"].apply(formatar_receita_compacta))

    # Limita a visualização aos últimos 12 meses para manter
    # os rótulos legíveis e evitar excesso de informação.
    df_linha_12m = df_linha.tail(12)


    fig_receita = px.line(
        df_linha_12m,
        x="ano_mes",
        y="receita_total",
        markers=True,
        text="texto_receita",
        labels={
            "ano_mes": "Mês",
            "receita_total": "Receita Total (R$)"
        }
    )

    fig_receita.update_traces(
        textposition="top center",
        textfont=dict(size=10),
        cliponaxis=False
    )

    max_y = df_linha_12m["receita_total"].max()

    min_y = df_linha_12m["receita_total"].min()


    # O range do eixo Y usa uma margem (95%/110%) em vez de
    # começar em zero, para que as variações entre os meses
    # fiquem mais visíveis na linha do gráfico.
    fig_receita.update_layout(
        height=220,
        xaxis_tickangle=-45,
        xaxis_title=None,
        yaxis=dict(
            title=None,
            showgrid=False,
            showticklabels=False,
            range=[
                min_y * 0.95,
                max_y * 1.10
            ]
        ),
        margin=dict(r=20, l=10, t=0, b=10)
    )


    st.plotly_chart(fig_receita, use_container_width=True)

else:

    st.warning("Não há dados de receita para o estado selecionado.")

st.divider()

# ============================================================
# 8. ANÁLISE MoM — MONTH OVER MONTH
# ============================================================

st.subheader("📊 Variação Mensal da Receita (MoM)")

st.caption(
    "Compara a receita de cada mês com o mês calendário imediatamente anterior."
)


# MoM compara a receita de cada mês com o mês calendário anterior.
#
# Para um estado selecionado, a view já disponibiliza a receita
# anterior e a variação calculada.
#
# Na visão nacional, a receita precisa ser consolidada por mês
# antes de calcular a variação.
if estado_selecionado_mapa:

    df_mom = (
        df_receita[
            [
                "ano",
                "mes",
                "mes_nome",
                "ano_mes",
                "receita_total",
                "receita_mes_anterior",
                "variacao_mom_pct"
            ]
        ].copy().sort_values(["ano", "mes"])
    )

else:
    df_mom = (
        df_receita
        .groupby(
            ["ano", "mes", "mes_nome", "ano_mes"],
            as_index=False
        ).agg(receita_total=("receita_total", "sum"))
        .sort_values(["ano", "mes"])
    )

    # Na visão nacional, calcula a receita do mês anterior
    # após a consolidação mensal.
    df_mom["receita_mes_anterior"] = (df_mom["receita_total"].shift(1))

    # np.where evita divisão por zero quando não há receita
    # no mês anterior (ex: primeiro mês da série ou mês sem
    # nenhum pedido registrado).

    df_mom["variacao_mom_pct"] = np.where(df_mom["receita_mes_anterior"] > 0,
        ((df_mom["receita_total"] - df_mom["receita_mes_anterior"]) 
         / df_mom["receita_mes_anterior"] * 100), np.nan).round(2)

    # Limita variações superiores a 1000% para evitar que
    # bases de comparação muito pequenas distorçam a leitura.

    df_mom.loc[df_mom["variacao_mom_pct"] > 1000, "variacao_mom_pct"] = np.nan

# ============================================================
# PREPARAÇÃO DA TABELA MoM
# ============================================================

df_mom["Mês"] = (df_mom["mes_nome"] + "/" + df_mom["ano"].astype(str))

df_mom_tabela = (
    df_mom[
        [
            "Mês",
            "receita_total",
            "receita_mes_anterior",
            "variacao_mom_pct"
        ]
    ]
    .rename(
        columns={
            "receita_total": "Receita",
            "receita_mes_anterior": "Receita Mês Anterior",
            "variacao_mom_pct": "MoM (%)"
        }
    )
)


# Identifica o contexto utilizado na análise, já que a mesma
# tabela é usada tanto para o Brasil quanto para um estado
# específico selecionado no mapa.

if estado_selecionado_mapa:

    st.caption(f"📍 Análise MoM do estado **{estado_selecionado_mapa}**")

else:

    st.caption("🌎 Análise MoM do Brasil")


# ============================================================
# FORMATAÇÃO DA TABELA MoM
# ============================================================

# A formatação ocorre somente na camada de apresentação,
# preservando os dados numéricos originais.
df_tabela_estilo = (
    df_mom_tabela
    .style
    .set_properties(**{"text-align": "right"}
    ).format(
        {
            "Receita": formatar_br,
            "Receita Mês Anterior": formatar_br,
            "MoM (%)": formatar_pct
        }
    )
)

# ============================================================
# EXIBIÇÃO DA TABELA
# ============================================================

st.dataframe(
    df_tabela_estilo,
    use_container_width=True,
    hide_index=True
)

st.divider()