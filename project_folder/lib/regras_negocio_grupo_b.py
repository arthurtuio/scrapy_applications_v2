

def DADOS_MEDICAO_DICT():
    return {
        "Equipamento": None,
        "Unidade de medida": None,
        "Origem da leitura atual": None,
        "Data da leitura anterior": None,
        "Data da leitura atual": None,
        "Data da próxima leitura": None,
        "Número de dias faturados": None,
        "Leitura atual": None,
        "Leitura anterior": None,
        "Constante de faturamento": None,
        "Consumo medido no mês": None,
        "Consumo faturado no mês": None,
        "Fator de potência": None,
    }


def HISTORICO_CONSUMO_ENERG_ELET_DICT():
    return {
        "Jan/": None,
        "Fev/": None,
        "Mar/": None,
        "Abr/": None,
        "Mai/": None,
        "Jun/": None,
        "Jul/": None,
        "Ago/": None,
        "Set/": None,
        "Out/": None,
        "Nov/": None,
        "Dez/": None,
    }


def N_DA_UNIDADE_CONSUMIDORA_DICT():
    return {
        "CONSUMIDORA": None,
        "VENCIMENTO": None,
        "CONSUMO TOTAL FATURADO": None,
        "VALOR ATÉ O VENCIMENTO": None,
        "Mensagens": None,
    }


def DADOS_DO_FATURAMENTO_DICT():
    return {
        "Consumo": {
            "Faturado": None,
            "Tarifa (R$)": None,
            "Valor (R$)": None,
        },
        "Subtotal (R$)": {"Valor (R$)": None},
    }


def LANCAMENTOS_E_SERVICOS_DICT():
    return {
        "Cosip": {"Valor (R$)": None},
        "Subtotal (R$)": {"Valor (R$)": None},
    }


def COMPOSICAO_PRECO_DICT():
    return {
        "DISTRIBUICAO": None,
        "ENC. SETORIAIS": None,
        "ENERGIA": None,
        "TRANSMISSAO": None,
        "TRIBUTOS": None,
        "Soma Demonstr.": None
    }
