import pandas as pd
import plotly.express as px
import streamlit as st
import sys
sys.path.append('.')

from views.vw_top_categorias import get_top_categorias

st.set_page_config(page_title="Desempenho das Categorias", layout="wide")

# Carregando os dados
@st.cache_data
def carregar_dados():
    pedidos  = pd.read_csv("dados/pedidos_limpo.csv", parse_dates=[
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ])
    itens    = pd.read_csv("dados/itens_limpo.csv", parse_dates=['shipping_limit_date'])
    produtos = pd.read_csv("dados/produtos_limpo.csv")
    
    # NOVO: Carregando a tabela de clientes!
    clientes = pd.read_csv("dados/clientes_limpo.csv") 
    
    return pedidos, itens, produtos, clientes

# NOVO: Recebendo a variável clientes aqui no desempacotamento
pedidos, itens, produtos, clientes = carregar_dados()

# Chamando a view (agora a variável 'clientes' existe e tem os dados!)
df_categorias = get_top_categorias(pedidos, itens, produtos, clientes)


# Título
st.title("📊 Desempenho de Categorias") #📊 
st.caption("Análise de receita, volume de vendas e ticket médio por categoria.")

#st.markdown("---")

# ==========================================
# 🔍 FILTROS GLOBAIS - CATEGORIAS
# ==========================================
# Pegando as opções únicas direto das tabelas base
anos_disponiveis    = sorted(pedidos['order_purchase_timestamp'].dt.year.dropna().unique())
estados_disponiveis = sorted(clientes['customer_state'].dropna().unique())

with st.expander("⚙️ Abrir Filtros da Página", expanded=False):
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        ano_selecionado = st.multiselect("📅 Selecione o Ano", options=anos_disponiveis, default=anos_disponiveis)
    
    with col_f2:
        estado_selecionado = st.multiselect("📍 Selecione o Estado", options=estados_disponiveis, default=estados_disponiveis)

# ==========================================
# 🚀 APLICAÇÃO DOS FILTROS
# ==========================================
# Se a lista de anos selecionados não estiver vazia, aplica o filtro
if ano_selecionado:
    df_categorias = df_categorias[df_categorias['ano'].isin(ano_selecionado)]

# Se a lista de estados selecionados não estiver vazia, aplica o filtro
if estado_selecionado:
    df_categorias = df_categorias[df_categorias['customer_state'].isin(estado_selecionado)]

st.markdown("---")
# A partir daqui, seguem os seus gráficos e KPIs de Categorias...



# ==========================================
# TRATAMENTO DE TEXTO (Title Case)
# ==========================================
# Troca '_' por espaço e coloca a primeira letra em maiúscula (ex: cama_mesa_banho -> Cama Mesa Banho)
df_categorias['product_category_name'] = df_categorias['product_category_name'].str.replace('_', ' ').str.title()

st.subheader("Indicadores de Categorias")

# ==========================================
# 1. KPIs (Topo)
# ==========================================
col1, col2, col3, col4 = st.columns(4)

receita_total = round(df_categorias['receita_total'].sum(), 2)
total_pedidos = df_categorias['total_pedidos'].sum()
total_itens   = df_categorias['total_itens'].sum()
receita_produtos = df_categorias['receita_produtos'].sum()

# Proteção contra divisão por zero
if total_pedidos > 0:
    ticket_medio = round(receita_total / total_pedidos, 2)
else:
    ticket_medio = 0

if total_itens > 0:
    preco_medio_item = round(receita_produtos / total_itens, 2)
else:
    preco_medio_item = 0

col1.metric("Faturamento Total",        f"R$ {receita_total:,.2f}")
col2.metric("Ticket Médio por Pedido",         f"R$ {ticket_medio:,.2f}")
col3.metric("Itens Vendidos",       f"{total_itens:,}")
col4.metric("Preço Médio por Item", f"R$ {preco_medio_item:,.2f}")

st.markdown("<br>", unsafe_allow_html=True) # Espaçamento extra

