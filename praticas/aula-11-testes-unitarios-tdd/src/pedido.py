"""Regras de negocio relacionadas ao calculo de pedidos."""


def validar_item(item: dict) -> None:
    """Valida preco e quantidade de um item.

    Raises:
        ValueError: se o preco ou a quantidade nao forem positivos.
    """
    if item["preco"] <= 0:
        raise ValueError("O preco deve ser positivo.")

    if item["quantidade"] <= 0:
        raise ValueError("A quantidade deve ser positiva.")


def calcular_total(itens: list[dict]) -> float:
    """Calcula o total do pedido.

    Uma lista vazia resulta em total igual a zero.
    """
    total = 0

    for item in itens:
        validar_item(item)
        total += item["preco"] * item["quantidade"]

    return total


# EXERCICIO:
# Implemente com TDD a funcao descrita abaixo.


def calcular_taxa_entrega(distancia_km: float, total_pedido: float) -> float:
    """Calcula a taxa de entrega.

    Regras obrigatorias:
    - ate 3 km, a taxa e R$ 5;
    - acima de 3 km, acrescentar R$ 2 por quilometro excedente;
    - pedidos a partir de R$ 100 possuem entrega gratuita.

    Desafio opcional:
    - distancia negativa deve gerar ValueError.
    """
    if total_pedido >= 100:
        return 0

    if distancia_km <= 3:
        return 5

    return 5 + (distancia_km - 3) * 2
