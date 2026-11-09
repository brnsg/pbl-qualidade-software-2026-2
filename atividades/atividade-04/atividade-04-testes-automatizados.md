# Atividade 4: Testes Automatizados do LocalEats

**Unidade Curricular:** Qualidade de Software
**Projeto:** LocalEats — https://local-eats-unisenac.vercel.app/
**Modalidade:** Individual
**Integrante:** Brian da Silva Guterres

---

## 1. Estrutura do projeto

```
atividade-04/
├── atividade-04-testes-automatizados.md
├── relatorio-pytest.txt
├── requirements.txt
├── pytest.ini
├── features/
│   └── filtrar_categoria.feature      # cenário BDD (Gherkin)
├── src/
│   ├── __init__.py
│   └── regras_localeats.py            # pedido_atingiu_valor_minimo
└── tests/
    ├── __init__.py
    ├── conftest.py                    # URL base e dados únicos de usuário
    ├── test_regras_localeats.py       # testes unitários
    ├── test_localeats.py              # teste funcional (Playwright)
    └── test_bdd_categoria.py          # teste funcional BDD (pytest-bdd + Playwright)
```

### Como executar

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install chromium
python -m pytest -v | Tee-Object -FilePath relatorio-pytest.txt
```

---

## 2. Identificação das responsabilidades

| ID   | Integrante | Tipo       | Comportamento verificado                                   | Arquivo e função |
|------|------------|------------|------------------------------------------------------------|------------------|
| TU01 | Brian da Silva Guterres | Unitário   | Pedido acima do valor mínimo retorna `True`                | `tests/test_regras_localeats.py::test_pedido_acima_do_minimo_retorna_true` |
| TU02 | Brian da Silva Guterres | Unitário   | Pedido abaixo do valor mínimo retorna `False`              | `tests/test_regras_localeats.py::test_pedido_abaixo_do_minimo_retorna_false` |
| TU03 | Brian da Silva Guterres | Unitário   | Casos de borda (30, 30.00, 29.99, 0) — parametrizado       | `tests/test_regras_localeats.py::test_limite_do_valor_minimo` |
| TU04 | Brian da Silva Guterres | Unitário   | Valor negativo gera `ValueError` (`pytest.raises`)         | `tests/test_regras_localeats.py::test_valor_negativo_gera_value_error` |
| TF01 | Brian da Silva Guterres | Funcional  | Criar conta redireciona para a página inicial com saudação | `tests/test_localeats.py::test_criar_conta_redireciona_para_pagina_inicial_com_saudacao` |
| TF02 | Brian da Silva Guterres | Funcional (BDD) | Filtrar restaurantes pela categoria "Japonesa"        | `tests/test_bdd_categoria.py::test_filtrar_restaurantes_por_categoria` |

---

## 3. Parte 1 — Testes unitários e TDD

### TDD de Brian da Silva Guterres

**Regra escolhida:** Regra 1, verificar valor mínimo do pedido (`pedido_atingiu_valor_minimo(valor_pedido)`). Pedidos de R$ 30,00 ou mais retornam `True`; abaixo de R$ 30,00 retornam `False`; valores negativos geram `ValueError`.

**Primeiro teste escrito:** `test_pedido_acima_do_minimo_retorna_true`, que verifica se `pedido_atingiu_valor_minimo(50)` retorna `True`.

**Por que o teste falhou inicialmente:** a função ainda não existia no arquivo `src/regras_localeats.py`, então o pytest nem conseguiu importar o teste:

```
E   ImportError: cannot import name 'pedido_atingiu_valor_minimo' from 'src.regras_localeats'
1 error in 0.18s
```

**Implementação mínima realizada:** só o necessário para esse teste passar, que é retornar sempre `True`:

```python
def pedido_atingiu_valor_minimo(valor_pedido):
    return True
