"""Repositorios del módulo Pedido (acceso a datos, sin reglas de negocio)."""

from app.core import database as db
from app.core.repository import InMemoryRepository


class PedidoRepository(InMemoryRepository[db.PedidoRow]):
    def __init__(self) -> None:
        super().__init__(db.pedidos)


class DetallePedidoRepository(InMemoryRepository[db.DetallePedidoRow]):
    def __init__(self) -> None:
        super().__init__(db.detalle_pedidos, id_attr="pedido_id")

    def list_by_pedido(self, pedido_id: int) -> list[db.DetallePedidoRow]:
        return [d for d in self._store if d.pedido_id == pedido_id]

    def delete_by_pedido(self, pedido_id: int) -> None:
        self.replace_where(lambda d: d.pedido_id != pedido_id)
