from app.categoria.schema import (
    CategoriaCreate,
    CategoriaPaginatedResponse,
    CategoriaRead,
    CategoriaUpdate,
)
from app.core import database as db
from app.core.errors import conflict, not_found
from app.core.schemas import PaginationParams, paginate

NOT_FOUND = "Categoría no encontrada"


def _to_read(row: db.CategoriaRow) -> CategoriaRead:
    return CategoriaRead.model_validate(row)


def _normalizar(nombre: str) -> str:
    return " ".join(nombre.split()).casefold()


def _buscar(categoria_id: int, incluir_inactivos: bool = False) -> db.CategoriaRow:
    for row in db.categorias:
        if row.id == categoria_id and (incluir_inactivos or row.activo):
            return row
    raise not_found(NOT_FOUND)  # RN-04 / RN-10


def _validar_nombre_unico(nombre: str, excluir_id: int | None = None) -> None:
    # RN-02: unicidad sin distinguir mayúsculas ni espacios externos (solo activas).
    objetivo = _normalizar(nombre)
    for row in db.categorias:
        if row.activo and row.id != excluir_id and _normalizar(row.nombre) == objetivo:
            raise conflict(f"Ya existe una categoría con el nombre '{row.nombre}'")


def listar(params: PaginationParams) -> CategoriaPaginatedResponse:
    rows = [c for c in db.categorias if params.incluir_inactivos or c.activo]
    if params.nombre:
        filtro = params.nombre.casefold()
        rows = [c for c in rows if filtro in c.nombre.casefold()]
    page, total = paginate(rows, params)
    return CategoriaPaginatedResponse(
        items=[_to_read(c) for c in page], total=total, offset=params.offset, limit=params.limit
    )


def obtener(categoria_id: int) -> CategoriaRead:
    return _to_read(_buscar(categoria_id))


def crear(data: CategoriaCreate) -> CategoriaRead:
    _validar_nombre_unico(data.nombre)
    row = db.CategoriaRow(id=db.seq_categoria.next(), nombre=data.nombre, descripcion=data.descripcion)
    db.categorias.append(row)
    return _to_read(row)


def actualizar(categoria_id: int, data: CategoriaUpdate) -> CategoriaRead:
    row = _buscar(categoria_id)
    _validar_nombre_unico(data.nombre, excluir_id=categoria_id)
    row.nombre = data.nombre
    row.descripcion = data.descripcion
    row.touch()
    return _to_read(row)


def _productos_activos_asociados(categoria_id: int) -> int:
    activos = {p.id for p in db.productos if p.activo}
    return sum(
        1
        for link in db.producto_categorias
        if link.categoria_id == categoria_id and link.producto_id in activos
    )


def eliminar(categoria_id: int) -> None:
    row = _buscar(categoria_id)
    cantidad = _productos_activos_asociados(categoria_id)
    if cantidad:
        # RN-05: no se puede eliminar una categoría con productos asociados.
        raise conflict(
            f"La categoría tiene {cantidad} producto(s) asociado(s); desasocialos o eliminalos primero"
        )
    row.soft_delete()  # borrado lógico


def productos_de_categoria(categoria_id: int) -> list[db.ProductoRow]:
    """GET /categorias/{id}/productos (relación N:M, solo consulta)."""
    _buscar(categoria_id)
    ids = {link.producto_id for link in db.producto_categorias if link.categoria_id == categoria_id}
    return [p for p in db.productos if p.id in ids and p.activo]
