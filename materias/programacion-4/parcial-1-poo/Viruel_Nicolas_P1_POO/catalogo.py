"""Dominio Food Store — catálogo de productos."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


class Exportable(Protocol):
    def exportar(self) -> str: ...


@dataclass(frozen=True)
class UnidadMedida:
    nombre: str
    simbolo: str
    tipo: str


class Categoria:
    def __init__(self, nombre: str, descripcion: str = "") -> None:
        if not nombre.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío")
        self._nombre = nombre.strip()
        self._descripcion = descripcion

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion


class ProductoCategoria:
    """Vínculo de composición: solo lo crea Producto."""

    def __init__(self, producto: Producto, categoria: Categoria, es_principal: bool) -> None:
        self._producto = producto
        self._categoria = categoria
        self._es_principal = es_principal

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @property
    def es_principal(self) -> bool:
        return self._es_principal

    def _marcar_principal(self, valor: bool) -> None:
        self._es_principal = valor


class Producto(ABC):
    def __init__(
        self,
        nombre: str,
        precio_base: float,
        categoria_principal: Categoria,
        stock_cantidad: float = 0,
        habilitado: bool = True,
        unidad_venta: UnidadMedida | None = None,
    ) -> None:
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if precio_base < 0:
            raise ValueError("El precio base no puede ser negativo")
        if stock_cantidad < 0:
            raise ValueError("El stock no puede ser negativo")

        self._nombre = nombre.strip()
        self._precio_base = float(precio_base)
        self._stock_cantidad = float(stock_cantidad)
        self._habilitado = habilitado
        self._unidad_venta = unidad_venta
        self._clasificaciones: list[ProductoCategoria] = [
            ProductoCategoria(self, categoria_principal, True)
        ]

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precio_base(self) -> float:
        return self._precio_base

    @property
    def unidad_venta(self) -> UnidadMedida | None:
        return self._unidad_venta

    @property
    def disponible(self) -> bool:
        return self._habilitado and self._stock_cantidad > 0

    @property
    def precio_publicado(self) -> str:
        if self._unidad_venta is None:
            return f"$ {self._precio_base:.2f}"
        return f"$ {self._precio_base:.2f} / {self._unidad_venta.simbolo}"

    def habilitar(self) -> None:
        self._habilitado = True

    def deshabilitar(self) -> None:
        self._habilitado = False

    def clasificar_en(self, categoria: Categoria, es_principal: bool = False) -> None:
        if not isinstance(categoria, Categoria):
            raise TypeError("categoria debe ser una instancia de Categoria")
        for vinculo in self._clasificaciones:
            if vinculo.categoria is categoria:
                raise ValueError("El producto ya está clasificado en esa categoría")
        if es_principal:
            for vinculo in self._clasificaciones:
                vinculo._marcar_principal(False)
        self._clasificaciones.append(ProductoCategoria(self, categoria, es_principal))

    def categorias(self) -> tuple[ProductoCategoria, ...]:
        return tuple(self._clasificaciones)

    def categoria_principal(self) -> Categoria:
        for vinculo in self._clasificaciones:
            if vinculo.es_principal:
                return vinculo.categoria
        raise ValueError("El producto no tiene categoría principal")

    @abstractmethod
    def precio_final(self, cantidad: float) -> float: ...

    def exportar(self) -> str:
        return f"PROD|{self.nombre}|{self.precio_publicado}|{'SI' if self.disponible else 'NO'}"

    def _validar_cantidad_entera(self, cantidad: float) -> None:
        if not isinstance(cantidad, (int, float)):
            raise TypeError("cantidad debe ser numérica")
        if cantidad < 1 or cantidad != int(cantidad):
            raise ValueError("La cantidad debe ser un entero mayor o igual a 1")


class ProductoSimple(Producto):
    def precio_final(self, cantidad: float) -> float:
        self._validar_cantidad_entera(cantidad)
        return self._precio_base * int(cantidad)


class ProductoPorPeso(Producto):
    def precio_final(self, cantidad: float) -> float:
        if not isinstance(cantidad, (int, float)):
            raise TypeError("cantidad debe ser numérica")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        return round(self._precio_base * float(cantidad), 2)


class ProductoCombo(Producto):
    def __init__(
        self,
        nombre: str,
        componentes: list[Producto],
        descuento: float,
        categoria_principal: Categoria,
        stock_cantidad: float = 0,
        habilitado: bool = True,
    ) -> None:
        if len(componentes) < 2:
            raise ValueError("Un combo requiere al menos 2 componentes")
        for componente in componentes:
            if not isinstance(componente, Producto):
                raise TypeError("Cada componente debe ser un Producto")
        if not 0 <= descuento < 1:
            raise ValueError("El descuento debe estar en [0, 1)")

        precio_unitario = sum(c.precio_final(1) for c in componentes) * (1 - descuento)
        super().__init__(
            nombre=nombre,
            precio_base=precio_unitario,
            categoria_principal=categoria_principal,
            stock_cantidad=stock_cantidad,
            habilitado=habilitado,
            unidad_venta=None,
        )
        self._componentes = list(componentes)
        self._descuento = descuento

    def componentes(self) -> tuple[Producto, ...]:
        return tuple(self._componentes)

    def precio_final(self, cantidad: float) -> float:
        self._validar_cantidad_entera(cantidad)
        unitario = sum(c.precio_final(1) for c in self._componentes) * (1 - self._descuento)
        return unitario * int(cantidad)


class DestacadoVidriera:
    """Reemplaza herencia de ProductoDestacado: cualquier producto puede destacarse."""

    def __init__(self, producto: Producto, orden_vidriera: int) -> None:
        if not isinstance(producto, Producto):
            raise TypeError("producto debe ser una instancia de Producto")
        if orden_vidriera < 1:
            raise ValueError("orden_vidriera debe ser >= 1")
        self._producto = producto
        self._orden_vidriera = orden_vidriera

    @property
    def producto(self) -> Producto:
        return self._producto

    @property
    def orden_vidriera(self) -> int:
        return self._orden_vidriera


def exportar_catalogo(items: list[Exportable]) -> list[str]:
    return [item.exportar() for item in items]
