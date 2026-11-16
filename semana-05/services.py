
from schemas import PedidoWebhook


def processar_pedido(pedido: PedidoWebhook) -> dict:
    """
    Recebe um pedido validado e processa suas informações.
    """

    valor_total = pedido.quantidade * pedido.valor_unitario

    resultado = {
        "status": "processado",
        "pedido_id": pedido.pedido_id,
        "cliente": pedido.cliente,
        "produto": pedido.produto,
        "quantidade": pedido.quantidade,
        "valor_unitario": pedido.valor_unitario,
        "valor_total": round(valor_total, 2),
        "mensagem": "Pedido processado com sucesso!"
    }

    return resultado
