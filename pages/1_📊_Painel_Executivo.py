import pandas as pd
import plotly.express as px
import streamlit as st

import numpy as np


from views.vw_receita_mensal     import get_receita_mensal
from views.vw_top_categorias     import get_top_categorias
from views.vw_receita_por_estado import get_receita_por_estado

st.set_page_config(page_title="Painel Executivo", layout="wide")

# Carregando os dados
@st.cache_data
def carregar_dados():
    pedidos    = pd.read_csv("dados/pedidos_limpo.csv", parse_dates=[
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ])
    clientes   = pd.read_csv("dados/clientes_limpo.csv")
    itens      = pd.read_csv("dados/itens_limpo.csv", parse_dates=['shipping_limit_date'])
    pagamentos = pd.read_csv("dados/pagamentos_limpo.csv")
    produtos   = pd.read_csv("dados/produtos_limpo.csv")
    return pedidos, clientes, itens, pagamentos, produtos

pedidos, clientes, itens, pagamentos, produtos = carregar_dados()

# Chamando as views
df_estado     = get_receita_por_estado(pedidos, clientes, pagamentos)
df_receita    = get_receita_mensal(pedidos, pagamentos, clientes)
df_categorias = get_top_categorias(pedidos, itens, produtos, clientes)

# Título
# st.title("🛒 Painel Executivo de Vendas")
# st.markdown("---")
st.title("🛒 Painel Executivo de Vendas")
st.caption("Visão geral de receita, pedidos, desempenho regional e logística.")

# ==========================================
# 1. FILTRO GLOBAL DE TEMPO (Ano)
# ==========================================
anos_disponiveis = sorted(pedidos['order_purchase_timestamp'].dt.year.dropna().unique())

with st.expander("⚙️ Abrir Filtros da Página", expanded=False):
    ano_selecionado = st.multiselect("📅 Selecione o Ano", options=anos_disponiveis, default=anos_disponiveis)

# Aplica o filtro de Ano em todos os DataFrames da página
if ano_selecionado:
    df_estado     = df_estado[df_estado['ano'].isin(ano_selecionado)]
    df_receita    = df_receita[df_receita['ano'].isin(ano_selecionado)]
    df_categorias = df_categorias[df_categorias['ano'].isin(ano_selecionado)]


# ==========================================
# 2. LEITURA DO CLIQUE NO MAPA (O "Truque" da Memória)
# ==========================================
estado_selecionado_mapa = None

# "Espiando" se o mapa já foi clicado antes mesmo de desenhá-lo
if "meu_mapa_interativo" in st.session_state:
    selecao = st.session_state["meu_mapa_interativo"].get("selection", {})
    if selecao and selecao.get("points"):
        estado_selecionado_mapa = selecao["points"][0]["location"]

# Criamos um DataFrame exclusivo para os KPIs. 
# Se tem estado selecionado, filtra. Se não, usa o Brasil inteiro.
if estado_selecionado_mapa:
    df_kpi = df_estado[df_estado['customer_state'] == estado_selecionado_mapa]
else:
    df_kpi = df_estado


# ==========================================
# 3. KPIs (Topo) - Usando o df_kpi!
# ==========================================
st.write("") 
st.write("")

st.subheader("Indicadores Gerais")
col1, col2, col3, col4 = st.columns(4)

# Valores dos KPIs
receita_total = df_kpi['receita_total'].sum()
total_pedidos = df_kpi['total_pedidos'].sum()

# Tratamento de erro caso o filtro retorne vazio
if total_pedidos > 0:
    ticket_medio = receita_total / total_pedidos
    prazo_medio = (
        df_kpi['soma_dias_total'].sum()
        / df_kpi['total_pedidos'].sum()
    )
else:
    ticket_medio = 0
    prazo_medio = 0


# ==========================================
# FORMATAÇÃO DOS CARDS
# ==========================================
def formatar_moeda_card(valor):
    if valor >= 1_000_000:
        # Usa o PONTO direto (ex: 15.42 milhões)
        return f"R$ {valor / 1_000_000:.2f} mi"
        
    elif valor >= 1_000:
        # Usa o PONTO direto (ex: 15.4 mil)
        return f"R$ {valor / 1_000:.1f} mil"
        
    else:
        # Usa a VÍRGULA apenas para valores inteiros menores (ex: R$ 158,52)
        texto = f"R$ {valor:,.2f}"
        return texto.replace(",", "X").replace(".", ",").replace("X", ".")
    
def formatar_contagem(valor):
    # Mantém a inversão para garantir que 96.478 fique com ponto no milhar
    texto = f"{valor:,.0f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


# ==========================================
# EXIBIÇÃO DOS KPIs
# ==========================================

col1.metric("Faturamento Total", formatar_moeda_card(receita_total))

col2.metric("Total de Pedidos", formatar_contagem(total_pedidos))

col3.metric("Ticket Médio", formatar_moeda_card(ticket_medio))

