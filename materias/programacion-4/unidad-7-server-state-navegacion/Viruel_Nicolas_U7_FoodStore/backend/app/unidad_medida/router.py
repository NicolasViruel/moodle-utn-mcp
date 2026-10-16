from fastapi import APIRouter

from app.unidad_medida import schema, service

router = APIRouter(prefix="/unidades-medida", tags=["Unidades de Medida (catálogo)"])


@router.get("/", response_model=schema.UnidadMedidaListResponse)
def listar_unidades():
    return service.listar()


@router.get("/{unidad_id}", response_model=schema.UnidadMedidaRead, responses={404: {}})
def detalle_unidad(unidad_id: int):
    return service.obtener(unidad_id)
