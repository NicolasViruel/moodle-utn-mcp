"""figuras.py — Dominio Figura / Polígono / Lado resuelto (Partes 1 a 4).

Versión Python idiomática del dominio: los 8 java-ismos corregidos, las relaciones
estructurales modeladas por ciclo de vida, la jerarquía con ABC y el contrato
`Exportable` como Protocol. Importa `libreria_externa` sin modificarla.

Mapa de decisiones (detalle completo en informe.md):

  - Encapsulamiento por convención: `_` como acuerdo; @property solo donde hay lógica.
  - Composición Polígono → Lado: el polígono FABRICA sus lados adentro (recibe floats).
  - Agregación Taller → Polígono: el taller RECIBE polígonos ya construidos.
  - Asociación Lado → Etiqueta: 0..1, escrita como `Etiqueta | None`.
  - Copia defensiva de entrada y de salida sobre las multiplicidades *.
  - Herencia solo donde el dominio afirma «es-un»; ABC con falla temprana al construir.
  - `PoligonoRegular` NO va por herencia: se reemplaza por un @classmethod fábrica.
  - Contrato `Exportable` como Protocol: `PlanoCAD` lo cumple sin heredar de nada.
"""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


# --------------------------------------------------------------------------- #
# Contrato estructural (Parte 4)
# --------------------------------------------------------------------------- #
@runtime_checkable
class Exportable(Protocol):
    """Contrato estructural: alcanza con TENER `exportar()`, no hay que heredarlo.

    Por eso `PlanoCAD` (de libreria_externa.py) lo cumple sin conocerlo ni tocar su
    código. Una ABC pura no serviría: obligaría a `PlanoCAD` a heredar de ella.
    """

    def exportar(self) -> str: ...


# --------------------------------------------------------------------------- #
# Objeto-valor inmutable (Parte 2)
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Etiqueta:
    """Identifica a un Lado con un texto. Es un objeto-valor: inmutable y sin identidad
    propia (dos etiquetas con el mismo texto son intercambiables)."""

    texto: str


# --------------------------------------------------------------------------- #
# La clase única y la asociación (Parte 2)
# --------------------------------------------------------------------------- #
class Lado:
    """Un lado de un polígono. Puede llevar, opcionalmente, una Etiqueta (asociación 0..1)."""

    def __init__(self, longitud: float, etiqueta: Etiqueta | None = None) -> None:
        self._longitud = self._validar(longitud)
        self._etiqueta = etiqueta

    @staticmethod
    def _validar(valor: float) -> float:
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        return float(valor)

    # @property porque HAY lógica: validación y solo-lectura hacia afuera.
    # El código cliente escribe `lado.longitud` igual que si fuera un atributo.
    @property
    def longitud(self) -> float:
        return self._longitud

    @property
    def etiqueta(self) -> Etiqueta | None:
        return self._etiqueta

    def etiquetar(self, etiqueta: Etiqueta) -> None:
        """Asociación 0..1: el Lado conserva una referencia a una Etiqueta creada aparte."""
        self._etiqueta = etiqueta

    def escalar(self, factor: float) -> None:
        self._longitud = self._validar(self._longitud * factor)

    def __repr__(self) -> str:
        marca = f" «{self._etiqueta.texto}»" if self._etiqueta else ""
        return f"Lado({self._longitud:g}{marca})"


# --------------------------------------------------------------------------- #
# Figura y la jerarquía de polígonos (Partes 1 y 3)
# --------------------------------------------------------------------------- #
class Figura(ABC):
    """Molde incompleto: sabe que toda figura tiene nombre, color y un área,
    pero no sabe calcular el área. Eso lo define cada subclase."""

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
    def area(self) -> float:
        ...


