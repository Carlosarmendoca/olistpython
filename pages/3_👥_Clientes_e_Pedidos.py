import pandas as pd
import plotly.express as px
import streamlit as st
import sys
sys.path.append('.')

from views.vw_clientes_regiao import get_clientes_regiao
from views.vw_status_pedidos  import get_status_pedidos

st.set_page_config(page_title="Análise de Clientes", layout="wide")

# Carregando os dados
@st.cache_data
def carregar_dados():
    pedidos  = pd.read_csv("dados/pedidos_limpo.csv", parse_dates=[
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ])
    clientes = pd.read_csv("dados/clientes_limpo.csv")
    return pedidos, clientes

pedidos, clientes = carregar_dados()

# Chamando as views
df_clientes = get_clientes_regiao(pedidos, clientes)
df_status = get_status_pedidos(pedidos, clientes)

# ==========================================
# TRATAMENTO DE TEXTO (Title Case)
# ==========================================
# Transforma "sao paulo" em "Sao Paulo"
df_clientes['customer_city'] = df_clientes['customer_city'].str.title()

# Título
st.title("👥 Clientes e Pedidos")
st.caption("Distribuição geográfica de clientes, evolução da base e status dos pedidos.")

# ==========================================
# 🔍 FILTROS GLOBAIS - CLIENTES
# ==========================================
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
if ano_selecionado:
    df_clientes = df_clientes[df_clientes['ano'].isin(ano_selecionado)]
    df_status   = df_status[df_status['ano'].isin(ano_selecionado)] # <-- Adicionado

if estado_selecionado:
    df_clientes = df_clientes[df_clientes['customer_state'].isin(estado_selecionado)]
    df_status   = df_status[df_status['customer_state'].isin(estado_selecionado)] # <-- Adicionado

# ==========================================
# 1. KPIs (Topo)
# ==========================================
st.subheader("Indicadores Gerais")
col1, col2, col3, col4 = st.columns(4)

total_clientes   = df_clientes['total_clientes'].sum()
total_entregues  = df_status[df_status['status_pt'] == 'Entregue']['quantidade'].sum()
total_cancelados = df_status[df_status['status_pt'] == 'Cancelado']['quantidade'].sum()
total_faturados  = df_status[df_status['status_pt'] == 'Faturado']['quantidade'].sum()

col1.metric("Total de Clientes",  f"{total_clientes:,}")
col2.metric("Pedidos Entregues",  f"{total_entregues:,}")
col3.metric("Pedidos Cancelados", f"{total_cancelados:,}")
col4.metric("Pedidos Faturados",  f"{total_faturados:,}")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 2. GRÁFICO AGRUPADO (Estados) COM RÓTULOS
# ==========================================
st.subheader("🗺️ Top 10 Entregas e Clientes por Estado")

df_estado_clientes = (df_clientes.groupby('customer_state')
                                  .agg(total_clientes = ('total_clientes', 'sum'))
                                  .reset_index())

df_estado_entregues = (df_clientes[df_clientes['order_status'] == 'delivered']
                                   .groupby('customer_state')
                                   .agg(total_entregues = ('total_pedidos', 'sum'))
                                   .reset_index())

df_estado_top = (df_estado_clientes
                 .merge(df_estado_entregues, on='customer_state', how='left')
                 .sort_values('total_clientes', ascending=False)
                 .head(10))

df_estado_top = df_estado_top.rename(columns={
    'total_clientes': 'Total de Clientes',
    'total_entregues': 'Pedidos Entregues'
})

fig_estado = px.bar(
    df_estado_top,
    x='customer_state',
    y=['Pedidos Entregues', 'Total de Clientes'],
    barmode='group',
    text_auto='.3s', # Adiciona rótulos formatados (ex: 41k em vez de 41000)
    labels={'customer_state': 'Estado', 'value': 'Quantidade', 'variable': 'Métrica'},
    color_discrete_map={
        'Total de Clientes': '#1F3B73',
        'Pedidos Entregues': '#75A8D3'
    }
)
fig_estado.update_traces(textposition='outside') # Coloca o número acima da barra
fig_estado.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_estado, use_container_width=True)

