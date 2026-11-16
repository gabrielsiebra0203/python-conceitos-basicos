
from pydantic import BaseModel, Field
from typing import Literal


class PedidoWebhook(BaseModel):
    evento: Literal["pedido.criado"]

    pedido_id: str = Field(min_length=1)

    cliente: str = Field(min_length=2)

    produto: str = Field(min_length=2)

    quantidade: int = Field(gt=0)

    valor_unitario: float = Field(gt=0)
