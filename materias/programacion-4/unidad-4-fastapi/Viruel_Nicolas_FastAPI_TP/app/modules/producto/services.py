from typing import List, Optional
from .schemas import ProductoCreate, ProductoRead

# Simulamos que la BD guarda objetos tipo ProductoRead (con ID asignado)
db_productos: List[ProductoRead] = []
id_counter = 1


def crear(data: ProductoCreate) -> ProductoRead:
    global id_counter
    nuevo = ProductoRead(id=id_counter, **data.model_dump())
    db_productos.append(nuevo)
    id_counter += 1
    return nuevo


def obtener_todos(skip: int, limit: int) -> List[ProductoRead]:
    return db_productos[skip : skip + limit]


def obtener_por_id(id: int) -> Optional[ProductoRead]:
    for p in db_productos:
        if p.id == id:
            return p
    return None


def actualizar_total(id: int, data: ProductoCreate) -> Optional[ProductoRead]:
    # Reemplazo total: Requiere todos los campos validables (ProductoCreate)
    for index, p in enumerate(db_productos):
        if p.id == id:
            producto_actualizado = ProductoRead(id=id, **data.model_dump())
            db_productos[index] = producto_actualizado
            return producto_actualizado
    return None


def desactivar(id: int) -> Optional[ProductoRead]:
    # Borrado lógico: Solo altera el estado 'activo'
    for index, p in enumerate(db_productos):
        if p.id == id:
            p_dict = p.model_dump()
            p_dict["activo"] = False
            producto_actualizado = ProductoRead(**p_dict)
            db_productos[index] = producto_actualizado
            return producto_actualizado
    return None


def obtener_estado_stock(id: int) -> Optional[dict]:
    producto = obtener_por_id(id)
    if not producto:
        return None

    # La lógica de negocio vive aquí
    alerta_stock = producto.stock < producto.stock_minimo

    return {
        "stock": producto.stock,
        "bajo_stock_minimo": alerta_stock,
        "activo": producto.activo,
    }
