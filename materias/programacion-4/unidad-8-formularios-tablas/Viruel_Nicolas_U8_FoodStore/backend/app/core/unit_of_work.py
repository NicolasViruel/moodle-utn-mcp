"""Unit of Work: snapshot de las tablas, commit o rollback atómico."""

from __future__ import annotations

from copy import deepcopy

from app.core import database as db
from app.core.repository import InMemoryRepository


class UnitOfWork:
    """Envuelve una operación de escritura. Si no hay commit, restaura el estado."""

    def __init__(self) -> None:
        self._snapshot: dict[str, object] | None = None
        self._committed = False
        self.categorias = InMemoryRepository(db.categorias)
        self.productos = InMemoryRepository(db.productos)
        self.producto_categorias = InMemoryRepository(db.producto_categorias, id_attr="producto_id")
        self.ingredientes = InMemoryRepository(db.ingredientes)
        self.producto_ingredientes = InMemoryRepository(db.producto_ingredientes, id_attr="producto_id")
        self.unidades_medida = InMemoryRepository(db.unidades_medida)
        self.usuarios = InMemoryRepository(db.usuarios)
        self.formas_pago = InMemoryRepository(db.formas_pago, id_attr="codigo")
        self.estados_pedido = InMemoryRepository(db.estados_pedido, id_attr="codigo")
        self.pedidos = InMemoryRepository(db.pedidos)
        self.detalle_pedidos = InMemoryRepository(db.detalle_pedidos, id_attr="pedido_id")

    def __enter__(self) -> UnitOfWork:
        self._snapshot = {
            "categorias": deepcopy(db.categorias),
            "productos": deepcopy(db.productos),
            "producto_categorias": deepcopy(db.producto_categorias),
            "ingredientes": deepcopy(db.ingredientes),
            "producto_ingredientes": deepcopy(db.producto_ingredientes),
            "unidades_medida": deepcopy(db.unidades_medida),
            "usuarios": deepcopy(db.usuarios),
            "formas_pago": deepcopy(db.formas_pago),
            "estados_pedido": deepcopy(db.estados_pedido),
            "pedidos": deepcopy(db.pedidos),
            "detalle_pedidos": deepcopy(db.detalle_pedidos),
            "seq_categoria": db.seq_categoria._value,
            "seq_producto": db.seq_producto._value,
            "seq_ingrediente": db.seq_ingrediente._value,
            "seq_pedido": db.seq_pedido._value,
            "seq_usuario": db.seq_usuario._value,
        }
        self._committed = False
        return self

    def commit(self) -> None:
        self._committed = True

    def rollback(self) -> None:
        if self._snapshot is None:
            return
        db.categorias[:] = self._snapshot["categorias"]  # type: ignore[index]
        db.productos[:] = self._snapshot["productos"]  # type: ignore[index]
        db.producto_categorias[:] = self._snapshot["producto_categorias"]  # type: ignore[index]
        db.ingredientes[:] = self._snapshot["ingredientes"]  # type: ignore[index]
        db.producto_ingredientes[:] = self._snapshot["producto_ingredientes"]  # type: ignore[index]
        db.unidades_medida[:] = self._snapshot["unidades_medida"]  # type: ignore[index]
        db.usuarios[:] = self._snapshot["usuarios"]  # type: ignore[index]
        db.formas_pago[:] = self._snapshot["formas_pago"]  # type: ignore[index]
        db.estados_pedido[:] = self._snapshot["estados_pedido"]  # type: ignore[index]
        db.pedidos[:] = self._snapshot["pedidos"]  # type: ignore[index]
        db.detalle_pedidos[:] = self._snapshot["detalle_pedidos"]  # type: ignore[index]
        db.seq_categoria._value = self._snapshot["seq_categoria"]  # type: ignore[index]
        db.seq_producto._value = self._snapshot["seq_producto"]  # type: ignore[index]
        db.seq_ingrediente._value = self._snapshot["seq_ingrediente"]  # type: ignore[index]
        db.seq_pedido._value = self._snapshot["seq_pedido"]  # type: ignore[index]
        db.seq_usuario._value = self._snapshot["seq_usuario"]  # type: ignore[index]

    def __exit__(self, exc_type, exc, tb) -> None:
        if exc_type is not None or not self._committed:
            self.rollback()
        self._snapshot = None
