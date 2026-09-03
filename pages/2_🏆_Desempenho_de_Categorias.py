import pandas as pd
import plotly.express as px
import streamlit as st

# O import do sys foi removido para manter o código limpo. 
# (Se der erro de módulo não encontrado ao rodar, basta voltar com o import sys e sys.path.append('.'))
from views.vw_top_categorias import get_top_categorias

st.set_page_config(page_title="Desempenho das Categorias", layout="wide")

# ==========================================
# CARREGAMENTO DE DADOS
# ==========================================
@st.cache_data
def carregar_dados():
    pedidos  = pd.read_csv("dados/pedidos_limpo.csv", parse_dates=[
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ])
    itens    = pd.read_csv("dados/itens_limpo.csv", parse_dates=['shipping_limit_date'])
    produtos = pd.read_csv("dados/produtos_limpo.csv")
    clientes = pd.read_csv("dados/clientes_limpo.csv") 
    
    return pedidos, itens, produtos, clientes

pedidos, itens, produtos, clientes = carregar_dados()

df_categorias = get_top_categorias(pedidos, itens, produtos, clientes)


# ==========================================
# CABEÇALHO
# ==========================================
st.title("📊 Desempenho de Categorias")
st.caption("Análise de receita, volume de vendas e ticket médio por categoria.")


# ==========================================
# 1. FILTROS GLOBAIS
# ==========================================
anos_disponiveis    = sorted(pedidos['order_purchase_timestamp'].dt.year.dropna().unique())
estados_disponiveis = sorted(clientes['customer_state'].dropna().unique())

with st.expander("⚙️ Abrir Filtros da Página", expanded=False):
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        ano_selecionado = st.multiselect("📅 Selecione o Ano", options=anos_disponiveis, default=anos_disponiveis)
    
    with col_f2:
        estado_selecionado = st.multiselect("📍 Selecione o Estado", options=estados_disponiveis, default=estados_disponiveis)

# APLICAÇÃO DOS FILTROS
if ano_selecionado:
    df_categorias = df_categorias[df_categorias['ano'].isin(ano_selecionado)]

if estado_selecionado:
    df_categorias = df_categorias[df_categorias['customer_state'].isin(estado_selecionado)]

st.divider()


# ==========================================
# TRATAMENTO DE TEXTO GERAL
# ==========================================
df_categorias['product_category_name'] = df_categorias['product_category_name'].str.replace('_', ' ').str.title()

st.subheader("Indicadores de Categorias")


# ==========================================
# 2. KPIs (Topo)
# ==========================================

col1, col2, col3, col4 = st.columns(4)

receita_total = round(df_categorias['receita_total'].sum(), 2)
total_pedidos = df_categorias['total_pedidos'].sum()
total_itens = df_categorias['total_itens'].sum()

# Proteção contra divisão por zero
if total_pedidos > 0:
    ticket_medio = round(receita_total / total_pedidos, 2)
else:
    ticket_medio = 0

if total_itens > 0:
    # CORREÇÃO: Usando a receita_total (com frete) em vez de apenas produtos
    preco_medio_item = round(receita_total / total_itens, 2)
else:
    preco_medio_item = 0

# ------------------------------------------
# Formatação dos Cards
# ------------------------------------------
def formatar_moeda_card(valor):
    if valor >= 1_000_000:
        # Usa o PONTO (ex: 15.42 milhões) 
        return f"R$ {valor / 1_000_000:.2f} mi"
        
    elif valor >= 1_000:
        # Usa o PONTO (ex: 15.4 mil)
        return f"R$ {valor / 1_000:.1f} mil"
        
    else:
        # Usa a VÍRGULA e padrão BR para valores inteiros (ex: R$ 158,52)
        texto = f"R$ {valor:,.2f}"
        return texto.replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_contagem(valor):
    return f"{valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Exibição
col1.metric("Faturamento Total", formatar_moeda_card(receita_total))
col2.metric("Ticket Médio por Pedido", formatar_moeda_card(ticket_medio))
col3.metric("Itens Vendidos", formatar_contagem(total_itens))
col4.metric("Preço Médio por Item", formatar_moeda_card(preco_medio_item))

st.divider()

# ==========================================
# 3. GRÁFICO DE BARRAS (Top Categorias)
# ==========================================
st.subheader("Top 10 Categorias por Faturamento")

df_cat = (df_categorias.groupby('product_category_name')
                       .agg(
                           receita_produtos = ('receita_produtos', 'sum'),
                           receita_total    = ('receita_total', 'sum'),
                           total_pedidos    = ('total_pedidos', 'sum'),
                           total_itens      = ('total_itens', 'sum')
                       )
                       .reset_index()
                       .sort_values('receita_total', ascending=False)
                       .head(10))

df_cat['ticket_medio'] = (df_cat['receita_total'] / df_cat['total_pedidos']).round(2)
df_cat['preco_medio_item'] = (df_cat['receita_produtos'] / df_cat['total_itens']).round(2)

