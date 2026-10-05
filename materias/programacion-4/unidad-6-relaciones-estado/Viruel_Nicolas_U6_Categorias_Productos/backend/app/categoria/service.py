from fastapi import HTTPException, status

from app.core import database as db
from app.categoria.schema import CategoriaCreate, CategoriaRead, CategoriaUpdate


def _to_read(row: db.CategoriaRow) -> CategoriaRead:
    return CategoriaRead(id=row.id, nombre=row.nombre, descripcion=row.descripcion)


def listar() -> list[CategoriaRead]:
    return [_to_read(c) for c in db.categorias]


def obtener(categoria_id: int) -> CategoriaRead:
    for c in db.categorias:
        if c.id == categoria_id:
            return _to_read(c)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")


def crear(data: CategoriaCreate) -> CategoriaRead:
    row = db.CategoriaRow(
        id=db.next_categoria_id(),
        nombre=data.nombre,
        descripcion=data.descripcion,
    )
    db.categorias.append(row)
    return _to_read(row)


def actualizar(categoria_id: int, data: CategoriaUpdate) -> CategoriaRead:
    for index, c in enumerate(db.categorias):
        if c.id == categoria_id:
            updated = db.CategoriaRow(
                id=categoria_id,
                nombre=data.nombre,
                descripcion=data.descripcion,
            )
            db.categorias[index] = updated
            return _to_read(updated)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")


def eliminar(categoria_id: int) -> None:
    for index, c in enumerate(db.categorias):
        if c.id == categoria_id:
            db.categorias.pop(index)
            db.producto_categorias[:] = [
                link
                for link in db.producto_categorias
                if link.categoria_id != categoria_id
            ]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
