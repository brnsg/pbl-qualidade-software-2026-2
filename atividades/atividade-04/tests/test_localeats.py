# Responsável: Brian da Silva Guterres
import re

from playwright.sync_api import Page, expect

from tests.conftest import BASE_URL


# Responsável: Brian da Silva Guterres
# TF01 - Criar uma conta e verificar a página inicial do usuário
def test_criar_conta_redireciona_para_pagina_inicial_com_saudacao(page: Page, novo_usuario):
    # Acessa o LocalEats (sem sessão, o sistema exibe a tela de login)
    page.goto(BASE_URL)
    expect(page).to_have_title("Entrar | Local Eats")

    # Interação: abre o formulário de registro e cria a conta
    page.get_by_role("button", name="Criar Conta").click()
    page.get_by_placeholder("Seu nome").fill(novo_usuario["nome"])
    page.get_by_placeholder("novo@teste.com").fill(novo_usuario["email"])
    page.get_by_placeholder("Min. 3 caracteres").fill(novo_usuario["senha"])
    page.get_by_role("button", name="Registrar").click()

    # Assertions sobre resultados observáveis
    expect(page).to_have_url(re.compile(r"/index\.html$"))
    # O LocalEats exibe apenas o primeiro nome na saudação
    primeiro_nome = novo_usuario["nome"].split()[0]
    expect(page.locator("#userBadge")).to_contain_text(f"Olá, {primeiro_nome}")
    expect(page.get_by_role("heading", name="Descubra sabores incríveis na sua cidade")).to_be_visible()
    expect(page.locator(".rest-card").first).to_be_visible()
