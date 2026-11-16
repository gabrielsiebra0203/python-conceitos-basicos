
from fastapi import FastAPI
from schemas import PedidoWebhook
from services import processar_pedido


# Criando nossa aplicação
app = FastAPI(
    title="API de Webhooks",
    description="API para receber e processar pedidos",
    version="1.0.0"
)


# Lista para armazenar os pedidos processados
pedidos_processados = []


# Endpoint inicial
@app.get("/")
def inicio():
    return {
        "mensagem": "API de Webhooks funcionando!",
        "status": "online"
    }


# Endpoint para consultar pedidos
@app.get("/pedidos")
def listar_pedidos():
    return {
        "total": len(pedidos_processados),
        "pedidos": pedidos_processados
    }


# Endpoint para receber webhooks
@app.post("/webhook")
def receber_webhook(pedido: PedidoWebhook):

    resultado = processar_pedido(pedido)

    pedidos_processados.append(resultado)

    return {
        "mensagem": "Webhook recebido com sucesso!",
        "pedido": resultado
    }
