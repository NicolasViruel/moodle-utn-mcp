"""Persistencia en memoria del módulo "Catálogo de Productos" (FOOD STORE).

Los datos viven mientras el servidor está en ejecución (RN-16). Todos los
modelos de negocio llevan campos de auditoría (created_at, updated_at,
deleted_at) y se eliminan de forma lógica (soft delete): nunca se borra una
fila físicamente.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal


def now() -> datetime:
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Models (filas de las tablas del UML)
# ---------------------------------------------------------------------------


@dataclass
class AuditMixin:
    created_at: datetime = field(default_factory=now)
    updated_at: datetime = field(default_factory=now)
    deleted_at: datetime | None = None

    @property
    def activo(self) -> bool:
        return self.deleted_at is None

    def touch(self) -> None:
        self.updated_at = now()

    def soft_delete(self) -> None:
        moment = now()
        self.deleted_at = moment
        self.updated_at = moment


@dataclass
class CategoriaRow(AuditMixin):
    id: int = 0
    nombre: str = ""
    descripcion: str = ""


@dataclass
class ProductoRow(AuditMixin):
    id: int = 0
    nombre: str = ""
    descripcion: str | None = None
    precio_base: Decimal = Decimal("0")
    imagenes_url: list[str] = field(default_factory=list)
    disponible: bool = True


@dataclass
class ProductoCategoriaRow:
    """«Link» ProductoCategoria — PK compuesta (producto_id, categoria_id)."""

    producto_id: int
    categoria_id: int
    es_principal: bool = False
    created_at: datetime = field(default_factory=now)


@dataclass
class IngredienteRow(AuditMixin):
    id: int = 0
    nombre: str = ""
    descripcion: str | None = None
    unidad_medida_id: int = 0


@dataclass
class ProductoIngredienteRow:
    """«Link» ProductoIngrediente — PK compuesta (producto_id, ingrediente_id)."""

    producto_id: int
    ingrediente_id: int
    cantidad: Decimal = Decimal("1")
    created_at: datetime = field(default_factory=now)


@dataclass
class UnidadMedidaRow:
    """«Catalog» UnidadMedida — solo lectura, se carga desde seed.py."""

    id: int
    nombre: str
    simbolo: str
    tipo: str


# ---------------------------------------------------------------------------
# "Tablas"
# ---------------------------------------------------------------------------

categorias: list[CategoriaRow] = []
productos: list[ProductoRow] = []
producto_categorias: list[ProductoCategoriaRow] = []
ingredientes: list[IngredienteRow] = []
producto_ingredientes: list[ProductoIngredienteRow] = []
unidades_medida: list[UnidadMedidaRow] = []


class _Sequence:
    """Emula un BIGSERIAL: ids autoincrementales asignados por el backend (RN-15)."""

    def __init__(self) -> None:
        self._value = 0

    def next(self) -> int:
        self._value += 1
        return self._value

    def reset(self) -> None:
        self._value = 0


seq_categoria = _Sequence()
seq_producto = _Sequence()
seq_ingrediente = _Sequence()


def reset() -> None:
    """Vacía todas las tablas (usado por el seed y por los tests)."""
    categorias.clear()
    productos.clear()
    producto_categorias.clear()
    ingredientes.clear()
    producto_ingredientes.clear()
    unidades_medida.clear()
    seq_categoria.reset()
    seq_producto.reset()
    seq_ingrediente.reset()
