import pandas as pd


def get_vw_clientes_regiao(pedidos, clientes):

    # ==========================================
    # 1. MERGE DAS TABELAS
    # ==========================================
    # Une pedidos e clientes pelo customer_id.
    # O LEFT JOIN preserva todos os pedidos, mesmo
    # que algum registro de cliente não seja encontrado.
    df = pedidos.merge(
        clientes,
        on='customer_id',
        how='left'
    )

    # ==========================================
    # 2. TRADUÇÃO DOS STATUS
    # ==========================================
    status_traducao = {
        'delivered':   'Entregue',
        'shipped':     'Em Transporte',
        'canceled':    'Cancelado',
        'unavailable': 'Indisponível',
        'invoiced':    'Faturado',
        'processing':  'Em Processamento',
        'created':     'Criado',
        'approved':    'Aprovado'
    }

    df['status_pt'] = (
        df['order_status']
        .map(status_traducao)
        .fillna('Outros')
    )

    # ==========================================
    # 3. DIMENSÕES DE TEMPO
    # ==========================================
    df['ano'] = (df['order_purchase_timestamp'].dt.year)

    df['mes'] = (df['order_purchase_timestamp'].dt.month)

    df['data_mes'] = (df['order_purchase_timestamp'].dt.to_period('M').astype(str))

    # ==========================================
    # 4. AGREGAÇÃO ANALÍTICA
    # ==========================================
    # Granularidade:
    # Estado × Cidade × Ano × Mês × Status
    #
    # total_clientes:
    # quantidade de clientes únicos que possuem
    # pedido naquele estado/cidade/mês/status.
    #
    # total_pedidos:
    # quantidade de pedidos únicos naquela
    # mesma granularidade.
    resultado = (
        df.groupby(
            [
                'customer_state',
                'customer_city',
                'ano',
                'mes',
                'data_mes',
                'status_pt'
            ]
        ).agg(total_clientes=('customer_unique_id','nunique'),
              total_pedidos=('order_id','nunique')).reset_index()
    )

    # ==========================================
    # 5. RETORNO
    # ==========================================
    # O percentual não é calculado nesta View.
    # Ele deve ser calculado na camada de apresentação
    # conforme o contexto da análise, evitando dupla
    # contagem de clientes entre diferentes status.
    return resultado.sort_values(
        'total_clientes',
        ascending=False
    )