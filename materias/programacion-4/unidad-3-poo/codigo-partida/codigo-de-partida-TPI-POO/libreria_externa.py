"""libreria_externa.py — Clase de un tercero. NO SE MODIFICA. NUNCA.

Simula una librería externa (por ejemplo, un SDK de CAD que instalaste con pip).
`PlanoCAD` ya tiene un método `exportar()`, pero:

  - No hereda de ninguna clase tuya (ni la conoce).
  - No la podés editar: es de otro, viene en un paquete instalado.

Ese es exactamente el punto de la Parte 4: hacer que `PlanoCAD` cumpla tu contrato
`Exportable` SIN tocar este archivo ni pedirle que herede de nada. Eso solo se puede
con un contrato estructural (`typing.Protocol`); una ABC pura no alcanzaría, porque
exigiría que `PlanoCAD` heredara de ella.
"""


class PlanoCAD:
    """Plano técnico de la librería externa. Cumple 'exportar()' por casualidad."""

    def __init__(self, identificador: str, escala: str = "1:100") -> None:
        self.identificador = identificador
        self.escala = escala

    def exportar(self) -> str:
        return f"PlanoCAD[{self.identificador} @ {self.escala}]"
