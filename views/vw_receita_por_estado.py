import pandas as pd

def get_receita_por_estado(pedidos, clientes, pagamentos):

    df = (pedidos
          .merge(clientes[['customer_id', 'customer_state', 'customer_city']], on='customer_id', how='left')
          .merge(pagamentos, on='order_id', how='left'))

    df = df[df['order_status'] == 'delivered']

    df['ano']      = df['order_purchase_timestamp'].dt.year
    df['data_mes'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

    df['dias_separacao']  = (df['order_delivered_carrier_date'] - df['order_purchase_timestamp']).dt.days
    df['dias_transporte'] = (df['order_delivered_customer_date'] - df['order_delivered_carrier_date']).dt.days
    df['dias_total']      = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days

    resultado = (df.groupby(['customer_state', 'ano', 'data_mes'])
                   .agg(
                       total_pedidos           = ('order_id',       'nunique'),
                       total_clientes          = ('customer_id',    'nunique'),
                       receita_total           = ('payment_value',  'sum'),
                       soma_dias_separacao     = ('dias_separacao', 'sum'),
                       soma_dias_transporte    = ('dias_transporte','sum'),
                       soma_dias_total         = ('dias_total',     'sum'),
                       total_pedidos_entregues = ('order_id',       'nunique')
                   )
                   .reset_index())

    resultado['receita_total']         = resultado['receita_total'].round(2)
    resultado['ticket_medio']          = (resultado['receita_total'] / resultado['total_pedidos']).round(2)
    resultado['prazo_separacao_dias']  = (resultado['soma_dias_separacao'] / resultado['total_pedidos_entregues']).round(1)
    resultado['prazo_transporte_dias'] = (resultado['soma_dias_transporte'] / resultado['total_pedidos_entregues']).round(1)
    resultado['prazo_total_dias']      = (resultado['soma_dias_total'] / resultado['total_pedidos_entregues']).round(1)

    return resultado