class Poligono(Figura):
    """Polígono abstracto. COMPONE sus lados: los fabrica adentro a partir de las
    longitudes que recibe, así que nacen y mueren con él (composición 3..*).

    Es abstracto: `lados_esperados()` es un @abstractmethod. Instanciar un Polígono
    (o una subclase que no lo implemente) revienta al construir — falla temprana.
    """

    def __init__(self, nombre: str, color: str, longitudes: list[float]) -> None:
        super().__init__(nombre, color)          # la cadena de init NO es automática
        esperados = self.lados_esperados()
        if len(longitudes) != esperados:
            raise ValueError(
                f"{type(self).__name__} espera {esperados} lados, recibió {len(longitudes)}"
            )
        # Composición: el polígono FABRICA sus propios Lado. No entran ya hechos.
        self._lados: list[Lado] = [Lado(l) for l in longitudes]

    @abstractmethod
    def lados_esperados(self) -> int:
        ...

    # Método CONCRETO en una ABC: todas las subclases lo heredan (área de polígono
    # regular). Asumimos lados iguales; el foco de la unidad es el diseño, no la
    # geometría de polígonos irregulares.
    def area(self) -> float:
        n = self.lados_esperados()
        lado = self._lados[0].longitud
        return (n * lado ** 2) / (4 * math.tan(math.pi / n))

    def perimetro(self) -> float:
        return sum(lado.longitud for lado in self._lados)

    def lados(self) -> tuple[Lado, ...]:
        """Copia defensiva de salida: una tupla, no la lista interna. El cliente no
        puede agregar ni quitar lados salteándose al polígono."""
        return tuple(self._lados)

    def etiquetar_lado(self, indice: int, etiqueta: Etiqueta) -> None:
        self._lados[indice].etiquetar(etiqueta)

    def exportar(self) -> str:
        return (
            f"{type(self).__name__.lower()}({self._nombre}, {self._color}, "
            f"lados={self.lados_esperados()}, perímetro={self.perimetro():g})"
        )

    # Fábrica de polígonos regulares. Reemplaza a la vieja clase `PoligonoRegular`,
    # que en el código de partida heredaba de Poligono SOLO para compartir el tipo en
    # una lista — una necesidad del compilador de Java que en Python no existe.
    @classmethod
    def regular(cls, nombre: str, color: str, longitud: float) -> "Poligono":
        n = cls._LADOS_REGULAR
        return cls(nombre, color, [longitud] * n)


class Triangulo(Poligono):
    _LADOS_REGULAR = 3

    def lados_esperados(self) -> int:
        return 3


class Cuadrado(Poligono):
    _LADOS_REGULAR = 4

    def lados_esperados(self) -> int:
        return 4


class Pentagono(Poligono):
    _LADOS_REGULAR = 5

    def lados_esperados(self) -> int:
        return 5


class Hexagono(Poligono):
    _LADOS_REGULAR = 6

    def lados_esperados(self) -> int:
        return 6


# --------------------------------------------------------------------------- #
# Agregación (Parte 2)
# --------------------------------------------------------------------------- #
class Taller:
    """Un taller que recibe polígonos ya construidos para restaurarlos y se los
    devuelve. AGREGACIÓN: los recibe hechos (entran por parámetro, no los fabrica) y
    les sobreviven — si el taller desaparece, los polígonos siguen existiendo."""

    def __init__(self) -> None:
        self._poligonos: list[Poligono] = []

    def recibir(self, poligono: Poligono) -> None:
        """La firma lo delata: el polígono ENTRA por parámetro, ya construido."""
        self._poligonos.append(poligono)

    def restaurar(self, poligono: Poligono) -> Poligono:
        """Lo devuelve tras 'restaurarlo'. El polígono sale del taller intacto: sigue
        siendo el mismo objeto y sigue funcionando fuera de acá."""
        if poligono in self._poligonos:
            self._poligonos.remove(poligono)
        return poligono

    def inventario(self) -> tuple[Poligono, ...]:
        """Copia defensiva de salida sobre la multiplicidad *."""
        return tuple(self._poligonos)


# --------------------------------------------------------------------------- #
# El contrato en acción (Parte 4)
# --------------------------------------------------------------------------- #
def exportar_todo(items: list[Exportable]) -> list[str]:
    """Recibe cualquier cosa que sepa `exportar()` — polígonos y planos CAD en la
    misma lista — y devuelve sus representaciones. No pregunta el tipo: duck typing."""
    return [item.exportar() for item in items]
