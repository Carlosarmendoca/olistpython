import pandas as pd
import numpy as np

def get_clientes_regiao(pedidos, clientes):

    df = pedidos.merge(clientes, on='customer_id', how='left')

    df['ano']      = df['order_purchase_timestamp'].dt.year
    df['data_mes'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

    resultado = (df.groupby(['customer_state', 'customer_city', 'ano', 'data_mes', 'order_status'])
                   .agg(
                       total_clientes = ('customer_unique_id', 'nunique'),
                       total_pedidos  = ('order_id',           'nunique')
                   )
                   .reset_index()
                   .sort_values('total_clientes', ascending=False))

    return resultado