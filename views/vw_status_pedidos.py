import pandas as pd

def get_status_pedidos(pedidos, clientes): # <-- Adicionado 'clientes' aqui

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
    
    # Fazendo o merge com a tabela de clientes para trazer o customer_state
    df = pedidos.merge(clientes[['customer_id', 'customer_state']], on='customer_id', how='left')
    
    df['status_pt']  = df['order_status'].map(status_traducao)
    df['ano']        = df['order_purchase_timestamp'].dt.year
    df['mes']        = df['order_purchase_timestamp'].dt.month
    df['ano_mes']    = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

    # Adicionado 'customer_state' no groupby
    resultado = (df.groupby(['customer_state', 'ano', 'mes', 'ano_mes', 'status_pt'])
                   .size()
                   .reset_index(name='quantidade'))

    # O total do mês agora também agrupa por estado para o cálculo do percentual ficar correto
    total_mes = resultado.groupby(['customer_state', 'ano_mes'])['quantidade'].transform('sum')
    resultado['percentual'] = (resultado['quantidade'] / total_mes * 100).round(2)

    return resultado