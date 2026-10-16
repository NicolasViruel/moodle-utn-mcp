from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.categoria import schema, service
from app.core.schemas import PaginationParams, pagination_params
from app.producto.schema import ProductoRead
from app.producto.service import to_read as producto_to_read

router = APIRouter(prefix="/categorias", tags=["Categorías"])

Pagination = Annotated[PaginationParams, Depends(pagination_params)]


@router.get("/", response_model=schema.CategoriaPaginatedResponse, summary="Listar categorías (paginado)")
def listar_categorias(params: Pagination):
    return service.listar(params)


@router.post(
    "/",
    response_model=schema.CategoriaRead,
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "Nombre duplicado (RN-02)"}},
)
def crear_categoria(body: schema.CategoriaCreate):
    return service.crear(body)


@router.get("/{categoria_id}", response_model=schema.CategoriaRead, responses={404: {}})
def detalle_categoria(categoria_id: int):
    return service.obtener(categoria_id)


@router.put("/{categoria_id}", response_model=schema.CategoriaRead, responses={404: {}, 409: {}})
def actualizar_categoria(categoria_id: int, body: schema.CategoriaUpdate):
    return service.actualizar(categoria_id, body)


@router.delete(
    "/{categoria_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {}, 409: {"description": "Tiene productos asociados (RN-05)"}},
)
def eliminar_categoria(categoria_id: int) -> None:
    service.eliminar(categoria_id)


@router.get(
    "/{categoria_id}/productos",
    response_model=list[ProductoRead],
    summary="Productos de una categoría (N:M, solo consulta)",
    responses={404: {}},
)
def productos_de_categoria(categoria_id: int):
    return [producto_to_read(p) for p in service.productos_de_categoria(categoria_id)]