st.markdown("---")

# ==========================================
# 3. GRÁFICO DE BARRAS (Cidades) COM RÓTULOS
# ==========================================
st.subheader("Top 10 Cidades por Número de Clientes")

df_cidade_top = (df_clientes.groupby('customer_city')
                              .agg(total_clientes = ('total_clientes', 'sum'))
                              .reset_index()
                              .sort_values('total_clientes', ascending=False)
                              .head(10))

fig_cidade = px.bar(
    df_cidade_top,
    x='customer_city',
    y='total_clientes',
    text_auto='.2s', # Rótulos formatados
    color_discrete_sequence=['#1F3B73'],
    labels={'customer_city': 'Cidade', 'total_clientes': 'Total de Clientes'}
)
fig_cidade.update_traces(textposition='outside') # Coloca o número acima da barra
fig_cidade.update_layout(
    xaxis_tickangle=-45, 
    margin={"r":0,"t":0,"l":0,"b":0}
)
st.plotly_chart(fig_cidade, use_container_width=True)

st.markdown("---")

# ==========================================
# 4. GRÁFICO DE LINHAS (Evolução)
# ==========================================
st.subheader("Evolução Acumulada da Base de Clientes")

df_evolucao = (df_clientes.groupby(['ano', 'data_mes'])
                           .agg(total_clientes = ('total_clientes', 'sum'))
                           .reset_index()
                           .sort_values(['ano', 'data_mes']))
df_evolucao['total_acumulado'] = df_evolucao['total_clientes'].cumsum()

fig_evolucao = px.line(
    df_evolucao,
    x='data_mes',
    y='total_acumulado',
    markers=True,
    text='total_acumulado', # Adiciona rótulos nos pontos da linha
    labels={
    'data_mes': 'Mês',
    'total_acumulado': 'Clientes Acumulados'
    } 
)
fig_evolucao.update_traces(textposition='top center') # Posiciona os números acima da linha
fig_evolucao.update_layout(
    xaxis_tickangle=-45,
    margin={"r":0,"t":10,"l":0,"b":0}
)
st.plotly_chart(fig_evolucao, use_container_width=True)

st.markdown("---")

# ==========================================
# 5. TABELA FINAL (Com Mapa de Calor)
# ==========================================
st.subheader("Pedidos por Status")
st.caption("Detalhamento dos pedidos não entregues.")

df_status_tab = (df_clientes[df_clientes['order_status'] != 'delivered']
                  .groupby('order_status')
                  .agg(total_clientes = ('total_clientes', 'sum'))
                  .reset_index()
                  .sort_values('total_clientes', ascending=False))

status_traducao = {
    'shipped':     'Em Transporte',
    'canceled':    'Cancelado',
    'unavailable': 'Indisponível',
    'invoiced':    'Faturado',
    'processing':  'Em Processamento',
    'created':     'Criado',
    'approved':    'Aprovado'
}

df_status_tab['status_pt'] = df_status_tab['order_status'].map(status_traducao)

df_exibir = df_status_tab[['status_pt', 'total_clientes']].rename(columns={
    'status_pt':     'Status',
    'total_clientes': 'Total de Clientes'
})

total_row = pd.DataFrame([{'Status': 'Total Geral', 'Total de Clientes': df_exibir['Total de Clientes'].sum()}])
df_exibir = pd.concat([df_exibir, total_row], ignore_index=True)

# Aplicando o gradiente de cores corporativo
st.dataframe(
    df_exibir.style
    .background_gradient(subset=['Total de Clientes'], cmap='Blues')
    .format({'Total de Clientes': '{:,}'}), # Garante a formatação com separador de milhar
    use_container_width=True, 
    hide_index=True
)