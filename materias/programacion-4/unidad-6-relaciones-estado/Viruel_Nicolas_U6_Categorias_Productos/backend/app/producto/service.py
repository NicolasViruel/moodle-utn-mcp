from fastapi import HTTPException, status

from app.core import database as db
from app.producto.schema import (
    ProductoCategoriaCreate,
    ProductoCategoriaRead,
    ProductoCreate,
    ProductoRead,
    ProductoUpdate,
)


def _producto_read(row: db.ProductoRow) -> ProductoRead:
    return ProductoRead(
        id=row.id,
        nombre=row.nombre,
        descripcion=row.descripcion,
        precio_base=row.precio_base,
        imagen_url=row.imagen_url,
        disponible=row.disponible,
    )


def listar_productos() -> list[ProductoRead]:
    return [_producto_read(p) for p in db.productos]


def obtener_producto(producto_id: int) -> ProductoRead:
    for p in db.productos:
        if p.id == producto_id:
            return _producto_read(p)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")


def crear_producto(data: ProductoCreate) -> ProductoRead:
    row = db.ProductoRow(
        id=db.next_producto_id(),
        nombre=data.nombre,
        descripcion=data.descripcion,
        precio_base=data.precio_base,
        imagen_url=list(data.imagen_url),
        disponible=data.disponible,
    )
    db.productos.append(row)
    return _producto_read(row)


def actualizar_producto(producto_id: int, data: ProductoUpdate) -> ProductoRead:
    for index, p in enumerate(db.productos):
        if p.id == producto_id:
            updated = db.ProductoRow(
                id=producto_id,
                nombre=data.nombre,
                descripcion=data.descripcion,
                precio_base=data.precio_base,
                imagen_url=list(data.imagen_url),
                disponible=data.disponible,
            )
            db.productos[index] = updated
            return _producto_read(updated)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")


def eliminar_producto(producto_id: int) -> None:
    for index, p in enumerate(db.productos):
        if p.id == producto_id:
            db.productos.pop(index)
            db.producto_categorias[:] = [
                link for link in db.producto_categorias if link.producto_id != producto_id
            ]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")


def _categoria_existe(categoria_id: int) -> bool:
    return any(c.id == categoria_id for c in db.categorias)


def _producto_existe(producto_id: int) -> bool:
    return any(p.id == producto_id for p in db.productos)


def listar_producto_categorias() -> list[ProductoCategoriaRead]:
    return [
        ProductoCategoriaRead(producto_id=link.producto_id, categoria_id=link.categoria_id)
        for link in db.producto_categorias
    ]


def crear_producto_categoria(data: ProductoCategoriaCreate) -> ProductoCategoriaRead:
    if not _producto_existe(data.producto_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    if not _categoria_existe(data.categoria_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    for link in db.producto_categorias:
        if link.producto_id == data.producto_id and link.categoria_id == data.categoria_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La relación producto-categoría ya existe",
            )
    db.producto_categorias.append(
        db.ProductoCategoriaRow(producto_id=data.producto_id, categoria_id=data.categoria_id)
    )
    return ProductoCategoriaRead(producto_id=data.producto_id, categoria_id=data.categoria_id)


def eliminar_producto_categoria(producto_id: int, categoria_id: int) -> None:
    for index, link in enumerate(db.producto_categorias):
        if link.producto_id == producto_id and link.categoria_id == categoria_id:
            db.producto_categorias.pop(index)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Relación producto-categoría no encontrada",
    )