# Aqui aplicamos um .replace(".", ",") rápido para o prazo médio ficar 12,5 em vez de 12.5
texto_prazo = f"{prazo_medio:.1f} dias".replace(".", ",")
col4.metric("Prazo Médio de Entrega", texto_prazo)


st.write("") # Espaçamento extra (substituindo o br do HTML para ficar mais limpo)
st.divider()
# ==========================================
# 4. MAPA DO BRASIL
# ==========================================
# st.subheader("🗺️ Faturamento por Estado")
st.subheader("Faturamento por Estado")
st.caption("Clique em um estado para filtrar os indicadores e análises abaixo.")

# O mapa CONTINUA usando o df_estado (que tem todos os estados do ano selecionado).
# Se usássemos o df_kpi aqui, o mapa sumiria com o resto do Brasil!
df_mapa = (df_estado.groupby('customer_state')
                    .agg(
                        receita_total = ('receita_total', 'sum'),
                        total_pedidos = ('total_pedidos', 'sum')
                    )
                    .reset_index())
df_mapa['ticket_medio'] = (df_mapa['receita_total'] / df_mapa['total_pedidos']).round(2)

fig_mapa = px.choropleth(
    df_mapa,
    geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
    locations='customer_state',
    featureidkey='properties.sigla',
    color='receita_total',
    hover_data=['total_pedidos', 'ticket_medio'],
    color_continuous_scale='Blues',
    labels={
        'customer_state': 'Estado',
        'receita_total': 'Receita Total',
        'total_pedidos': 'Total de Pedidos',
        'ticket_medio': 'Ticket Médio'
    }
)
fig_mapa.update_geos(fitbounds="locations", visible=False)
fig_mapa.update_layout(margin={"r":0,"t":10,"l":0,"b":10})

# O segredo final: o parâmetro KEY que guarda o clique na memória
evento_mapa = st.plotly_chart(
    fig_mapa, 
    use_container_width=True, 
    on_select="rerun", 
    key="meu_mapa_interativo" # <--- ESSA KEY É FUNDAMENTAL
)


# ==========================================
# 5. FILTRO DOS GRÁFICOS ABAIXO DO MAPA
# ==========================================
if estado_selecionado_mapa:
    st.info(f"📍 Estado selecionado: **{estado_selecionado_mapa}**. " 
            "Clique novamente no estado para retornar à visão nacional.")
    
    # Cruzamento de filtros (Cross-Filtering) para Receita Mensal e Categorias
    df_categorias = df_categorias[df_categorias['customer_state'] == estado_selecionado_mapa]
    df_receita    = df_receita[df_receita['customer_state'] == estado_selecionado_mapa]

st.divider()
# ==========================================
# 6. GRÁFICO DE BARRAS (Largura Total)
# ==========================================
st.subheader("Top 10 Categorias por Pedidos") #🏆 

# ------------------------------------------
# Tratamento de Dados
# ------------------------------------------
df_cat = (df_categorias.groupby('product_category_name')
                       .agg(
                           receita_total = ('receita_total', 'sum'),
                           total_pedidos = ('total_pedidos', 'sum'),
                           total_itens   = ('total_itens',   'sum')
                       )
                       .reset_index()
                       .sort_values('total_pedidos', ascending=False)
                       .head(10))

# Prevenção de erro caso o estado clicado não tenha vendas
if not df_cat.empty:
    df_cat['ticket_medio']     = (df_cat['receita_total'] / df_cat['total_pedidos']).round(2)
    df_cat['preco_medio_item'] = (df_cat['receita_total'] / df_cat['total_itens']).round(2)

    df_cat['product_category_name'] = df_cat['product_category_name'].str.replace('_', ' ').str.title()

    # ------------------------------------------
    # Gráfico
    # ------------------------------------------
    fig_cat = px.bar(
        df_cat,
        x='total_pedidos',
        y='product_category_name',
        orientation='h',
        text_auto='.2s', 
        color_discrete_sequence=['#1F3B73'],
        hover_data=['total_pedidos', 'ticket_medio'],
        labels={'total_pedidos': 'Total de Pedidos', 'product_category_name': 'Categoria'}
    )
    
    # ------------------------------------------
    # Rótulos
    # ------------------------------------------
    fig_cat.update_traces(
        textposition='outside',
        cliponaxis=False # Evita que o número (ex: 9.3k) seja cortado na direita
    ) 
    
    # ------------------------------------------
    # Layout 
    # ------------------------------------------
    fig_cat.update_layout(
        xaxis=dict(
            title=None,              # Remove o título inferior ("Total de Pedidos")
            showgrid=False,          # Remove as linhas de grade verticais
            showticklabels=False     # Remove os números do eixo X
        ),
        yaxis=dict(
            title=None,              # Remove a palavra lateral ("Categoria")
            categoryorder='total ascending' # Garante a maior barra no topo
        ),
        margin=dict(r=40, l=10, t=10, b=10) # Margem 'r' (direita) dá espaço para o rótulo da barra maior
    )
    
    st.plotly_chart(fig_cat, use_container_width=True)
else:
    st.warning("Não há dados de categorias para o estado selecionado.")

