"""UoW del módulo Pedido: transacción atómica pedido + detalles."""

from app.core.unit_of_work import UnitOfWork
from app.pedido.repository import DetallePedidoRepository, PedidoRepository


class PedidoUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        super().__init__()
        self.pedidos = PedidoRepository()
        self.detalles = DetallePedidoRepository()
