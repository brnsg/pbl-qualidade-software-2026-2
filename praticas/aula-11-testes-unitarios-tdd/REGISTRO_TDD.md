# Registro do ciclo de TDD

## Comportamento escolhido

1. Cobrar taxa inicial de R$ 5,00 para distância de até 3 km (2 km e pedido de R$ 50,00).
2. Acrescentar R$ 2,00 por quilômetro excedente acima de 3 km (4 km e pedido de R$ 50,00).
3. Conceder entrega gratuita para pedidos a partir de R$ 100,00 (5 km e pedido de R$ 100,00).

## Red

**Teste criado:**
- Ciclo 1: `test_taxa_entrega_ate_3km`
- Ciclo 2: `test_taxa_entrega_acima_de_3km`
- Ciclo 3: `test_taxa_entrega_gratuita_para_pedido_a_partir_de_100`

**Motivo da falha:**
- Ciclo 1: A função `calcular_taxa_entrega` possuía apenas `pass` e retornava `None` (`assert None == 5`).
- Ciclo 2: A função retornava valor fixo `5`, falhando para 4 km (`assert 5 == 7`).
- Ciclo 3: A função calculava a distância sem verificar o valor mínimo para frete grátis (`assert 9 == 0`).

## Green

**Implementacao realizada:**
- Ciclo 1: `return 5`
- Ciclo 2: `if distancia_km <= 3: return 5` seguido de `return 5 + (distancia_km - 3) * 2`
- Ciclo 3: Adicionada verificação `if total_pedido >= 100: return 0` no início da função.

## Refactor

**Melhoria realizada:** Adicionadas anotações de tipo (`distancia_km: float, total_pedido: float -> float`) mantendo a legibilidade e consistência com o restante do módulo `src/pedido.py`.

**Resultado final:** Todos os 7 testes da suíte (`tests/test_pedido.py`) passaram com sucesso (`7 passed`).
