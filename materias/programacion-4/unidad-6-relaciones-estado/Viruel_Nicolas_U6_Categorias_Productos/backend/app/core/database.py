from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CategoriaRow:
    id: int
    nombre: str
    descripcion: str


@dataclass
class ProductoRow:
    id: int
    nombre: str
    descripcion: str
    precio_base: str
    imagen_url: list[str]
    disponible: bool


@dataclass
class ProductoCategoriaRow:
    producto_id: int
    categoria_id: int


categorias: list[CategoriaRow] = [
    CategoriaRow(id=1, nombre="Electrónica", descripcion="Dispositivos y accesorios"),
    CategoriaRow(id=2, nombre="Hogar", descripcion="Artículos para el hogar"),
]
productos: list[ProductoRow] = [
    ProductoRow(
        id=1,
        nombre="Notebook",
        descripcion="14 pulgadas, 16 GB RAM",
        precio_base="899000.00",
        imagen_url=["https://example.com/notebook.jpg"],
        disponible=True,
    ),
]
producto_categorias: list[ProductoCategoriaRow] = [
    ProductoCategoriaRow(producto_id=1, categoria_id=1),
]

_next_categoria_id = 3
_next_producto_id = 2


def next_categoria_id() -> int:
    global _next_categoria_id
    value = _next_categoria_id
    _next_categoria_id += 1
    return value


def next_producto_id() -> int:
    global _next_producto_id
    value = _next_producto_id
    _next_producto_id += 1
    return value
