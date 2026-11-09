import time

import pytest

BASE_URL = "https://local-eats-unisenac.vercel.app/"


@pytest.fixture
def novo_usuario():
    """Gera dados únicos para cada execução, mantendo os testes independentes."""
    sufixo = time.time_ns()
    return {
        "nome": "Brian Teste",
        "email": f"brian.{sufixo}@teste.com",
        "senha": "abc123",
    }
