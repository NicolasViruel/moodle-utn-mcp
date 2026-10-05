from fastapi import APIRouter, status

from app.categoria import schema, service

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.get("/", response_model=list[schema.CategoriaRead])
def listar_categorias():
    return service.listar()


@router.get("/{categoria_id}", response_model=schema.CategoriaRead)
def detalle_categoria(categoria_id: int):
    return service.obtener(categoria_id)


@router.post("/", response_model=schema.CategoriaRead, status_code=status.HTTP_201_CREATED)
def crear_categoria(body: schema.CategoriaCreate):
    return service.crear(body)


@router.put("/{categoria_id}", response_model=schema.CategoriaRead)
def actualizar_categoria(categoria_id: int, body: schema.CategoriaUpdate):
    return service.actualizar(categoria_id, body)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(categoria_id: int):
    service.eliminar(categoria_id)
