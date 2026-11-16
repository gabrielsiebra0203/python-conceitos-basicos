
import pytest
from fastapi.testclient import TestClient

from main import app, pedidos_processados


# Criando um cliente para testar nossa API
client = TestClient(app)


# Limpa os pedidos antes de cada teste
@pytest.fixture(autouse=True)
def limpar_pedidos():
    pedidos_processados.clear()
    yield
    pedidos_processados.clear()


# Teste 1: verificar se a API está funcionando
def test_inicio():
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "online"


# Teste 2: verificar se a lista começa vazia
def test_listar_pedidos_vazios():
    resposta = client.get("/pedidos")

    assert resposta.status_code == 200
    assert resposta.json()["total"] == 0


# Teste 3: enviar um pedido válido
def test_receber_webhook():
    dados = {
        "evento": "pedido.criado",
        "pedido_id": "PED001",
        "cliente": "Gabriel",
        "produto": "Bolsa feminina",
        "quantidade": 2,
        "valor_unitario": 89.90
    }

    resposta = client.post("/webhook", json=dados)

    assert resposta.status_code == 200
    assert resposta.json()["pedido"]["valor_total"] == 179.8


# Teste 4: verificar se a API rejeita quantidade zero
def test_webhook_quantidade_invalida():
    dados = {
        "evento": "pedido.criado",
        "pedido_id": "PED002",
        "cliente": "Gabriel",
        "produto": "Bolsa feminina",
        "quantidade": 0,
        "valor_unitario": 89.90
    }

    resposta = client.post("/webhook", json=dados)

    assert resposta.status_code == 422


# Teste 5: verificar se pedidos processados são armazenados
def test_consultar_pedidos_apos_webhook():
    dados = {
        "evento": "pedido.criado",
        "pedido_id": "PED003",
        "cliente": "Gabriel",
        "produto": "Bolsa feminina",
        "quantidade": 3,
        "valor_unitario": 50.00
    }

    client.post("/webhook", json=dados)

    resposta = client.get("/pedidos")

    assert resposta.status_code == 200
    assert resposta.json()["total"] == 1
    assert resposta.json()["pedidos"][0]["valor_total"] == 150.0
