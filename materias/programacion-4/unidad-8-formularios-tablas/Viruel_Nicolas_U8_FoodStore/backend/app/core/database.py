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


@dataclass
class UsuarioRow(AuditMixin):
    id: int = 0
    nombre: str = ""
    apellido: str = ""
    email: str = ""


@dataclass
class FormaPagoRow:
    """«Catalog» FormaPago — solo lectura."""

    codigo: str
    descripcion: str
    activo: bool = True


@dataclass
class EstadoPedidoRow:
    """«Catalog» EstadoPedido — solo lectura."""

    codigo: str
    descripcion: str
    orden: int
    es_terminal: bool


@dataclass
class PedidoRow(AuditMixin):
    id: int = 0
    usuario_id: int = 0
    direccion_id: int | None = None
    estado_codigo: str = "PENDIENTE"
    forma_pago_codigo: str = "EFECTIVO"
    subtotal: Decimal = Decimal("0")
    descuento: Decimal = Decimal("0")
    costo_envio: Decimal = Decimal("0")
    total: Decimal = Decimal("0")
    notas: str | None = None


@dataclass
class DetallePedidoRow:
    pedido_id: int
    producto_id: int
    cantidad: int = 1
    nombre_producto_snap: str = ""
    precio_unitario_snap: Decimal = Decimal("0")
    subtotal_snap: Decimal = Decimal("0")
    personalizacion: dict | None = None
    created_at: datetime = field(default_factory=now)


# ---------------------------------------------------------------------------
# "Tablas"
# ---------------------------------------------------------------------------

categorias: list[CategoriaRow] = []
productos: list[ProductoRow] = []
producto_categorias: list[ProductoCategoriaRow] = []
ingredientes: list[IngredienteRow] = []
producto_ingredientes: list[ProductoIngredienteRow] = []
unidades_medida: list[UnidadMedidaRow] = []
usuarios: list[UsuarioRow] = []
formas_pago: list[FormaPagoRow] = []
estados_pedido: list[EstadoPedidoRow] = []
pedidos: list[PedidoRow] = []
detalle_pedidos: list[DetallePedidoRow] = []


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
seq_pedido = _Sequence()
seq_usuario = _Sequence()


def reset() -> None:
    """Vacía todas las tablas (usado por el seed y por los tests)."""
    categorias.clear()
    productos.clear()
    producto_categorias.clear()
    ingredientes.clear()
    producto_ingredientes.clear()
    unidades_medida.clear()
    usuarios.clear()
    formas_pago.clear()
    estados_pedido.clear()
    pedidos.clear()
    detalle_pedidos.clear()
    seq_categoria.reset()
    seq_producto.reset()
    seq_ingrediente.reset()
    seq_pedido.reset()
    seq_usuario.reset()
