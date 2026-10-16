from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.core.schemas import AuditRead, PaginatedResponse


class DetallePedidoCreate(BaseModel):
    producto_id: int = Field(gt=0)
    cantidad: int = Field(ge=1, examples=[1])
    personalizacion: dict | None = None


class DetallePedidoRead(DetallePedidoCreate):
    nombre_producto_snap: str
    precio_unitario_snap: Decimal
    subtotal_snap: Decimal


class PedidoCreate(BaseModel):
    usuario_id: int = Field(gt=0)
    direccion_id: int | None = None
    estado_codigo: str = "PENDIENTE"
    forma_pago_codigo: str = Field(min_length=1, examples=["EFECTIVO"])
    descuento: Decimal = Field(default=Decimal("0"), ge=0)
    costo_envio: Decimal = Field(default=Decimal("0"), ge=0)
    notas: str | None = None
    # RN-12: al menos un detalle
    detalles: list[DetallePedidoCreate] = Field(min_length=1)

    @field_validator("detalles")
    @classmethod
    def al_menos_un_detalle(cls, value: list[DetallePedidoCreate]) -> list[DetallePedidoCreate]:
        if not value:
            raise ValueError("Un pedido debe tener al menos un DetallePedido")
        return value


class PedidoUpdate(BaseModel):
    """PUT: actualiza el estado del pedido."""

    estado_codigo: str = Field(min_length=1)


class PedidoRead(AuditRead):
    id: int
    usuario_id: int
    direccion_id: int | None
    estado_codigo: str
    forma_pago_codigo: str
    subtotal: Decimal
    descuento: Decimal
    costo_envio: Decimal
    total: Decimal
    notas: str | None
    detalles: list[DetallePedidoRead]


class PedidoPaginatedResponse(PaginatedResponse[PedidoRead]):
    pass
