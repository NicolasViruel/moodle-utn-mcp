"""Demo ejecutable del dominio resuelto."""

from __future__ import annotations

from figuras import (
    Cuadrado,
    Etiqueta,
    Hexagono,
    Lado,
    Pentagono,
    Poligono,
    Taller,
    Triangulo,
    exportar_todo,
)
from libreria_externa import PlanoCAD


def demostrar_falla_temprana_abc() -> None:
    print("\n=== Falla temprana: instanciar Poligono abstracto ===")
    try:
        Poligono("abstracto", "gris", [])
    except TypeError as error:
        print(f"OK: {error}")


def main() -> None:
    taller = Taller()

    triangulo = Triangulo(
        "Triángulo",
        "rojo",
        [Lado(3, Etiqueta("base")), Lado(4), Lado(5)],
    )
    cuadrado = Cuadrado("Cuadrado", "azul", 2)
    cuadrado.lados()[1].etiquetar("lateral")
    pentagono = Pentagono("Pentágono", "verde", 2)
    hexagono = Hexagono("Hexágono", "amarillo", 2)

    for poligono in (triangulo, cuadrado, pentagono, hexagono):
        taller.recibir(poligono)

    plano = PlanoCAD("A-101")
    exportaciones = exportar_todo([triangulo, cuadrado, pentagono, hexagono, plano])

    print("=== Inventario del taller ===")
    for indice, poligono in enumerate(taller.inventario(), start=1):
        print(
            f"{indice}. {poligono.nombre} | P={poligono.perimetro():.2f} | A={poligono.area():.2f}"
        )

    print("\n=== Exportaciones (Protocol Exportable) ===")
    for linea in exportaciones:
        print(linea)

    print("\n=== Lados etiquetados ===")
    for poligono in taller.inventario():
        for lado in poligono.lados():
            if lado.etiqueta:
                print(f"{poligono.nombre}: {lado.etiqueta.texto}")

    print("\n=== Agregación: el polígono sobrevive al taller ===")
    referencia = hexagono
    taller.restaurar(hexagono)
    print(f"Hexágono fuera del taller: P={referencia.perimetro():.2f}")

    print("\n=== Composición: los lados viven con su polígono ===")
    lados = referencia.lados()
    print(f"Cantidad de lados del hexágono: {len(lados)}")

    demostrar_falla_temprana_abc()


if __name__ == "__main__":
    main()
