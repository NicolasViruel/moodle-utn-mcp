from typing import List, Optional

from fastapi import APIRouter, HTTPException, Path, Query, status

from . import schemas, services

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


@router.post(
    "/",
    response_model=schemas.ProveedorRead,
    status_code=status.HTTP_201_CREATED,
)
def alta_proveedor(proveedor: schemas.ProveedorCreate):
    try:
        return services.crear(proveedor)
    except ValueError as exc:
        if str(exc) == "codigo_duplicado":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un proveedor con ese codigo",
            ) from exc
        raise


@router.get(
    "/",
    response_model=List[schemas.ProveedorRead],
    status_code=status.HTTP_200_OK,
)
def listar_proveedores(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    activo: Optional[bool] = Query(None),
):
    return services.obtener_todos(skip=skip, limit=limit, activo=activo)


@router.get(
    "/{id}",
    response_model=schemas.ProveedorRead,
    status_code=status.HTTP_200_OK,
)
def detalle_proveedor(id: int = Path(..., gt=0)):
    proveedor = services.obtener_por_id(id)
    if not proveedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado",
        )
    return proveedor


@router.put(
    "/{id}",
    response_model=schemas.ProveedorRead,
    status_code=status.HTTP_200_OK,
)
def actualizar_proveedor(
    proveedor: schemas.ProveedorCreate,
    id: int = Path(..., gt=0),
):
    try:
        actualizado = services.actualizar_total(id, proveedor)
    except ValueError as exc:
        if str(exc) == "codigo_duplicado":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un proveedor con ese codigo",
            ) from exc
        raise
    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado",
        )
    return actualizado


@router.put(
    "/{id}/desactivar",
    response_model=schemas.ProveedorRead,
    status_code=status.HTTP_200_OK,
)
def desactivar_proveedor(id: int = Path(..., gt=0)):
    try:
        desactivado = services.desactivar(id)
    except ValueError as exc:
        if str(exc) == "ya_desactivado":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El proveedor ya esta desactivado",
            ) from exc
        raise
    if not desactivado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proveedor no encontrado",
        )
    return desactivado
