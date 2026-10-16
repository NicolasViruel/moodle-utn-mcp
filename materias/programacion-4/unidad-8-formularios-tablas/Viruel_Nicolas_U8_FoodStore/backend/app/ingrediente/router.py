from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.schemas import PaginationParams, pagination_params
from app.ingrediente import schema, service

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

Pagination = Annotated[PaginationParams, Depends(pagination_params)]


@router.get("/", response_model=schema.IngredientePaginatedResponse)
def listar_ingredientes(params: Pagination):
    return service.listar(params)


@router.post("/", response_model=schema.IngredienteRead, status_code=status.HTTP_201_CREATED)
def crear_ingrediente(body: schema.IngredienteCreate):
    return service.crear(body)


@router.get("/{ingrediente_id}", response_model=schema.IngredienteRead, responses={404: {}})
def detalle_ingrediente(ingrediente_id: int):
    return service.obtener(ingrediente_id)


@router.put("/{ingrediente_id}", response_model=schema.IngredienteRead, responses={404: {}})
def actualizar_ingrediente(ingrediente_id: int, body: schema.IngredienteUpdate):
    return service.actualizar(ingrediente_id, body)


@router.delete("/{ingrediente_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {}})
def eliminar_ingrediente(ingrediente_id: int) -> None:
    service.eliminar(ingrediente_id)
