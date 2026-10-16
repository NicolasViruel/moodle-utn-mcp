from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.categoria.schema import CategoriaRead
from app.core.schemas import PaginationParams, pagination_params
from app.ingrediente.schema import IngredienteDeProductoRead
from app.producto import schema, service

router = APIRouter(prefix="/productos", tags=["Productos"])

Pagination = Annotated[PaginationParams, Depends(pagination_params)]


@router.get("/", response_model=schema.ProductoPaginatedResponse, summary="Listar productos (paginado)")
def listar_productos(params: Pagination):
    return service.listar(params)


@router.post(
    "/",
    response_model=schema.ProductoRead,
    status_code=status.HTTP_201_CREATED,
    responses={404: {"description": "Categoría/ingrediente inexistente (RN-11)"}, 422: {}},
)
def crear_producto(body: schema.ProductoCreate):
    return service.crear(body)


@router.get("/{producto_id}", response_model=schema.ProductoRead, responses={404: {}})
def detalle_producto(producto_id: int):
    return service.obtener(producto_id)


@router.put("/{producto_id}", response_model=schema.ProductoRead, responses={404: {}})
def actualizar_producto(producto_id: int, body: schema.ProductoUpdate):
    return service.actualizar(producto_id, body)


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {}})
def eliminar_producto(producto_id: int) -> None:
    service.eliminar(producto_id)


@router.get(
    "/{producto_id}/categorias",
    response_model=list[CategoriaRead],
    summary="Categorías de un producto (N:M, solo consulta)",
    responses={404: {}},
)
def categorias_de_producto(producto_id: int):
    return [CategoriaRead.model_validate(c) for c in service.categorias_de_producto(producto_id)]


@router.get(
    "/{producto_id}/ingredientes",
    response_model=list[IngredienteDeProductoRead],
    summary="Ingredientes de un producto con su cantidad (N:M, solo consulta)",
    responses={404: {}},
)
def ingredientes_de_producto(producto_id: int):
    return [
        IngredienteDeProductoRead(
            id=ing.id,
            nombre=ing.nombre,
            descripcion=ing.descripcion,
            unidad_medida_id=ing.unidad_medida_id,
            cantidad=link.cantidad,
            created_at=ing.created_at,
            updated_at=ing.updated_at,
            deleted_at=ing.deleted_at,
        )
        for ing, link in service.ingredientes_de_producto(producto_id)
    ]
