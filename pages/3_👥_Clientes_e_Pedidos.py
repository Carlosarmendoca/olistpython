import pandas as pd
import plotly.express as px
import streamlit as st
import sys
sys.path.append('.')

# Importando apenas a NOVA view unificada
from views.vw_clientes_regiao import get_vw_clientes_regiao

st.set_page_config(page_title="Análise de Clientes", layout="wide")

# ==========================================
# CARREGAMENTO DOS DADOS
# ==========================================
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

# Chamando a view unificada UMA única vez
df_view = get_vw_clientes_regiao(pedidos, clientes)

# Tratamento de Texto (Title Case para Cidades)
df_view['customer_city'] = df_view['customer_city'].str.title()

# Título
st.title("👥 Clientes e Pedidos")
st.caption("Distribuição geográfica de clientes, evolução da base e status dos pedidos.")

# ==========================================
# 🔍 FILTROS GLOBAIS - CLIENTES
# ==========================================
anos_disponiveis    = sorted(df_view['ano'].dropna().unique())
estados_disponiveis = sorted(df_view['customer_state'].dropna().unique())

with st.expander("⚙️ Abrir Filtros da Página", expanded=False):
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        ano_selecionado = st.multiselect("📅 Selecione o Ano", options=anos_disponiveis, default=anos_disponiveis)
    
    with col_f2:
        estado_selecionado = st.multiselect("📍 Selecione o Estado", options=estados_disponiveis, default=estados_disponiveis)

# Aplicação dos filtros em um único DataFrame
if ano_selecionado:
    df_view = df_view[df_view['ano'].isin(ano_selecionado)]

if estado_selecionado:
    df_view = df_view[df_view['customer_state'].isin(estado_selecionado)]

# ==========================================
# 1. KPIs (Topo) - Calculados da mesma view
# ==========================================
st.subheader("Indicadores Gerais")
col1, col2, col3, col4 = st.columns(4)

total_clientes   = df_view['total_clientes'].sum()
total_entregues  = df_view[df_view['status_pt'] == 'Entregue']['total_clientes'].sum()
total_cancelados = df_view[df_view['status_pt'] == 'Cancelado']['total_clientes'].sum()
total_faturados  = df_view[df_view['status_pt'] == 'Faturado']['total_clientes'].sum()

col1.metric("Total de Clientes",  f"{total_clientes:,.0f}".replace(',', '.'))
col2.metric("Clientes com Pedidos Entregues",  f"{total_entregues:,.0f}".replace(',', '.'))
col3.metric("Clientes com Pedidos Cancelados", f"{total_cancelados:,.0f}".replace(',', '.'))
col4.metric("Clientes com Pedidos Faturados",  f"{total_faturados:,.0f}".replace(',', '.'))

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 2. GRÁFICO AGRUPADO (Estados) COM RÓTULOS
# ==========================================
st.subheader("🗺️ Top 10 Estados por Clientes e Pedidos Entregues")

# Agrupa total de clientes
df_estado_clientes = df_view.groupby('customer_state')['total_clientes'].sum().reset_index()

# Agrupa apenas os entregues
df_estado_entregues = (df_view[df_view['status_pt'] == 'Entregue']
                       .groupby('customer_state')['total_clientes']
                       .sum().reset_index()
                       .rename(columns={'total_clientes': 'Pedidos Entregues'}))

# Junta os dois para o gráfico e pega o Top 10
df_estado_top = (df_estado_clientes
                 .merge(df_estado_entregues, on='customer_state', how='left')
                 .fillna(0) # Preenche com 0 estados sem entregas
                 .rename(columns={'total_clientes': 'Total de Clientes'})
                 .sort_values('Total de Clientes', ascending=False)
                 .head(10))

fig_estado = px.bar(
    df_estado_top,
    x='customer_state',
    y=['Pedidos Entregues', 'Total de Clientes'],
    barmode='group',
    text_auto='.3s',
    labels={'customer_state': 'Estado', 'value': 'Quantidade', 'variable': 'Métrica'},
    color_discrete_map={
        'Total de Clientes': '#1F3B73',
        'Pedidos Entregues': '#75A8D3'
    }
)
fig_estado.update_traces(textposition='outside')
fig_estado.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_estado, use_container_width=True)

st.markdown("---")

# ==========================================
# 3. GRÁFICO DE BARRAS (Cidades)
# ==========================================
st.subheader("Top 10 Cidades por Número de Clientes")

df_cidade_top = (df_view.groupby('customer_city')['total_clientes']
                        .sum().reset_index()
                        .sort_values('total_clientes', ascending=False)
                        .head(10))

fig_cidade = px.bar(
    df_cidade_top,
    x='customer_city',
    y='total_clientes',
    text_auto='.2s',
    color_discrete_sequence=['#1F3B73'],
    labels={'customer_city': 'Cidade', 'total_clientes': 'Total de Clientes'}
)
fig_cidade.update_traces(textposition='outside')
fig_cidade.update_layout(xaxis_tickangle=-45, margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_cidade, use_container_width=True)

st.markdown("---")

# ==========================================
# 4. GRÁFICO DE LINHAS (Evolução)
# ==========================================
st.subheader("Evolução Acumulada da Base de Clientes")

df_evolucao = (df_view.groupby(['ano', 'data_mes'])['total_clientes']
                      .sum().reset_index()
                      .sort_values(['ano', 'data_mes']))
df_evolucao['total_acumulado'] = df_evolucao['total_clientes'].cumsum()

fig_evolucao = px.line(
    df_evolucao,
    x='data_mes',
    y='total_acumulado',
    markers=True,
    text='total_acumulado',
    labels={'data_mes': 'Mês', 'total_acumulado': 'Clientes Acumulados'} 
)
fig_evolucao.update_traces(textposition='top center')
fig_evolucao.update_layout(xaxis_tickangle=-45, margin={"r":0,"t":10,"l":0,"b":0})
st.plotly_chart(fig_evolucao, use_container_width=True)

st.markdown("---")

# ==========================================
# 5. TABELA FINAL (Pedidos por Status)
# ==========================================
st.subheader("Clientes por Status dos Pedidos")
st.caption("Distribuição dos clientes entre os status de pedidos não entregues.")

# Filtra tudo que não é 'Entregue' e agrupa pelo status já traduzido
df_status_tab = (df_view[df_view['status_pt'] != 'Entregue']
                 .groupby('status_pt')['total_clientes']
                 .sum().reset_index()
                 .sort_values('total_clientes', ascending=False)
                 .rename(columns={'status_pt': 'Status', 'total_clientes': 'Total de Clientes'}))

# Adiciona a linha de Total Geral
total_row = pd.DataFrame([{'Status': 'Total Geral', 'Total de Clientes': df_status_tab['Total de Clientes'].sum()}])
df_exibir = pd.concat([df_status_tab, total_row], ignore_index=True)

# Exibe com o gradiente de cores
st.dataframe(
    df_exibir.style
    .background_gradient(subset=['Total de Clientes'], cmap='Blues')
    .format({'Total de Clientes': '{:,.0f}'}), 
    use_container_width=True, 
    hide_index=True
)