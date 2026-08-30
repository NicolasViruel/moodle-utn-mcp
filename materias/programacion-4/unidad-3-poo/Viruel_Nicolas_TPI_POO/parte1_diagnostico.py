"""parte1_diagnostico.py corregido — mismas clases, sin acento de Java."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod


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
    def __init__(self, longitud: float) -> None:
        self._longitud = longitud

    @property
    def longitud(self) -> float:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor


class Poligono(Figura, ABC):
    def __init__(
        self,
        nombre: str,
        color: str,
        lados: list[Lado] | None = None,
        observaciones: list[str] | None = None,
    ) -> None:
        super().__init__(nombre, color)
        self._lados = list(lados or [])
        self._observaciones = list(observaciones or [])

    @abstractmethod
    def lados_esperados(self) -> int: ...

    def perimetro(self) -> float:
        return sum(lado.longitud for lado in self._lados)

    def area(self) -> float:
        return 0.0

    def agregar_observacion(self, texto: str) -> None:
        self._observaciones.append(texto)

    def lados(self) -> tuple[Lado, ...]:
        return tuple(self._lados)


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
    def __init__(self, nombre: str, color: str, lados: list[Lado]) -> None:
        super().__init__(nombre, color, lados)

    def lados_esperados(self) -> int:
        return 4

    def area(self) -> float:
        return self._lados[0].longitud**2


if __name__ == "__main__":
    triangulo = Triangulo("Triángulo", "rojo", [Lado(3), Lado(4), Lado(5)])
    cuadrado = Cuadrado("Cuadrado", "azul", [Lado(2), Lado(2), Lado(2), Lado(2)])

    print(f"Perímetro del triángulo: {triangulo.perimetro()}")
    print(f"Perímetro del cuadrado: {cuadrado.perimetro()}")
    triangulo.agregar_observacion("revisar el vértice A")
    print(f"Nombre (via property): {triangulo.nombre}")