# ==========================================
# 2. GRÁFICO DE BARRAS COM RÓTULOS
# ==========================================
st.subheader("Top 10 Categorias por Faturamento") #🏆

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
    text_auto='.2s', # Adiciona os rótulos de dados resumidos
    color_discrete_sequence=['#1F3B73'], # Minimalismo Premium: Cor sólida corporativa
    hover_data=['total_pedidos', 'ticket_medio'],
    labels={'receita_total': 'Receita Total (R$)', 'product_category_name': 'Categoria'}
)
fig_cat.update_traces(textposition='outside') # Posiciona o texto logo após a barra
fig_cat.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    margin={"r":0,"t":0,"l":0,"b":0}
)
st.plotly_chart(fig_cat, use_container_width=True)

st.markdown("---")

# ==========================================
# 3. GRÁFICO DE LINHAS COM RÓTULOS
# ==========================================
st.subheader("Evolução Mensal do Ticket Médio por Pedido") #📈 

df_ticket = (df_categorias.groupby(['data_mes', 'ano'])
                           .agg(
                               receita_total = ('receita_total', 'sum'),
                               total_pedidos = ('total_pedidos', 'sum')
                           )
                           .reset_index())
df_ticket['ticket_medio'] = (df_ticket['receita_total'] / df_ticket['total_pedidos']).round(2)
df_ticket = df_ticket.sort_values(['ano', 'data_mes'])

fig_ticket = px.line(
    df_ticket,
    x='data_mes',
    y='ticket_medio',
    markers=True,
    text='ticket_medio', # Adiciona os rótulos de dados na linha
    labels={'data_mes': 'Mês', 'ticket_medio': 'Ticket Médio (R$)'}
)
fig_ticket.update_traces(textposition='top center') # Posiciona o texto acima do marcador
fig_ticket.update_layout(
    xaxis_tickangle=-45,
    margin={"r":0,"t":10,"l":0,"b":0}
)
st.plotly_chart(fig_ticket, use_container_width=True)

st.markdown("---")

# ==========================================
# 4. TABELA DE DADOS
# ==========================================
# Tabela com mapa de calor
st.subheader("Resumo por Categoria")#📋 

df_tabela = (df_categorias.groupby('product_category_name')
             .agg(
                 receita_produtos = ('receita_produtos', 'sum'),
                 receita_total    = ('receita_total', 'sum'),
                 total_pedidos    = ('total_pedidos', 'sum'),
                 total_itens      = ('total_itens', 'sum'),
             )
             .reset_index()
             .sort_values('receita_total', ascending=False))

df_tabela['ticket_medio'] = (df_tabela['receita_total'] / df_tabela['total_pedidos']).round(2)

df_tabela['preco_medio_item'] = (
    df_tabela['receita_produtos'] / df_tabela['total_itens']
).round(2)

df_tabela['valor_medio_item_com_frete'] = (
    df_tabela['receita_total'] / df_tabela['total_itens']
).round(2)

# ==========================================
# NOVO: Renomeando as colunas para o usuário
# ==========================================
df_tabela_exibicao = df_tabela.rename(columns={
    'product_category_name': 'Categoria',
    'receita_total': 'Faturamento',
    'total_pedidos': 'Total de Pedidos',
    'total_itens': 'Total de Itens',
    'ticket_medio': 'Ticket Médio',
    'preco_medio_item': 'Preço Médio por Item',
    'valor_medio_item_com_frete': 'Valor Médio por Item com Frete'
})

# Removendo receita_produtos da tabela exibida
df_tabela_exibicao = df_tabela_exibicao.drop(columns=['receita_produtos'])

# ==========================================
# FORMATAÇÃO VISUAL DA TABELA
# ==========================================
st.dataframe(
    df_tabela_exibicao.style
    .background_gradient(
        subset=['Faturamento'],
        cmap='Blues'
    )
    .background_gradient(
        subset=['Total de Pedidos'],
        cmap='Blues'
    )
    .background_gradient(
        subset=['Ticket Médio'],
        cmap='Blues'
    )
    .format({
        'Faturamento': 'R$ {:,.2f}',
        'Total de Pedidos': '{:,.0f}',
        'Total de Itens': '{:,.0f}',
        'Preço Médio por Item': 'R$ {:,.2f}',
        'Valor Médio por Item com Frete': 'R$ {:,.2f}',
        'Ticket Médio': 'R$ {:,.2f}'
    }),
    use_container_width=True,
    height=500
)