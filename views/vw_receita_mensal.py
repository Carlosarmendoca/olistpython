
import pandas as pd
import numpy as np


def get_receita_mensal(pedidos, pagamentos, clientes):

    # =========================================================
    # 1. TRADUÇÃO DOS MESES
    # =========================================================

    meses_traducao = {
        'Jan': 'Jan', 'Feb': 'Fev', 'Mar': 'Mar',
        'Apr': 'Abr', 'May': 'Mai', 'Jun': 'Jun',
        'Jul': 'Jul', 'Aug': 'Ago', 'Sep': 'Set',
        'Oct': 'Out', 'Nov': 'Nov', 'Dec': 'Dez'
    }


    # =========================================================
    # 2. MERGE DOS DATAFRAMES
    # =========================================================
    # Pedidos → Pagamentos → Clientes
    #
    # O merge com clientes é necessário para obter
    # o customer_state.
    # =========================================================

    df = (
        pedidos
        .merge(pagamentos, on='order_id', how='left')
        .merge(
            clientes[['customer_id', 'customer_state']],
            on='customer_id',
            how='left'
        )
    )


    # =========================================================
    # 3. CONSIDERAR SOMENTE PEDIDOS ENTREGUES
    # =========================================================

    df = df[df['order_status'] == 'delivered'].copy()


    # =========================================================
    # 4. CRIAÇÃO DAS DIMENSÕES DE TEMPO
    # =========================================================

    df['ano'] = (
        df['order_purchase_timestamp']
        .dt.year
    )

    df['mes'] = (
        df['order_purchase_timestamp']
        .dt.month
    )

    df['mes_nome'] = (
        df['order_purchase_timestamp']
        .dt.strftime('%b')
        .map(meses_traducao)
    )

    df['ano_mes'] = (
        df['order_purchase_timestamp']
        .dt.to_period('M')
        .astype(str)
    )


    # =========================================================
    # 5. RECEITA MENSAL POR ESTADO
    # =========================================================
    # Aqui temos somente os meses que realmente possuem
    # movimentação.
    # =========================================================

    resultado = (
        df.groupby(
            [
                'customer_state',
                'ano',
                'mes',
                'mes_nome',
                'ano_mes'
            ]
        )
        .agg(
            total_pedidos=('order_id', 'nunique'),
            receita_total=('payment_value', 'sum')
        )
        .reset_index()
    )

    resultado['receita_total'] = (
        resultado['receita_total']
        .round(2)
    )


    # =========================================================
    # 6. CRIAR CALENDÁRIO MENSAL COMPLETO
    # =========================================================
    #
    # Este é o ponto novo.
    #
    # Exemplo:
    #
    # SP possui:
    # 2016-10
    # 2017-01
    #
    # O calendário vai criar também:
    # 2016-11
    # 2016-12
    #
    # Assim conseguimos mostrar esses meses na tabela.
    # =========================================================

    estados = resultado['customer_state'].dropna().unique()

    data_inicio = pd.to_datetime(
        resultado['ano_mes'].min()
    )

    data_fim = pd.to_datetime(
        resultado['ano_mes'].max()
    )

    calendario = pd.DataFrame({
        'ano_mes': pd.period_range(
            start=data_inicio,
            end=data_fim,
            freq='M'
        ).astype(str)
    })


    # =========================================================
    # 7. CRIAR TODAS AS COMBINAÇÕES
    # ESTADO × MÊS
    # =========================================================

    calendario['chave'] = 1

    estados_df = pd.DataFrame({
        'customer_state': estados
    })

    estados_df['chave'] = 1

    calendario_completo = (
        estados_df
        .merge(calendario, on='chave')
        .drop(columns='chave')
    )


    # =========================================================
    # 8. MERGE COM OS DADOS REAIS
    # =========================================================

    resultado = calendario_completo.merge(
        resultado,
        on=['customer_state', 'ano_mes'],
        how='left'
    )


    # =========================================================
    # 9. RECONSTRUIR ANO, MÊS E NOME DO MÊS
    # =========================================================

    data_mes = pd.to_datetime(
        resultado['ano_mes']
    )

    resultado['ano'] = data_mes.dt.year
    resultado['mes'] = data_mes.dt.month

    resultado['mes_nome'] = (
        data_mes
        .dt.strftime('%b')
        .map(meses_traducao)
    )


    # =========================================================
    # 10. PREENCHER MESES SEM MOVIMENTAÇÃO
    # =========================================================
    #
    # Receita sem movimentação = 0
    # Pedidos sem movimentação = 0
    #
    # IMPORTANTE:
    # Esses zeros servem para a visualização.
    # Eles NÃO serão utilizados como mês anterior
    # no cálculo do MoM.
    # =========================================================

    resultado['receita_total'] = (
        resultado['receita_total']
        .fillna(0)
        .round(2)
    )

    resultado['total_pedidos'] = (
        resultado['total_pedidos']
        .fillna(0)
        .astype(int)
    )


    # =========================================================
    # 11. ORDENAÇÃO
    # =========================================================

    resultado = (
        resultado
        .sort_values(
            ['customer_state', 'ano', 'mes']
        )
        .reset_index(drop=True)
    )


    # =========================================================
    # 12. IDENTIFICAR O MÊS CALENDÁRIO ANTERIOR
    # =========================================================

    resultado['ano_mes_anterior'] = (
        pd.to_datetime(resultado['ano_mes'])
        - pd.DateOffset(months=1)
    ).dt.to_period('M').astype(str)


        # =========================================================
    # 13. IDENTIFICAR A LINHA ANTERIOR
    # =========================================================
    #
    # Como agora tem TODOS os meses no calendário,
    # o shift representa o mês calendário anterior.
    # =========================================================

    resultado['ano_mes_linha_anterior'] = (
        resultado
        .groupby('customer_state')['ano_mes']
        .shift(1)
    )

    resultado['receita_mes_anterior'] = (
        resultado
        .groupby('customer_state')['receita_total']
        .shift(1)
    )


    # =========================================================
    # 14. VALIDAR SE O MÊS ANTERIOR É REALMENTE O ANTERIOR
    # =========================================================
    #
    # Como o calendário está completo, normalmente o shift
    # já representa o mês calendário anterior.
    #
    # Mantemos esta validação para garantir a consistência.
    # =========================================================

    resultado.loc[
        resultado['ano_mes_linha_anterior']
        != resultado['ano_mes_anterior'],
        'receita_mes_anterior'
    ] = np.nan


    # =========================================================
    # 15. CÁLCULO DO MoM
    # =========================================================
    #
    # O MoM só será calculado quando:
    #
    #   • o mês anterior tiver receita > 0
    #   • o mês atual tiver receita > 0
    #
    # A receita_mes_anterior, porém, continua mostrando
    # o valor real do mês anterior.
    # =========================================================

    resultado['variacao_mom_pct'] = (
        (
            resultado['receita_total']
            - resultado['receita_mes_anterior']
        )
        / resultado['receita_mes_anterior']
        * 100
    ).round(2)


    # =========================================================
    # 16. EVITAR INFINITO E CASOS SEM BASE VÁLIDA
    # =========================================================

    resultado['variacao_mom_pct'] = (
        resultado['variacao_mom_pct']
        .replace([np.inf, -np.inf], np.nan)
    )

    # =========================================================
    # 17. REMOVER COLUNAS AUXILIARES
    # =========================================================

    resultado = resultado.drop(
        columns=[
            'ano_mes_anterior',
            'ano_mes_linha_anterior'
        ]
    )


    # =========================================================
    # 18. ORDEM FINAL DAS COLUNAS
    # =========================================================

    resultado = resultado[
        [
            'customer_state',
            'ano',
            'mes',
            'mes_nome',
            'ano_mes',
            'total_pedidos',
            'receita_total',
            'receita_mes_anterior',
            'variacao_mom_pct'
        ]
    ]


    return resultado
