from typing import List, Optional

from .schemas import ProveedorCreate, ProveedorRead

db_proveedores: List[ProveedorRead] = []
id_counter = 1


def _codigo_existe(codigo: str, excluir_id: Optional[int] = None) -> bool:
    for proveedor in db_proveedores:
        if proveedor.codigo == codigo and proveedor.id != excluir_id:
            return True
    return False


def crear(data: ProveedorCreate) -> ProveedorRead:
    global id_counter
    if _codigo_existe(data.codigo):
        raise ValueError("codigo_duplicado")
    nuevo = ProveedorRead(id=id_counter, **data.model_dump())
    db_proveedores.append(nuevo)
    id_counter += 1
    return nuevo


def obtener_todos(
    skip: int = 0,
    limit: int = 10,
    activo: Optional[bool] = None,
) -> List[ProveedorRead]:
    filtrados = db_proveedores
    if activo is not None:
        filtrados = [p for p in db_proveedores if p.activo == activo]
    return filtrados[skip : skip + limit]


def obtener_por_id(id: int) -> Optional[ProveedorRead]:
    for proveedor in db_proveedores:
        if proveedor.id == id:
            return proveedor
    return None


def actualizar_total(id: int, data: ProveedorCreate) -> Optional[ProveedorRead]:
    if _codigo_existe(data.codigo, excluir_id=id):
        raise ValueError("codigo_duplicado")
    for index, proveedor in enumerate(db_proveedores):
        if proveedor.id == id:
            actualizado = ProveedorRead(id=id, **data.model_dump())
            db_proveedores[index] = actualizado
            return actualizado
    return None


def desactivar(id: int) -> Optional[ProveedorRead]:
    for index, proveedor in enumerate(db_proveedores):
        if proveedor.id == id:
            if not proveedor.activo:
                raise ValueError("ya_desactivado")
            actualizado = proveedor.model_copy(update={"activo": False})
            db_proveedores[index] = actualizado
            return actualizado
    return None
