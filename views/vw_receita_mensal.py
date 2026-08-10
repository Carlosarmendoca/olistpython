import pandas as pd
import numpy as np

def get_receita_mensal(pedidos, pagamentos, clientes): # <-- Adicionado 'clientes' aqui

    meses_traducao = {
        'Jan': 'Jan', 'Feb': 'Fev', 'Mar': 'Mar',
        'Apr': 'Abr', 'May': 'Mai', 'Jun': 'Jun',
        'Jul': 'Jul', 'Aug': 'Ago', 'Sep': 'Set',
        'Oct': 'Out', 'Nov': 'Nov', 'Dec': 'Dez'
    }

    # Merge com pagamentos e depois com clientes para pegar o estado
    df = (pedidos
          .merge(pagamentos, on='order_id', how='left')
          .merge(clientes[['customer_id', 'customer_state']], on='customer_id', how='left'))
          
    df = df[df['order_status'] == 'delivered']

    df['ano']      = df['order_purchase_timestamp'].dt.year
    df['mes']      = df['order_purchase_timestamp'].dt.month
    df['mes_nome'] = df['order_purchase_timestamp'].dt.strftime('%b').map(meses_traducao)
    df['ano_mes']  = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

    # Adicionado 'customer_state' no agrupamento
    resultado = (df.groupby(['customer_state', 'ano', 'mes', 'mes_nome', 'ano_mes'])
                   .agg(
                       total_pedidos = ('order_id', 'nunique'),
                       receita_total = ('payment_value', 'sum')
                   )
                   .reset_index()
                   .sort_values(['ano', 'mes']))

    resultado['receita_total'] = resultado['receita_total'].round(2)

    # Variação MoM (calculada por estado agora)
    resultado['receita_mes_anterior'] = (
        resultado.groupby(['customer_state', 'ano'])['receita_total'].shift(1)
    )

    resultado['variacao_mom_pct'] = (
        (resultado['receita_total'] - resultado['receita_mes_anterior'])
        / resultado['receita_mes_anterior'] * 100
    ).round(2)

    resultado['variacao_mom_pct'] = resultado['variacao_mom_pct'].replace([np.inf, -np.inf], np.nan)

    return resultado