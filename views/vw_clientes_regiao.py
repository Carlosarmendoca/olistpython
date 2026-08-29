import pandas as pd

def get_vw_clientes_regiao(pedidos, clientes):
    # 1. Merge das tabelas (trazendo todas as informações de clientes)
    df = pedidos.merge(clientes, on='customer_id', how='left')
    
    # 2. Tradução de status
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
    df['status_pt'] = df['order_status'].map(status_traducao).fillna('Outros')
    
    # 3. Tratamento de Datas
    df['ano'] = df['order_purchase_timestamp'].dt.year
    df['mes'] = df['order_purchase_timestamp'].dt.month
    df['data_mes'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
    
    # 4. Agrupamento Único (aqui está a mágica da sua View do SQL)
    resultado = (df.groupby(['customer_state', 'customer_city', 'ano', 'mes', 'data_mes', 'status_pt'])
                   .agg(
                       total_clientes = ('customer_unique_id', 'nunique'),
                       total_pedidos  = ('order_id', 'nunique')
                   )
                   .reset_index())
    
    # 5. Cálculo do Percentual (mantendo a funcionalidade que você tinha em status_pedidos)
    # Calcula o total de clientes por estado e mês para gerar o percentual
    total_mes_estado = resultado.groupby(['customer_state', 'data_mes'])['total_clientes'].transform('sum')
    resultado['percentual'] = ((resultado['total_clientes'] / total_mes_estado) * 100).round(2)
    
    return resultado.sort_values('total_clientes', ascending=False)