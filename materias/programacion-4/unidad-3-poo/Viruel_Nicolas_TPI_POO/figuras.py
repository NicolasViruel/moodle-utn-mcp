"""Dominio Figura / Poligono / Lado resuelto (Partes 1 a 4)."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


class Exportable(Protocol):
    def exportar(self) -> str: ...


@dataclass(frozen=True)
class Etiqueta:
    texto: str


class Figura(ABC):
    def __init__(self, nombre: str, color: str) -> None:
        self._nombre = nombre
        self._color = color

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def color(self) -> str:
        return self._color

    @abstractmethod
    def area(self) -> float: ...


class Lado:
    def __init__(self, longitud: float, etiqueta: Etiqueta | None = None) -> None:
        self._longitud = longitud
        self._etiqueta = etiqueta

    @property
    def longitud(self) -> float:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor

    @property
    def etiqueta(self) -> Etiqueta | None:
        return self._etiqueta

    def escalar(self, factor: float) -> None:
        if factor <= 0:
            raise ValueError("El factor debe ser positivo")
        self.longitud = self._longitud * factor

    def etiquetar(self, texto: str) -> None:
        self._etiqueta = Etiqueta(texto)


class Poligono(Figura, ABC):
    def __init__(self, nombre: str, color: str, lados: list[Lado] | None = None) -> None:
        super().__init__(nombre, color)
        self._lados = list(lados or [])
        self._validar_lados()

    @abstractmethod
    def lados_esperados(self) -> int: ...

    def _validar_lados(self) -> None:
        esperados = self.lados_esperados()
        if len(self._lados) != esperados:
            raise ValueError(
                f"{type(self).__name__} requiere {esperados} lados, recibió {len(self._lados)}"
            )

    def perimetro(self) -> float:
        return sum(lado.longitud for lado in self._lados)

    def lados(self) -> tuple[Lado, ...]:
        return tuple(self._lados)

    def exportar(self) -> str:
        return f"{self.nombre} [{self.color}] P={self.perimetro():.2f} A={self.area():.2f}"


class Triangulo(Poligono):
    def __init__(self, nombre: str, color: str, lados: list[Lado]) -> None:
        super().__init__(nombre, color, lados)

    def lados_esperados(self) -> int:
        return 3

    def area(self) -> float:
        a, b, c = (lado.longitud for lado in self._lados)
        s = (a + b + c) / 2
        radicando = s * (s - a) * (s - b) * (s - c)
        return math.sqrt(max(radicando, 0.0))


class Cuadrado(Poligono):
    def __init__(self, nombre: str, color: str, lado: float) -> None:
        lados = [Lado(lado) for _ in range(4)]
        super().__init__(nombre, color, lados)

    def lados_esperados(self) -> int:
        return 4

    def area(self) -> float:
        return self._lados[0].longitud**2


class Pentagono(Poligono):
    def __init__(self, nombre: str, color: str, lado: float) -> None:
        lados = [Lado(lado) for _ in range(5)]
        super().__init__(nombre, color, lados)

    def lados_esperados(self) -> int:
        return 5

    def area(self) -> float:
        lado = self._lados[0].longitud
        return (5 * lado**2) / (4 * math.tan(math.pi / 5))


class Hexagono(Poligono):
    def __init__(self, nombre: str, color: str, lado: float) -> None:
        lados = [Lado(lado) for _ in range(6)]
        super().__init__(nombre, color, lados)

    def lados_esperados(self) -> int:
        return 6

    def area(self) -> float:
        lado = self._lados[0].longitud
        return (3 * math.sqrt(3) / 2) * lado**2


class Taller:
    def __init__(self) -> None:
        self._poligonos: list[Poligono] = []

    def recibir(self, poligono: Poligono) -> None:
        self._poligonos.append(poligono)

    def restaurar(self, poligono: Poligono) -> None:
        if poligono in self._poligonos:
            self._poligonos.remove(poligono)

    def inventario(self) -> tuple[Poligono, ...]:
        return tuple(self._poligonos)


def exportar_todo(items: list[Exportable]) -> list[str]:
    return [item.exportar() for item in items]


def crear_poligono_regular(lados: int, nombre: str, color: str, longitud: float) -> Poligono:
    """Reemplazo de PoligonoRegular: sin herencia artificial, usa subclases concretas."""

    if lados == 3:
        return Triangulo(nombre, color, [Lado(longitud) for _ in range(3)])
    if lados == 4:
        return Cuadrado(nombre, color, longitud)
    if lados == 5:
        return Pentagono(nombre, color, longitud)
    if lados == 6:
        return Hexagono(nombre, color, longitud)
    raise ValueError(f"No hay subclase de dominio para {lados} lados")


__all__ = [
    "Etiqueta",
    "Exportable",
    "Figura",
    "Hexagono",
    "Lado",
    "Pentagono",
    "Poligono",
    "Triangulo",
    "Cuadrado",
    "Taller",
    "crear_poligono_regular",
    "exportar_todo",
]
