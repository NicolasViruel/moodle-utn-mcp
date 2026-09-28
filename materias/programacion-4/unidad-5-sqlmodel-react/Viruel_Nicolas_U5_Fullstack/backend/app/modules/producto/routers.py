from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.database import get_session
from app.modules.producto import schemas
from app.modules.producto.services import ProductoService

router = APIRouter(prefix="/productos", tags=["Productos"])


def get_service(session: Session = Depends(get_session)) -> ProductoService:
    return ProductoService(session)


@router.post(
    "/",
    response_model=schemas.ProductoRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_producto(
    payload: schemas.ProductoCreate,
    service: ProductoService = Depends(get_service),
):
    return service.crear(payload)


@router.get("/", response_model=list[schemas.ProductoRead])
def listar_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    service: ProductoService = Depends(get_service),
):
    return service.listar(skip=skip, limit=limit)


@router.get("/{producto_id}", response_model=schemas.ProductoRead)
def detalle_producto(
    producto_id: int,
    service: ProductoService = Depends(get_service),
):
    return service.obtener(producto_id)


@router.put("/{producto_id}", response_model=schemas.ProductoRead)
def actualizar_producto(
    producto_id: int,
    payload: schemas.ProductoUpdate,
    service: ProductoService = Depends(get_service),
):
    return service.actualizar(producto_id, payload)


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(
    producto_id: int,
    service: ProductoService = Depends(get_service),
):
    service.eliminar(producto_id)
