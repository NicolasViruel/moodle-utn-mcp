"""Demuestra 2 síntomas del código original antes de corregirlo."""

from __future__ import annotations


class PoligonoRoto:
    """Versión mínima que reproduce los java-ismos del código de partida."""

    catalogo: list[PoligonoRoto] = []

    def __init__(self, nombre: str, observaciones=[]) -> None:
        self.nombre = nombre
        self._observaciones = observaciones
        PoligonoRoto.catalogo.append(self)

    def agregar_observacion(self, texto: str) -> None:
        self._observaciones.append(texto)

    def get_lados(self) -> list[str]:
        return self._lados

    def set_lados(self, lados: list[str]) -> None:
        self._lados = lados


def sintoma_lista_compartida() -> None:
    print("=== Síntoma 1: argumento mutable compartido (observaciones=[]) ===")
    p1 = PoligonoRoto("A")
    p2 = PoligonoRoto("B")
    p1.agregar_observacion("solo para A")
    print(f"p1.observaciones = {p1._observaciones}")
    print(f"p2.observaciones = {p2._observaciones}")
    print(f"¿Comparten la misma lista? {p1._observaciones is p2._observaciones}")


def sintoma_coleccion_interna_expuesta() -> None:
    print("\n=== Síntoma 2: getLados() devuelve referencia interna ===")
    poligono = PoligonoRoto("Cuadrado")
    poligono.set_lados(["norte", "sur"])
    externa = poligono.get_lados()
    externa.append("este")
    print(f"Lista interna luego de mutar desde afuera: {poligono.get_lados()}")


if __name__ == "__main__":
    sintoma_lista_compartida()
    sintoma_coleccion_interna_expuesta()