```

Resultado: `1 passed`.

**Segundo teste escrito:** `test_pedido_abaixo_do_minimo_retorna_false`, que verifica se `pedido_atingiu_valor_minimo(20)` retorna `False`. Com a implementação anterior ele falhou (`assert True is False`, `1 failed, 1 passed`), mostrando que o `return True` não bastava. A implementação foi ajustada para `return valor_pedido >= 30` e os dois testes passaram (`2 passed`).

Depois disso:
- o teste de limite com `@pytest.mark.parametrize` (30, 30.00, 29.99 e 0) passou de primeira (`6 passed`), confirmando que o `>=` já tratava corretamente o valor exato de R$ 30,00;
- o teste de valor negativo com `pytest.raises` falhou (`Failed: DID NOT RAISE ValueError`). Para ele passar, foi adicionada a validação `if valor_pedido < 0: raise ValueError(...)` (`7 passed`).

**Melhoria ou refatoração realizada:** o número `30` foi trocado pela constante `VALOR_MINIMO_PEDIDO = 30.00`, que deixa claro o que o valor significa. Também foram adicionadas uma docstring explicando a regra e a identificação do responsável e do ID (TU01–TU04) em cada teste. Os testes continuaram passando (`7 passed`).

---

## 4. Parte 2 — Testes funcionais com Playwright

Durante a exploração do LocalEats foi observado que, sem sessão, o sistema redireciona para `static/login.html`, que possui as abas **Entrar** e **Criar Conta**. Após o registro, o usuário é enviado para `static/index.html`, que exibe a saudação "Olá, <primeiro nome>", a busca, os filtros de categoria (Todos, Italiana, Japonesa, Brasileira, Mexicana) e os cards dos restaurantes (`.rest-card`).

Cada teste gera um e-mail único (`conftest.py`), garantindo que os testes sejam independentes e possam ser executados várias vezes. Nenhum teste usa `time.sleep`: as esperas são feitas pelas assertions `expect(...)` do Playwright, que aguardam automaticamente.

### TF01 — Criar conta (Brian da Silva Guterres)

- Acessa o LocalEats e verifica o título `Entrar | Local Eats`.
- Interação: clica em **Criar Conta**, preenche nome, e-mail e senha e clica em **Registrar**.
- Assertions:
  1. a URL termina em `/index.html`;
  2. o badge do usuário (`#userBadge`) contém `Olá, Brian`;
  3. o título "Descubra sabores incríveis na sua cidade" está visível;
  4. ao menos um card de restaurante está visível.

### TF02 — Filtrar restaurantes por categoria, com BDD (Brian da Silva Guterres)

Cenário em Gherkin (`features/filtrar_categoria.feature`):

```gherkin
# language: pt
Funcionalidade: Filtrar restaurantes por categoria
  Como usuário do LocalEats
  Quero filtrar os restaurantes por categoria
  Para encontrar rapidamente o tipo de comida que desejo

  Cenário: Filtrar restaurantes da categoria Japonesa
    Dado que estou logado na página inicial do LocalEats
    Quando eu seleciono a categoria "Japonesa"
    Então todos os restaurantes exibidos devem ser da categoria "Japonesa"
    E nenhum restaurante da categoria "Italiana" deve ser exibido
```

Os passos são implementados com `pytest-bdd` em `tests/test_bdd_categoria.py`. Assertions: o botão "Japonesa" fica com a classe `active`; o primeiro card passa a conter "Japonesa"; a lista não está vazia e cada card exibido contém "Japonesa"; nenhum card contém "Italiana".

---

## 5. Explicação individual (Brian da Silva Guterres) — TF01

Escolhi explicar o TF01, `test_criar_conta_redireciona_para_pagina_inicial_com_saudacao`, porque ele testa um fluxo completo, do jeito que um usuário faria.

**O que o teste faz:**
1. Abre o LocalEats. Como não há ninguém logado, o site mostra a tela de login, e o teste confere que o título da aba é `Entrar | Local Eats`.
2. Clica na aba **Criar Conta**, preenche nome, e-mail e senha e clica em **Registrar**.
3. Verifica se o cadastro funcionou olhando o que aparece na tela: a URL muda para `index.html`, aparece "Olá, Brian" no canto da página, aparece o título "Descubra sabores incríveis na sua cidade" e a lista de restaurantes é exibida.

