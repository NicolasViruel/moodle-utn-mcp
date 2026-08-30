"""parte1_diagnostico.py — YA CORREGIDO (Parte 1).

El mismo dominio del código de partida, con los 8 java-ismos desactivados y el ruido
sintáctico limpio. Se entrega junto a la versión original para que se vea el punto de
partida y el resultado. `figuras.py` lleva este dominio más lejos (Taller, Etiqueta,
Protocol) para las Partes 2 a 4.

Corrección de los 8 java-ismos (tabla completa en informe.md):

  1. Getters preventivos sin lógica  -> atributos / @property de solo-lectura.
  2. Argumento por defecto mutable     -> `None` + copia adentro.
  3. Atributo de clase mutable         -> estado de instancia.
  4. super().__init__() olvidado       -> se llama la cadena de init.
  5. Type hint que mentía / @Override   -> firma honesta; el área se calcula de verdad.
  6. Sobrecarga de constructor Java     -> @classmethod como constructor alternativo.
  7. Bucle acumulador manual            -> comprehension / sum.
  8. (fuera del checklist) Sin copia    -> copia defensiva de entrada y de salida.
     defensiva de la lista recibida
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod


class Figura(ABC):
    def __init__(self, nombre: str, color: str) -> None:
        self._nombre = nombre
        self._color = color

    # Solo-lectura: HAY una razón (proteger la invariante), y el cliente escribe
    # `figura.nombre` igual que si fuera un atributo público.
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def color(self) -> str:
        return self._color

    @abstractmethod
    def area(self) -> float:
        ...


class Lado:
    def __init__(self, longitud: float) -> None:
        self._longitud = self._validar(longitud)

    @staticmethod
    def _validar(valor: float) -> float:
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        return float(valor)

    # El ÚNICO getter que sí correspondía convertir en @property: tiene lógica
    # (validación). El código cliente sigue escribiendo `lado.longitud`.
    @property
    def longitud(self) -> float:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: float) -> None:
        self._longitud = self._validar(valor)


class Poligono(Figura):
    def __init__(self, nombre: str, color: str, longitudes: list[float]) -> None:
        super().__init__(nombre, color)                       # (4) cadena de init
        esperados = self.lados_esperados()
        if len(longitudes) != esperados:
            raise ValueError(
                f"{type(self).__name__} espera {esperados} lados, recibió {len(longitudes)}"
            )
        # (8) copia defensiva de entrada: el polígono fabrica sus propios lados.
        self._lados: list[Lado] = [Lado(l) for l in longitudes]
        self._observaciones: list[str] = []                   # (3) estado de instancia

    @abstractmethod
    def lados_esperados(self) -> int:
        ...

    # (5) firma honesta: el área se calcula de verdad (polígono regular).
    def area(self) -> float:
        n = self.lados_esperados()
        lado = self._lados[0].longitud
        return (n * lado ** 2) / (4 * math.tan(math.pi / n))

    # (7) comprehension en vez de bucle acumulador.
    def perimetro(self) -> float:
        return sum(lado.longitud for lado in self._lados)

    def lados(self) -> tuple[Lado, ...]:
        return tuple(self._lados)                             # (8) copia de salida

    def observar(self, texto: str) -> None:
        self._observaciones.append(texto)


class Triangulo(Poligono):
    def lados_esperados(self) -> int:
        return 3

    # (6) constructor alternativo con @classmethod, no sobrecarga con isinstance.
    @classmethod
    def equilatero(cls, nombre: str, color: str, longitud: float) -> "Triangulo":
        return cls(nombre, color, [longitud, longitud, longitud])


class Cuadrado(Poligono):
    def lados_esperados(self) -> int:
        return 4

    @classmethod
    def regular(cls, nombre: str, color: str, longitud: float) -> "Cuadrado":
        return cls(nombre, color, [longitud] * 4)


if __name__ == "__main__":
    triangulo = Triangulo("Triángulo", "rojo", [3, 4, 5])
    cuadrado = Cuadrado.regular("Cuadrado", "azul", 2)
    print(f"Perímetro del triángulo: {triangulo.perimetro():g}")
    print(f"Perímetro del cuadrado: {cuadrado.perimetro():g}")
    print(f"Área del cuadrado: {cuadrado.area():.2f}")
    print(f"Nombre (acceso por atributo): {triangulo.nombre}")
