from app.core import database as db
from app.core.errors import not_found
from app.core.schemas import PaginationParams, paginate
from app.producto.schema import (
    ProductoCreate,
    ProductoIngredienteInput,
    ProductoIngredienteRead,
    ProductoPaginatedResponse,
    ProductoRead,
    ProductoUpdate,
)

NOT_FOUND = "Producto no encontrado"


# ---------------------------------------------------------------------------
# Mapeo
# ---------------------------------------------------------------------------


def _categoria_ids(producto_id: int) -> list[int]:
    return [l.categoria_id for l in db.producto_categorias if l.producto_id == producto_id]


def _ingredientes(producto_id: int) -> list[ProductoIngredienteRead]:
    return [
        ProductoIngredienteRead(ingrediente_id=l.ingrediente_id, cantidad=l.cantidad)
        for l in db.producto_ingredientes
        if l.producto_id == producto_id
    ]


def to_read(row: db.ProductoRow) -> ProductoRead:
    return ProductoRead(
        id=row.id,
        nombre=row.nombre,
        descripcion=row.descripcion,
        precio_base=row.precio_base,
        imagenes_url=list(row.imagenes_url),
        disponible=row.disponible,
        created_at=row.created_at,
        updated_at=row.updated_at,
        deleted_at=row.deleted_at,
        categoria_ids=_categoria_ids(row.id),
        ingredientes=_ingredientes(row.id),
    )


# ---------------------------------------------------------------------------
# Búsquedas / validaciones de integridad referencial
# ---------------------------------------------------------------------------


def _buscar(producto_id: int, incluir_inactivos: bool = False) -> db.ProductoRow:
    for row in db.productos:
        if row.id == producto_id and (incluir_inactivos or row.activo):
            return row
    raise not_found(NOT_FOUND)  # RN-10


def _validar_categorias(categoria_ids: list[int]) -> None:
    # RN-11: todas las categorías deben existir (y estar activas).
    activas = {c.id for c in db.categorias if c.activo}
    faltantes = [cid for cid in categoria_ids if cid not in activas]
    if faltantes:
        raise not_found(f"Categoría(s) inexistente(s): {faltantes}")


def _validar_ingredientes(items: list[ProductoIngredienteInput]) -> None:
    activos = {i.id for i in db.ingredientes if i.activo}
    faltantes = [it.ingrediente_id for it in items if it.ingrediente_id not in activos]
    if faltantes:
        raise not_found(f"Ingrediente(s) inexistente(s): {faltantes}")
    ids = [it.ingrediente_id for it in items]
    if len(ids) != len(set(ids)):
        raise not_found("Hay ingredientes repetidos en la solicitud")


def _reemplazar_categorias(producto_id: int, categoria_ids: list[int]) -> None:
    # RN-12: reemplazo total de las asociaciones.
    db.producto_categorias[:] = [l for l in db.producto_categorias if l.producto_id != producto_id]
    for index, cid in enumerate(categoria_ids):
        db.producto_categorias.append(
            db.ProductoCategoriaRow(producto_id=producto_id, categoria_id=cid, es_principal=index == 0)
        )


def _reemplazar_ingredientes(producto_id: int, items: list[ProductoIngredienteInput]) -> None:
    # RN-21: reemplazo total.
    db.producto_ingredientes[:] = [l for l in db.producto_ingredientes if l.producto_id != producto_id]
    for it in items:
        db.producto_ingredientes.append(
            db.ProductoIngredienteRow(producto_id=producto_id, ingrediente_id=it.ingrediente_id, cantidad=it.cantidad)
        )


# ---------------------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------------------


def listar(params: PaginationParams) -> ProductoPaginatedResponse:
    rows = [p for p in db.productos if params.incluir_inactivos or p.activo]
    if params.nombre:
        filtro = params.nombre.casefold()
        rows = [p for p in rows if filtro in p.nombre.casefold()]
    page, total = paginate(rows, params)
    return ProductoPaginatedResponse(
        items=[to_read(p) for p in page], total=total, offset=params.offset, limit=params.limit
    )


def obtener(producto_id: int) -> ProductoRead:
    return to_read(_buscar(producto_id))


def crear(data: ProductoCreate) -> ProductoRead:
    # RN-17: validar todo ANTES de modificar el catálogo.
    _validar_categorias(data.categoria_ids)
    _validar_ingredientes(data.ingredientes)
    row = db.ProductoRow(
        id=db.seq_producto.next(),
        nombre=data.nombre,
        descripcion=data.descripcion,
        precio_base=data.precio_base,
        imagenes_url=list(data.imagenes_url),
        disponible=data.disponible,
    )
    db.productos.append(row)
    _reemplazar_categorias(row.id, data.categoria_ids)
    _reemplazar_ingredientes(row.id, data.ingredientes)
    return to_read(row)


def actualizar(producto_id: int, data: ProductoUpdate) -> ProductoRead:
    row = _buscar(producto_id)
    if data.categoria_ids is not None:
        _validar_categorias(data.categoria_ids)
    if data.ingredientes is not None:
        _validar_ingredientes(data.ingredientes)

    row.nombre = data.nombre
    row.descripcion = data.descripcion
    row.precio_base = data.precio_base
    row.imagenes_url = list(data.imagenes_url)
    row.disponible = data.disponible
    row.touch()
    if data.categoria_ids is not None:
        _reemplazar_categorias(producto_id, data.categoria_ids)
    if data.ingredientes is not None:
        _reemplazar_ingredientes(producto_id, data.ingredientes)
    return to_read(row)


def eliminar(producto_id: int) -> None:
    row = _buscar(producto_id)
    row.soft_delete()
    # RN-14: en cascada se eliminan sus asociaciones.
    db.producto_categorias[:] = [l for l in db.producto_categorias if l.producto_id != producto_id]
    db.producto_ingredientes[:] = [l for l in db.producto_ingredientes if l.producto_id != producto_id]


# ---------------------------------------------------------------------------
# Relaciones N:M (solo consulta)
# ---------------------------------------------------------------------------


def categorias_de_producto(producto_id: int) -> list[db.CategoriaRow]:
    _buscar(producto_id)
    ids = set(_categoria_ids(producto_id))
    return [c for c in db.categorias if c.id in ids and c.activo]


def ingredientes_de_producto(producto_id: int) -> list[tuple[db.IngredienteRow, db.ProductoIngredienteRow]]:
    _buscar(producto_id)
    links = {l.ingrediente_id: l for l in db.producto_ingredientes if l.producto_id == producto_id}
    return [(i, links[i.id]) for i in db.ingredientes if i.id in links and i.activo]