fig_cat = px.bar(
    df_cat,
    x='receita_total',
    y='product_category_name',
    orientation='h',
    text_auto='.2s', 
    color_discrete_sequence=['#1F3B73'], 
    hover_data=['total_pedidos', 'ticket_medio'],
    labels={'receita_total': 'Receita Total (R$)', 'product_category_name': 'Categoria'}
)

# Limpeza e Ajuste Executivo
fig_cat.update_traces(
    textposition='outside',
    cliponaxis=False
) 
fig_cat.update_layout(
    xaxis=dict(title=None, showgrid=False, showticklabels=False),
    yaxis=dict(title=None, categoryorder='total ascending'),
    margin=dict(r=40, l=10, t=10, b=10)
)
st.plotly_chart(fig_cat, use_container_width=True)

st.divider()


# ==========================================
# 4. GRÁFICO DE LINHAS (Evolução Ticket)
# ==========================================
st.subheader("Evolução Mensal do Ticket Médio por Pedido")

df_ticket = (df_categorias.groupby(['data_mes', 'ano'])
                           .agg(
                               receita_total = ('receita_total', 'sum'),
                               total_pedidos = ('total_pedidos', 'sum')
                           )
                           .reset_index())

df_ticket['ticket_medio'] = (df_ticket['receita_total'] / df_ticket['total_pedidos']).round(2)
df_ticket = df_ticket.sort_values(['ano', 'data_mes'])

# Criando coluna de texto formatada para o padrão BR no gráfico
df_ticket['ticket_texto'] = df_ticket['ticket_medio'].apply(
    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)

fig_ticket = px.line(
    df_ticket,
    x='data_mes',
    y='ticket_medio',
    markers=True,
    text='ticket_texto', # Rótulo formatado no padrão Brasil
    labels={'data_mes': 'Mês', 'ticket_medio': 'Ticket Médio (R$)'}
)

# Limpeza e Ajuste Executivo
max_y_ticket = df_ticket['ticket_medio'].max()

fig_ticket.update_traces(
    textposition='top center',
    cliponaxis=False
)
fig_ticket.update_layout(
    xaxis_tickangle=-45,
    xaxis_title=None,
    yaxis=dict(
        title=None, 
        showgrid=False, 
        showticklabels=False,
        range=[0, max_y_ticket * 1.15]
    ),
    margin=dict(r=20, l=10, t=30, b=10)
)
st.plotly_chart(fig_ticket, use_container_width=True)

st.divider()


# ==========================================
# 5. TABELA DE DADOS
# ==========================================
st.subheader("Resumo por Categoria")
st.caption("Comparativo de faturamento, pedidos, itens e valores médios por categoria.")

df_tabela = (
    df_categorias
    .groupby('product_category_name')
    .agg(
        receita_produtos=('receita_produtos', 'sum'),
        receita_total=('receita_total', 'sum'),
        total_pedidos=('total_pedidos', 'sum'),
        total_itens=('total_itens', 'sum')
    )
    .reset_index()
    .sort_values('receita_total', ascending=False)
)

df_tabela['ticket_medio'] = (df_tabela['receita_total'] / df_tabela['total_pedidos']).round(2)
df_tabela['preco_medio_item'] = (df_tabela['receita_produtos'] / df_tabela['total_itens']).round(2)
df_tabela['valor_medio_item_com_frete'] = (df_tabela['receita_total'] / df_tabela['total_itens']).round(2)

df_tabela_exibicao = df_tabela.rename(columns={
    'product_category_name': 'Categoria',
    'receita_total': 'Faturamento',
    'total_pedidos': 'Total de Pedidos',
    'total_itens': 'Total de Itens',
    'ticket_medio': 'Ticket Médio',
    'preco_medio_item': 'Preço Médio por Item',
    'valor_medio_item_com_frete': 'Valor Médio por Item com Frete'
})

df_tabela_exibicao = df_tabela_exibicao.drop(columns=['receita_produtos'])

# ------------------------------------------
# Funções de Formatação Padrão Brasil (Tabela)
# ------------------------------------------
def formata_br(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formata_qtd(valor):
    return f"{valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ------------------------------------------
# Estilização
# ------------------------------------------
df_tabela_estilo = (
    df_tabela_exibicao.style
    .background_gradient(subset=['Faturamento', 'Total de Pedidos', 'Total de Itens'], cmap='Blues')
    .format({
        'Faturamento': formata_br,
        'Total de Pedidos': formata_qtd,
        'Total de Itens': formata_qtd,
        'Ticket Médio': formata_br,
        'Preço Médio por Item': formata_br,
        'Valor Médio por Item com Frete': formata_br
    })
)

st.dataframe(
    df_tabela_estilo,
    use_container_width=True,
    height=550,
    hide_index=True
)
st.divider()