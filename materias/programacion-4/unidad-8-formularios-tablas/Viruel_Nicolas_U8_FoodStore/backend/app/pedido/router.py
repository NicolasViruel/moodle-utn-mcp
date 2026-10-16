from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.schemas import PaginationParams, pagination_params
from app.pedido import schema, service

router = APIRouter(prefix="/pedido", tags=["Pedidos"])

Pagination = Annotated[PaginationParams, Depends(pagination_params)]


@router.get("/", response_model=schema.PedidoPaginatedResponse, summary="Listar pedidos")
def listar_pedidos(params: Pagination):
    return service.listar(params)


@router.post(
    "/",
    response_model=schema.PedidoRead,
    status_code=status.HTTP_201_CREATED,
    responses={404: {}, 422: {"description": "Sin detalles (RN-12) o datos inválidos"}},
)
def crear_pedido(body: schema.PedidoCreate):
    return service.crear(body)


@router.get("/{pedido_id}", response_model=schema.PedidoRead, responses={404: {}})
def detalle_pedido(pedido_id: int):
    return service.obtener(pedido_id)


@router.put("/{pedido_id}", response_model=schema.PedidoRead, responses={404: {}})
def actualizar_pedido(pedido_id: int, body: schema.PedidoUpdate):
    return service.actualizar(pedido_id, body)


@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {}})
def eliminar_pedido(pedido_id: int) -> None:
    service.eliminar(pedido_id)
