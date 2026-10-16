from app.core import database as db
from app.core.errors import conflict, not_found
from app.core.schemas import PaginationParams, paginate
from app.ingrediente.schema import (
    IngredienteCreate,
    IngredientePaginatedResponse,
    IngredienteRead,
    IngredienteUpdate,
)

NOT_FOUND = "Ingrediente no encontrado"


def _to_read(row: db.IngredienteRow) -> IngredienteRead:
    return IngredienteRead.model_validate(row)


def _buscar(ingrediente_id: int, incluir_inactivos: bool = False) -> db.IngredienteRow:
    for row in db.ingredientes:
        if row.id == ingrediente_id and (incluir_inactivos or row.activo):
            return row
    raise not_found(NOT_FOUND)


def _validar_unidad(unidad_medida_id: int) -> None:
    if not any(u.id == unidad_medida_id for u in db.unidades_medida):
        raise not_found(f"Unidad de medida inexistente: {unidad_medida_id}")


def _validar_nombre_unico(nombre: str, excluir_id: int | None = None) -> None:
    # RN-10: nombre obligatorio y único (sin distinguir mayúsculas).
    objetivo = " ".join(nombre.split()).casefold()
    for row in db.ingredientes:
        if row.activo and row.id != excluir_id and " ".join(row.nombre.split()).casefold() == objetivo:
            raise conflict(f"Ya existe un ingrediente con el nombre '{row.nombre}'")


def listar(params: PaginationParams) -> IngredientePaginatedResponse:
    rows = [i for i in db.ingredientes if params.incluir_inactivos or i.activo]
    if params.nombre:
        filtro = params.nombre.casefold()
        rows = [i for i in rows if filtro in i.nombre.casefold()]
    page, total = paginate(rows, params)
    return IngredientePaginatedResponse(
        items=[_to_read(i) for i in page], total=total, offset=params.offset, limit=params.limit
    )


def obtener(ingrediente_id: int) -> IngredienteRead:
    return _to_read(_buscar(ingrediente_id))


def crear(data: IngredienteCreate) -> IngredienteRead:
    _validar_unidad(data.unidad_medida_id)
    _validar_nombre_unico(data.nombre)
    row = db.IngredienteRow(
        id=db.seq_ingrediente.next(),
        nombre=data.nombre,
        descripcion=data.descripcion,
        unidad_medida_id=data.unidad_medida_id,
    )
    db.ingredientes.append(row)
    return _to_read(row)


def actualizar(ingrediente_id: int, data: IngredienteUpdate) -> IngredienteRead:
    row = _buscar(ingrediente_id)
    _validar_unidad(data.unidad_medida_id)
    _validar_nombre_unico(data.nombre, excluir_id=ingrediente_id)
    row.nombre = data.nombre
    row.descripcion = data.descripcion
    row.unidad_medida_id = data.unidad_medida_id
    row.touch()
    return _to_read(row)


def eliminar(ingrediente_id: int) -> None:
    row = _buscar(ingrediente_id)
    row.soft_delete()
    db.producto_ingredientes[:] = [
        l for l in db.producto_ingredientes if l.ingrediente_id != ingrediente_id
    ]
