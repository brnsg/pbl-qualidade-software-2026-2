# Responsável: Brian da Silva Guterres
import pytest

from src.regras_localeats import pedido_atingiu_valor_minimo


# Responsável: Brian da Silva Guterres
# TU01 - comportamento esperado: pedido acima do mínimo
def test_pedido_acima_do_minimo_retorna_true():
    resultado = pedido_atingiu_valor_minimo(50)
    assert resultado is True


# Responsável: Brian da Silva Guterres
# TU02 - comportamento alternativo: pedido abaixo do mínimo
def test_pedido_abaixo_do_minimo_retorna_false():
    resultado = pedido_atingiu_valor_minimo(20)
    assert resultado is False


# Responsável: Brian da Silva Guterres
# TU03 - caso de borda: valores exatamente no limite e logo abaixo dele
@pytest.mark.parametrize(
    "valor, esperado",
    [(30, True), (30.00, True), (29.99, False), (0, False)],
)
def test_limite_do_valor_minimo(valor, esperado):
    assert pedido_atingiu_valor_minimo(valor) is esperado


# Responsável: Brian da Silva Guterres
# TU04 - comportamento inválido: valor negativo gera ValueError
def test_valor_negativo_gera_value_error():
    with pytest.raises(ValueError):
        pedido_atingiu_valor_minimo(-1)
