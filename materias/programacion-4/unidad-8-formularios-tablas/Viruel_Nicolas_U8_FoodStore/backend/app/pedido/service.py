from decimal import Decimal

from app.core import database as db
from app.core.errors import not_found
from app.core.schemas import PaginationParams, paginate
from app.pedido.schema import (
    DetallePedidoRead,
    PedidoCreate,
    PedidoPaginatedResponse,
    PedidoRead,
    PedidoUpdate,
)
from app.pedido.unit_of_work import PedidoUnitOfWork

NOT_FOUND = "Pedido no encontrado"


def _detalles_read(pedido_id: int) -> list[DetallePedidoRead]:
    return [
        DetallePedidoRead(
            producto_id=d.producto_id,
            cantidad=d.cantidad,
            personalizacion=d.personalizacion,
            nombre_producto_snap=d.nombre_producto_snap,
            precio_unitario_snap=d.precio_unitario_snap,
            subtotal_snap=d.subtotal_snap,
        )
        for d in db.detalle_pedidos
        if d.pedido_id == pedido_id
    ]


def _to_read(row: db.PedidoRow) -> PedidoRead:
    return PedidoRead(
        id=row.id,
        usuario_id=row.usuario_id,
        direccion_id=row.direccion_id,
        estado_codigo=row.estado_codigo,
        forma_pago_codigo=row.forma_pago_codigo,
        subtotal=row.subtotal,
        descuento=row.descuento,
        costo_envio=row.costo_envio,
        total=row.total,
        notas=row.notas,
        created_at=row.created_at,
        updated_at=row.updated_at,
        deleted_at=row.deleted_at,
        detalles=_detalles_read(row.id),
    )


def _producto_activo(producto_id: int) -> db.ProductoRow:
    for p in db.productos:
        if p.id == producto_id and p.activo:
            return p
    raise not_found(f"Producto inexistente: {producto_id}")


def _validar_catalogos(usuario_id: int, estado: str, forma_pago: str) -> None:
    if not any(u.id == usuario_id and u.activo for u in db.usuarios):
        raise not_found(f"Usuario inexistente: {usuario_id}")
    if not any(e.codigo == estado for e in db.estados_pedido):
        raise not_found(f"Estado de pedido inexistente: {estado}")
    if not any(f.codigo == forma_pago and f.activo for f in db.formas_pago):
        raise not_found(f"Forma de pago inexistente: {forma_pago}")


def listar(params: PaginationParams) -> PedidoPaginatedResponse:
    rows = [p for p in db.pedidos if params.incluir_inactivos or p.activo]
    page, total = paginate(rows, params)
    return PedidoPaginatedResponse(
        items=[_to_read(p) for p in page], total=total, offset=params.offset, limit=params.limit
    )


def obtener(pedido_id: int) -> PedidoRead:
    for row in db.pedidos:
        if row.id == pedido_id and row.activo:
            return _to_read(row)
    raise not_found(NOT_FOUND)


def crear(data: PedidoCreate) -> PedidoRead:
    with PedidoUnitOfWork() as uow:
        _validar_catalogos(data.usuario_id, data.estado_codigo, data.forma_pago_codigo)
        lineas: list[db.DetallePedidoRow] = []
        subtotal = Decimal("0")
        for det in data.detalles:
            producto = _producto_activo(det.producto_id)
            linea_sub = producto.precio_base * det.cantidad
            subtotal += linea_sub
            lineas.append(
                db.DetallePedidoRow(
                    pedido_id=0,
                    producto_id=producto.id,
                    cantidad=det.cantidad,
                    nombre_producto_snap=producto.nombre,
                    precio_unitario_snap=producto.precio_base,
                    subtotal_snap=linea_sub,
                    personalizacion=det.personalizacion,
                )
            )
        total = subtotal - data.descuento + data.costo_envio
        if total < 0:
            total = Decimal("0")
        pedido = db.PedidoRow(
            id=db.seq_pedido.next(),
            usuario_id=data.usuario_id,
            direccion_id=data.direccion_id,
            estado_codigo=data.estado_codigo,
            forma_pago_codigo=data.forma_pago_codigo,
            subtotal=subtotal,
            descuento=data.descuento,
            costo_envio=data.costo_envio,
            total=total,
            notas=data.notas,
        )
        uow.pedidos.add(pedido)
        for linea in lineas:
            linea.pedido_id = pedido.id
            uow.detalles.add(linea)
        uow.commit()
        return _to_read(pedido)


def actualizar(pedido_id: int, data: PedidoUpdate) -> PedidoRead:
    with PedidoUnitOfWork() as uow:
        row = uow.pedidos.get(pedido_id)
        if row is None or not row.activo:
            raise not_found(NOT_FOUND)
        if not any(e.codigo == data.estado_codigo for e in db.estados_pedido):
            raise not_found(f"Estado de pedido inexistente: {data.estado_codigo}")
        row.estado_codigo = data.estado_codigo
        row.touch()
        uow.commit()
        return _to_read(row)


def eliminar(pedido_id: int) -> None:
    with PedidoUnitOfWork() as uow:
        row = uow.pedidos.get(pedido_id)
        if row is None or not row.activo:
            raise not_found(NOT_FOUND)
        row.soft_delete()
        uow.detalles.delete_by_pedido(pedido_id)
        uow.commit()
