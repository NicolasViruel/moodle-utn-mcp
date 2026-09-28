from fastapi import HTTPException, status
from sqlmodel import Session

from app.modules.producto.models import Producto
from app.modules.producto.repository import ProductoRepository
from app.modules.producto.schemas import ProductoCreate, ProductoRead, ProductoUpdate


class ProductoService:
    def __init__(self, session: Session) -> None:
        self.repo = ProductoRepository(session)

    def crear(self, data: ProductoCreate) -> ProductoRead:
        if self.repo.get_by_nombre(data.nombre):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un producto con nombre '{data.nombre}'",
            )
        entity = Producto(**data.model_dump())
        saved = self.repo.create(entity)
        return ProductoRead.model_validate(saved)

    def listar(self, skip: int, limit: int) -> list[ProductoRead]:
        items = self.repo.list(skip=skip, limit=limit)
        return [ProductoRead.model_validate(p) for p in items]

    def obtener(self, producto_id: int) -> ProductoRead:
        entity = self.repo.get_by_id(producto_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )
        return ProductoRead.model_validate(entity)

    def actualizar(self, producto_id: int, data: ProductoUpdate) -> ProductoRead:
        entity = self.repo.get_by_id(producto_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )
        otro = self.repo.get_by_nombre(data.nombre)
        if otro and otro.id != producto_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un producto con nombre '{data.nombre}'",
            )
        entity.nombre = data.nombre
        entity.descripcion = data.descripcion
        entity.precio = data.precio
        updated = self.repo.update(entity)
        return ProductoRead.model_validate(updated)

    def eliminar(self, producto_id: int) -> None:
        entity = self.repo.get_by_id(producto_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )
        self.repo.delete(entity)
