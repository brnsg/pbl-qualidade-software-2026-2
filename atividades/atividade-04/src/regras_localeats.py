# Responsável: Brian da Silva Guterres
"""Regras de negócio do LocalEats."""

VALOR_MINIMO_PEDIDO = 30.00


def pedido_atingiu_valor_minimo(valor_pedido):
    """Retorna True se o pedido atingiu o valor mínimo de R$ 30,00.

    Pedidos abaixo de R$ 30,00 retornam False.
    Valores negativos geram ValueError.
    """
    if valor_pedido < 0:
        raise ValueError("O valor do pedido não pode ser negativo.")
    return valor_pedido >= VALOR_MINIMO_PEDIDO
