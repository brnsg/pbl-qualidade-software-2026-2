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

**Regra escolhida:** Regra 1 — verificar valor mínimo do pedido (`pedido_atingiu_valor_minimo(valor_pedido)`): pedidos de R$ 30,00 ou mais retornam `True`; abaixo de R$ 30,00 retornam `False`; valores negativos geram `ValueError`.

**Primeiro teste escrito:** `test_pedido_acima_do_minimo_retorna_true` — verifica que `pedido_atingiu_valor_minimo(50)` retorna `True`.

**Por que o teste falhou inicialmente:** o módulo `src/regras_localeats.py` e a função ainda não existiam. O pytest falhou na coleta com `ModuleNotFoundError: No module named 'src.regras_localeats'` (fase Red).

**Implementação mínima realizada:** criação do arquivo `src/regras_localeats.py` com a função `pedido_atingiu_valor_minimo` retornando a comparação `valor_pedido >= VALOR_MINIMO_PEDIDO`, o suficiente para o primeiro teste passar (fase Green).

**Segundo teste escrito:** `test_pedido_abaixo_do_minimo_retorna_false`, que verifica que `pedido_atingiu_valor_minimo(20)` retorna `False`. Também foram escritos o teste de limite (`30` deve retornar `True` e `29.99` deve retornar `False`) e o teste de valor negativo com `pytest.raises(ValueError)`, que exige a validação `if valor_pedido < 0: raise ValueError(...)`.

**Melhoria ou refatoração realizada:** o valor `30` fica na constante `VALOR_MINIMO_PEDIDO = 30.00` (evita número mágico), a função tem uma docstring explicando a regra e os casos de borda foram agrupados em um único teste com `@pytest.mark.parametrize`, evitando testes duplicados.

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

O teste `test_criar_conta_redireciona_para_pagina_inicial_com_saudacao` valida o fluxo de criação de conta de ponta a ponta pela interface. Ele usa a fixture `page` do `pytest-playwright` para abrir o navegador e a fixture `novo_usuario` para gerar um e-mail único com `time.time_ns()`. Sem isso, a segunda execução falharia porque o e-mail já estaria cadastrado, ou seja, o teste dependeria de execuções anteriores.

Os elementos são localizados com locators orientados ao usuário: `get_by_role("button", name="Criar Conta")` e `get_by_placeholder(...)`. Esses locators são mais estáveis que seletores CSS baseados em layout. Depois do clique em **Registrar**, as assertions `expect(page).to_have_url(...)` e `expect(locator).to_contain_text(...)` esperam automaticamente até 5 segundos pelo resultado. Por isso não é necessário usar `time.sleep`, e o teste verifica resultados que o usuário realmente vê: a mudança de página, a saudação com o nome e a lista de restaurantes.

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

**Ferramenta utilizada:** Antigravity (assistente de programação com IA).

**Como a ferramenta foi utilizada:** apoio para organizar a estrutura de pastas, escrever o rascunho dos testes unitários, explorar a interface do LocalEats com scripts Playwright (para descobrir textos, placeholders e ids reais) e escrever os passos do pytest-bdd.

**Uma sugestão que precisou ser alterada ou rejeitada:** a primeira versão do TF01 gerada pela IA esperava a saudação com o nome completo (`Olá, Brian Teste`). A execução mostrou que o sistema exibe só o primeiro nome, e a assertion foi alterada. Na revisão, uma assertion do TF02 que comparava a contagem total de cards com a contagem filtrada também foi substituída por uma verificação card a card, que é mais clara.

**Como o código sugerido foi verificado:** executando os testes unitários antes da implementação (falha confirmada), executando toda a suíte com `python -m pytest -v`, conferindo no site os textos usados nos locators e comparando a tabela de responsabilidades com as funções presentes no relatório.
