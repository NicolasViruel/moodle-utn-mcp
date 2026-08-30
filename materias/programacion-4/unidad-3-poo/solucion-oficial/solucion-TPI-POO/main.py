"""main.py — Demo ejecutable del dominio resuelto.

Arma un taller con 4 polígonos (uno de cada subclase), etiqueta 2 lados, exporta todo
junto con un PlanoCAD y muestra el inventario. Además deja a la vista las decisiones de
diseño que la unidad pide distinguir: composición vs. agregación y la falla temprana de
la ABC.

Correlo con:  python main.py
"""

from figuras import (
    Triangulo, Cuadrado, Pentagono, Hexagono,
    Etiqueta, Taller, Poligono, exportar_todo,
)
from libreria_externa import PlanoCAD


def separador(titulo: str) -> None:
    print(f"\n=== {titulo} ===")


def main() -> None:
    # --- Armado del taller (agregación: recibe polígonos ya construidos) ---
    separador("Taller con 4 polígonos")
    triangulo = Triangulo("Triángulo", "rojo", [3, 4, 5])
    cuadrado = Cuadrado.regular("Cuadrado", "azul", 2)      # fábrica de regulares
    pentagono = Pentagono.regular("Pentágono", "verde", 2)
    hexagono = Hexagono.regular("Hexágono", "negro", 2)

    taller = Taller()
    for poligono in (triangulo, cuadrado, pentagono, hexagono):
        taller.recibir(poligono)

    # --- Etiquetar al menos 2 lados (asociación 0..1) ---
    triangulo.etiquetar_lado(0, Etiqueta("hipotenusa"))
    cuadrado.etiquetar_lado(0, Etiqueta("base"))
    print("Lados del triángulo:", triangulo.lados())
    print("Lados del cuadrado :", cuadrado.lados())

    # --- Exportar todo junto con un PlanoCAD (contrato Protocol) ---
    separador("exportar_todo (polígonos + PlanoCAD en la misma lista)")
    plano = PlanoCAD("PL-042")
    for linea in exportar_todo([triangulo, cuadrado, pentagono, hexagono, plano]):
        print(" -", linea)

    # --- Inventario del taller (copia defensiva de salida) ---
    separador("Inventario del taller")
    for poligono in taller.inventario():
        print(f" - {poligono.nombre}: área={poligono.area():.2f}, perímetro={poligono.perimetro():g}")

    # --- Agregación: el polígono SOBREVIVE al taller ---
    separador("Agregación: el polígono sobrevive al taller")
    taller.restaurar(cuadrado)                     # el cuadrado sale del taller
    print("Cuadrado tras salir del taller ->", cuadrado.exportar())
    print("Sigue en inventario del taller:", cuadrado in taller.inventario())

    # --- Composición: el polígono FABRICA sus lados adentro ---
    separador("Composición: los lados nacen dentro del polígono")
    print("El triángulo se construyó desde [3, 4, 5] (floats), no desde objetos Lado.")
    print("Sus lados son objetos que fabricó él:", triangulo.lados())
    copia = triangulo.lados()
    print("lados() devuelve una copia:", copia is not triangulo._lados)

    # --- Falla temprana de la ABC: instanciar al abstracto revienta al construir ---
    separador("Falla temprana: instanciar un Polígono abstracto")
    try:
        Poligono("genérico", "gris", [1, 2, 3])    # type: ignore[abstract]
    except TypeError as e:
        print("TypeError al construir (correcto):", e)


if __name__ == "__main__":
    main()
