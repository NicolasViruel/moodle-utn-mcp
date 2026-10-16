from app.core import database as db
from app.core.errors import not_found
from app.unidad_medida.schema import UnidadMedidaListResponse, UnidadMedidaRead


def listar() -> UnidadMedidaListResponse:
    items = [UnidadMedidaRead.model_validate(u) for u in db.unidades_medida]
    return UnidadMedidaListResponse(items=items, total=len(items))


def obtener(unidad_id: int) -> UnidadMedidaRead:
    for u in db.unidades_medida:
        if u.id == unidad_id:
            return UnidadMedidaRead.model_validate(u)
    raise not_found("Unidad de medida no encontrada")