st.divider()
# ==========================================
# 7. LINHA DO TEMPO (Largura Total)
# ==========================================
st.subheader("📈 Evolução Mensal do Faturamento")

# Prevenção de erro caso o estado clicado não tenha histórico
if not df_receita.empty:
    
    # ------------------------------------------
    # Tratamento de Dados
    # ------------------------------------------
    # Agrupamos novamente a receita, pois agora ela tem a granularidade de estado
    df_linha = (df_receita.groupby(['ano', 'mes', 'ano_mes'])
                          .agg(receita_total = ('receita_total', 'sum'))
                          .reset_index()
                          .sort_values(['ano', 'mes']))

    # ------------------------------------------
    # Gráfico
    # ------------------------------------------
    fig_receita = px.line(
        df_linha,
        x='ano_mes',
        y='receita_total',
        markers=True,
        text='receita_total',
        labels={'ano_mes': 'Mês', 'receita_total': 'Receita Total (R$)'}
    )
    
    # ------------------------------------------
    # Rótulos
    # ------------------------------------------
    fig_receita.update_traces(
        textposition='top center', 
        texttemplate='%{text:.2s}',
        cliponaxis=False # Evita que o número do pico do gráfico seja cortado
    ) 
    
    # ------------------------------------------
    # Layout (Limpeza Visual Executiva)
    # ------------------------------------------
    max_y_linha = df_linha['receita_total'].max()
    
    fig_receita.update_layout(
        xaxis_tickangle=-45,
        xaxis_title=None,             # Remove a palavra "Mês"
        yaxis=dict(
            title=None,               # Remove a palavra "Receita Total (R$)"
            showgrid=False,           # Remove linhas horizontais
            showticklabels=False,     # Remove os números laterais do eixo Y
            range=[0, max_y_linha * 1.15] # 15% de respiro no topo
        ),
        margin=dict(r=20, l=10, t=30, b=10) 
    )
    
    st.plotly_chart(fig_receita, use_container_width=True)
else:
    st.warning("Não há dados de receita para o estado selecionado.")

st.divider()
# ==========================================
# 8. ANÁLISE MoM — MONTH OVER MONTH
# ==========================================

st.subheader("📊 Variação Mensal da Receita (MoM)")
st.caption("Compara a receita de cada mês com o mês calendário imediatamente anterior.")

# ------------------------------------------
# Preparação da Análise
# ------------------------------------------
if estado_selecionado_mapa:
    df_mom = (
        df_receita[
            [
                'ano', 'mes', 'mes_nome', 'ano_mes',
                'receita_total', 'receita_mes_anterior', 'variacao_mom_pct'
            ]
        ]
        .copy()
        .sort_values(['ano', 'mes'])
    )
else:
    df_mom = (df_receita.groupby(
            ['ano', 'mes', 'mes_nome', 'ano_mes'],
            as_index=False).agg(receita_total=('receita_total', 'sum')
        ).sort_values(['ano', 'mes'])
    )
    df_mom['receita_mes_anterior'] = (df_mom['receita_total'].shift(1))
    df_mom['variacao_mom_pct'] = np.where(
        df_mom['receita_mes_anterior'] > 0,
        (
            (df_mom['receita_total']- df_mom['receita_mes_anterior'])
            / df_mom['receita_mes_anterior'] * 100
        ), np.nan).round(2)

# ------------------------------------------
# Preparação da Tabela
# ------------------------------------------
df_mom['Mês'] = (df_mom['mes_nome']+ "/" + df_mom['ano'].astype(str))

df_mom_tabela = (df_mom[
        [
            'Mês',
            'receita_total',
            'receita_mes_anterior',
            'variacao_mom_pct'
        ]
    ].rename(
        columns={
            'receita_total': 'Receita',
            'receita_mes_anterior': 'Receita Mês Anterior',
            'variacao_mom_pct': 'MoM (%)'
        }
    )
)

# Identificação do contexto da análise
if estado_selecionado_mapa:
    st.caption(f"📍 Análise MoM do estado **{estado_selecionado_mapa}**")
else:
    st.caption("🌎 Análise MoM do Brasil")


# ==========================================
# 9. EXIBIÇÃO E FORMATAÇÃO DA TABELA
# ==========================================
df_exibir = df_mom_tabela.copy()

# Tratamento de Nulos (Remove os 'nan' antes de formatar como string)
df_exibir = df_exibir.fillna('-')

# Formatação Moeda
df_exibir['Receita'] = df_exibir['Receita'].apply(
    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if isinstance(x, (int, float)) else x
)

df_exibir['Receita Mês Anterior'] = df_exibir['Receita Mês Anterior'].apply(
    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if isinstance(x, (int, float)) else x
)

# Formatação Percentual (Ignora se for um hífen)
df_exibir['MoM (%)'] = df_exibir['MoM (%)'].apply(
    lambda x: f"{x:.2f}%".replace(".", ",") if isinstance(x, (int, float)) else x
)

# Plotagem
st.dataframe(
    df_exibir,
    use_container_width=True,
    hide_index=True
)
st.divider()