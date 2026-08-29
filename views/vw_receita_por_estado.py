import pandas as pd


def get_receita_por_estado(pedidos, clientes, pagamentos):

    # ==========================================
    # 1. CONSOLIDANDO OS PAGAMENTOS POR PEDIDO
    # ==========================================
    # Um pedido pode possuir mais de um registro de pagamento.
    # Consolidamos primeiro para evitar duplicação (fan-out)
    # após o merge com a tabela de pedidos.
    pagamentos_consolidados = (pagamentos.groupby('order_id', as_index=False)
        .agg(total_pago_pedido=('payment_value', 'sum')))

    # ==========================================
    # 2. UNINDO AS TABELAS
    # ==========================================
    df = (pedidos.merge(
            clientes[
                ['customer_id', 'customer_state', 'customer_city']
            ],
            on='customer_id',
            how='left').merge(pagamentos_consolidados,on='order_id',how='left'))

    # ==========================================
    # 3. FILTRANDO PEDIDOS ENTREGUES
    # ==========================================
    df = df[df['order_status'] == 'delivered'].copy()

    # ==========================================
    # 4. CRIANDO DIMENSÕES DE TEMPO
    # ==========================================
    # Ano da compra
    df['ano'] = (df['order_purchase_timestamp'].dt.year)

    # Mês da compra
    df['data_mes'] = (df['order_purchase_timestamp'].dt.to_period('M').astype(str))

    # ==========================================
    # 5. CRIANDO CÓDIGO GEOGRÁFICO DO ESTADO
    # ==========================================
    # Formato utilizado para representar os estados
    # brasileiros em mapas geográficos.
    # Exemplo: SP → BR-SP
    df['state_geo'] = ('BR-' + df['customer_state'])

    # ==========================================
    # 6. CALCULANDO PRAZOS DE ENTREGA
    # ==========================================
    # Tempo entre a compra e a entrega à transportadora
    df['dias_separacao'] = (
    df['order_delivered_carrier_date'].dt.normalize()- df['order_purchase_timestamp'].dt.normalize()).dt.days

    # Tempo entre a entrega à transportadora e a entrega
    # ao cliente
    df['dias_transporte'] = (
    df['order_delivered_customer_date'].dt.normalize()- df['order_delivered_carrier_date'].dt.normalize()).dt.days

    # Tempo total entre a compra e a entrega ao cliente
    df['dias_total'] = (
    df['order_delivered_customer_date'].dt.normalize()- df['order_purchase_timestamp'].dt.normalize()).dt.days

    # ==========================================
    # 7. AGRUPANDO OS DADOS
    # ==========================================
    resultado = (
    df.groupby(
        ['customer_state', 'state_geo', 'ano', 'data_mes']
    )
    .agg(
        total_pedidos=('order_id', 'nunique'),
        total_clientes=('customer_id', 'nunique'),
        receita_total=('total_pago_pedido', 'sum'),
        soma_dias_separacao=('dias_separacao', 'sum'),
        soma_dias_transporte=('dias_transporte', 'sum'),
        soma_dias_total=('dias_total', 'sum'),
        total_pedidos_entregues=('order_id', 'nunique')
    )
    .reset_index()
)

    # ==========================================
    # 8. CALCULANDO INDICADORES DERIVADOS
    # ==========================================

    # Receita total
    resultado['receita_total'] = (resultado['receita_total'].round(2))

    # Ticket médio por pedido
    resultado['ticket_medio'] = (resultado['receita_total'] / resultado['total_pedidos']).round(2)

    # Prazo médio de separação
    resultado['prazo_separacao_dias'] = (resultado['soma_dias_separacao'] / resultado['total_pedidos_entregues']).round(1)

    # Prazo médio de transporte
    resultado['prazo_transporte_dias'] = (resultado['soma_dias_transporte'] / resultado['total_pedidos_entregues']).round(1)

    # Prazo médio total de entrega
    resultado['prazo_total_dias'] = (resultado['soma_dias_total'] / resultado['total_pedidos_entregues']).round(1)

    return resultado