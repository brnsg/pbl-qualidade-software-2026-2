# Responsável: Brian da Silva Guterres
import re

from playwright.sync_api import Page, expect
from pytest_bdd import given, parsers, scenario, then, when

from tests.conftest import BASE_URL


# Responsável: Brian da Silva Guterres
# TF02 - Cenário BDD: filtrar restaurantes por categoria
@scenario("filtrar_categoria.feature", "Filtrar restaurantes da categoria Japonesa")
def test_filtrar_restaurantes_por_categoria():
    pass


@given("que estou logado na página inicial do LocalEats")
def usuario_logado(page: Page, novo_usuario):
    page.goto(BASE_URL)
    page.get_by_role("button", name="Criar Conta").click()
    page.get_by_placeholder("Seu nome").fill(novo_usuario["nome"])
    page.get_by_placeholder("novo@teste.com").fill(novo_usuario["email"])
    page.get_by_placeholder("Min. 3 caracteres").fill(novo_usuario["senha"])
    page.get_by_role("button", name="Registrar").click()
    expect(page).to_have_url(re.compile(r"/index\.html$"))
    expect(page.locator(".rest-card").first).to_be_visible()


@when(parsers.parse('eu seleciono a categoria "{categoria}"'))
def selecionar_categoria(page: Page, categoria):
    page.get_by_role("button", name=categoria, exact=True).click()
    expect(page.get_by_role("button", name=categoria, exact=True)).to_have_class(re.compile(r"\bactive\b"))


@then(parsers.parse('todos os restaurantes exibidos devem ser da categoria "{categoria}"'))
def restaurantes_da_categoria(page: Page, categoria):
    cards = page.locator(".rest-card")
    # O primeiro card passa a ser da categoria escolhida (aguarda a atualização da lista)
    expect(cards.first).to_contain_text(categoria)
    # Rola a página até os restaurantes filtrados, como um usuário faria para vê-los
    cards.first.scroll_into_view_if_needed()
    expect(cards.first).to_be_in_viewport()
    # A lista não está vazia e cada card exibido pertence à categoria
    assert cards.count() > 0
    for card in cards.all():
        expect(card).to_contain_text(categoria)


@then(parsers.parse('nenhum restaurante da categoria "{categoria}" deve ser exibido'))
def nenhum_restaurante_da_categoria(page: Page, categoria):
    expect(page.locator(".rest-card", has_text=categoria)).to_have_count(0)
