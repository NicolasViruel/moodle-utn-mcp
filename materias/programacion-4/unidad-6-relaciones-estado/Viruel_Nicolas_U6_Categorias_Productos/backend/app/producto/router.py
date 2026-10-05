from fastapi import APIRouter, status

from app.producto import schema, service

router = APIRouter(tags=["Productos"])


@router.get("/productos", response_model=list[schema.ProductoRead])
def listar_productos():
    return service.listar_productos()


@router.get("/productos/{producto_id}", response_model=schema.ProductoRead)
def detalle_producto(producto_id: int):
    return service.obtener_producto(producto_id)


@router.post("/productos", response_model=schema.ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(body: schema.ProductoCreate):
    return service.crear_producto(body)


@router.put("/productos/{producto_id}", response_model=schema.ProductoRead)
def actualizar_producto(producto_id: int, body: schema.ProductoUpdate):
    return service.actualizar_producto(producto_id, body)


@router.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int):
    service.eliminar_producto(producto_id)


@router.get("/producto-categorias", response_model=list[schema.ProductoCategoriaRead])
def listar_relaciones():
    return service.listar_producto_categorias()


@router.post(
    "/producto-categorias",
    response_model=schema.ProductoCategoriaRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_relacion(body: schema.ProductoCategoriaCreate):
    return service.crear_producto_categoria(body)


@router.delete("/producto-categorias/{producto_id}/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_relacion(producto_id: int, categoria_id: int):
    service.eliminar_producto_categoria(producto_id, categoria_id)
