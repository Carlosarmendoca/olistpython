import pandas as pd
import numpy as np

def get_top_categorias(pedidos, itens, produtos, clientes): # <-- Adicionado 'clientes' aqui

    df = (itens
          .merge(produtos[['product_id', 'product_category_name']], on='product_id', how='left')
          .merge(pedidos[['order_id', 'order_status', 'order_purchase_timestamp', 'customer_id']], on='order_id', how='left')
          .merge(clientes[['customer_id', 'customer_state']], on='customer_id', how='left')) # <-- Novo merge

    df = df[df['order_status'] == 'delivered']

    df['ano']             = df['order_purchase_timestamp'].dt.year
    df['data_mes']        = df['order_purchase_timestamp'].dt.to_period('M').astype(str)
    df['receita_produto'] = df['price']
    df['receita_frete']   = df['freight_value']
    df['receita_item']    = df['price'] + df['freight_value']

    # Adicionado 'customer_state' no agrupamento
    resultado = (df.groupby(['customer_state', 'product_category_name', 'ano', 'data_mes'])
                   .agg(
                       total_pedidos    = ('order_id',        'nunique'),
                       total_itens      = ('order_item_id',   'count'),
                       total_vendedores = ('seller_id',       'nunique'),
                       receita_produtos = ('receita_produto', 'sum'),
                       receita_frete    = ('receita_frete',   'sum'),
                       receita_total    = ('receita_item',    'sum'),
                   )
                   .reset_index()
                   .sort_values('receita_total', ascending=False))

    resultado['receita_total']    = resultado['receita_total'].round(2)
    resultado['receita_produtos'] = resultado['receita_produtos'].round(2)
    resultado['receita_frete']    = resultado['receita_frete'].round(2)
    resultado['ticket_medio']     = (resultado['receita_total'] / resultado['total_pedidos']).round(2)
    resultado['preco_medio_item'] = (resultado['receita_produtos'] / resultado['total_itens']).round(2)

    return resultado