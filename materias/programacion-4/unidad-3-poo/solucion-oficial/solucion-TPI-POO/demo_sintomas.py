"""demo_sintomas.py — Dos java-ismos con síntoma reproducible (Parte 1).

Muestra el síntoma ANTES del arreglo y, al lado, el comportamiento correcto DESPUÉS.
Cada bloque es autocontenido para que el síntoma se vea sin depender del resto.

Correlo con:  python demo_sintomas.py
"""


def sintoma_default_mutable() -> None:
    """Java-ismo #2 — argumento por defecto mutable.

    El valor por defecto `[]` se evalúa UNA sola vez, al definir la función, y todas
    las instancias que usan el default terminan compartiendo la MISMA lista.
    """
    print("== Síntoma 1: argumento por defecto mutable ==")

    class PoligonoAntes:
        def __init__(self, nombre, observaciones=[]):     # <-- java-ismo
            self.nombre = nombre
            self._observaciones = observaciones

        def observar(self, texto):
            self._observaciones.append(texto)

    p1 = PoligonoAntes("p1")
    p2 = PoligonoAntes("p2")
    p1.observar("revisar vértice")
    print("  p1._observaciones:", p1._observaciones)
    print("  p2._observaciones:", p2._observaciones, "  <- ¡se contaminó sin tocar p2!")
    print("  p1._observaciones is p2._observaciones ->", p1._observaciones is p2._observaciones)

    class PoligonoDespues:
        def __init__(self, nombre, observaciones=None):   # <-- corregido
            self.nombre = nombre
            self._observaciones = list(observaciones) if observaciones else []

        def observar(self, texto):
            self._observaciones.append(texto)

    q1 = PoligonoDespues("q1")
    q2 = PoligonoDespues("q2")
    q1.observar("revisar vértice")
    print("  DESPUÉS -> q1:", q1._observaciones, "| q2:", q2._observaciones,
          "| comparten:", q1._observaciones is q2._observaciones)
    print()


def sintoma_atributo_de_clase_mutable() -> None:
    """Java-ismo #3 — atributo de clase mutable (un 'static' accidental).

    Definido a nivel de clase, el `catalogo = []` es UNO solo para todas las
    instancias: objetos sin relación entre sí terminan compartiendo estado.
    """
    print("== Síntoma 2: atributo de clase mutable (static accidental) ==")

    class FiguraAntes:
        catalogo = []                                     # <-- java-ismo

        def __init__(self, nombre):
            self.nombre = nombre
            FiguraAntes.catalogo.append(nombre)

    a = FiguraAntes("triángulo")
    b = FiguraAntes("cuadrado")
    print("  a.catalogo:", a.catalogo)
    print("  b.catalogo:", b.catalogo, "  <- la misma lista para objetos distintos")
    print("  a.catalogo is b.catalogo ->", a.catalogo is b.catalogo)

    class FiguraDespues:
        def __init__(self, nombre):                       # <-- corregido: estado de instancia
            self.nombre = nombre
            self._historial = [nombre]

    c = FiguraDespues("triángulo")
    d = FiguraDespues("cuadrado")
    print("  DESPUÉS -> c._historial:", c._historial, "| d._historial:", d._historial,
          "| comparten:", c._historial is d._historial)
    print()


if __name__ == "__main__":
    sintoma_default_mutable()
    sintoma_atributo_de_clase_mutable()