**Por que foi feito assim:**
- **E-mail diferente a cada execução:** a fixture `novo_usuario`, em `conftest.py`, gera o e-mail com `time.time_ns()`. Se o e-mail fosse fixo, o teste passaria só na primeira vez, porque na segunda o e-mail já estaria cadastrado. Assim cada execução é independente.
- **Locators pelo que o usuário vê:** usei `get_by_role("button", name="Criar Conta")` e `get_by_placeholder("Seu nome")` em vez de seletores CSS complicados. Se o layout mudar mas o botão continuar com o mesmo nome, o teste continua funcionando.
- **Sem `time.sleep`:** o `expect(...)` do Playwright espera sozinho, até 5 segundos, o resultado aparecer. Se aparecer antes, o teste segue na hora. Com `sleep`, o teste ficaria mais lento ou poderia falhar quando o site demorasse.

**Algo que aprendi com esse teste:** na primeira execução ele falhou, porque eu esperava "Olá, Brian Teste" e o site mostra só o primeiro nome ("Olá, Brian"). O problema não era o sistema, era a minha expectativa (ver seção 6).

---

## 6. Registro de falha encontrada e corrigida

Na primeira execução, o TF01 falhou:

```
AssertionError: Locator expected to contain text 'Olá, Brian Teste'
Actual value:  Olá, Brian
```

A análise mostrou que o LocalEats exibe **apenas o primeiro nome** do usuário na saudação. A falha estava na expectativa do teste, não no sistema. O teste foi corrigido para comparar com o primeiro nome (`novo_usuario["nome"].split()[0]`), e esse comportamento foi documentado no próprio código com um comentário.

---

## 7. Relatório da execução

O relatório foi gerado com:

```powershell
python -m pytest -v | Tee-Object -FilePath relatorio-pytest.txt
```

Resultado: **9 testes coletados, 9 aprovados, 0 reprovados**. O TU03 é parametrizado e aparece 4 vezes no relatório, uma para cada valor de borda. Ver `relatorio-pytest.txt`.

---

## 8. Uso de inteligência artificial

**Ferramenta utilizada:** Antigravity (assistente de programação com IA, no editor).

**Como a ferramenta foi utilizada:** a IA leu o enunciado da atividade e gerou a estrutura de pastas, o código da regra, os testes unitários, os testes funcionais e o rascunho deste Markdown. Ela também rodou scripts Playwright no LocalEats para descobrir os textos, placeholders e ids reais da interface (tela de login, formulário de registro, filtros de categoria e cards de restaurante), em vez de inventar seletores. O ciclo TDD foi executado passo a passo, rodando o pytest a cada etapa, e as saídas registradas na seção 3 são as reais.

**Uma sugestão que precisou ser alterada ou rejeitada:**
1. A primeira versão do TF01 esperava a saudação com o nome completo (`Olá, Brian Teste`). Quando o teste rodou, falhou, porque o site mostra só o primeiro nome. A assertion foi corrigida (ver seção 6).
2. Na revisão, uma assertion do TF02 que comparava a quantidade total de cards com a quantidade filtrada foi considerada fraca e trocada por uma verificação card a card.
3. O primeiro registro de TDD descrevia o ciclo de forma simplificada, diferente do que tinha sido executado. Ele foi refeito executando o ciclo de verdade, etapa por etapa.

**Como o código sugerido foi verificado:**
- execução de toda a suíte com `python -m pytest -v` (9 testes aprovados, ver `relatorio-pytest.txt`);
- execução do ciclo TDD com o pytest em cada etapa, confirmando as falhas e os acertos;
- conferência dos textos usados nos locators com a interface real do LocalEats;
- comparação da tabela de responsabilidades com as funções que aparecem no relatório.
