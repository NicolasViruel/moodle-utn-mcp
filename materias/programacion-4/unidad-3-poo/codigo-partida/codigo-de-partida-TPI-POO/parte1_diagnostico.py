"""parte1_diagnostico.py — El dominio Figura / Polígono / Lado, funcionando.

⚠️ Este módulo corre de punta a punta sin lanzar un solo traceback. No tiene bugs
de sintaxis: tiene ACENTO DE JAVA.

Contiene exactamente 8 java-ismos de DISEÑO. Siete están en el checklist de la
Actividad 4; el octavo no está en ese checklist y hay que encontrarlo con criterio,
no con la lista.

Además hay ruido sintáctico (punto y coma al final de línea, comparaciones contra
True, concatenación con + donde iría un f-string). Ese ruido también se limpia, pero
NO cuenta dentro de los 8.

Tu trabajo (Parte 1): encontrarlos, listarlos en informe.md y corregirlos, cada uno
justificado con la inversión conceptual que lo explica.
"""

import math


class Figura:
    def __init__(self, nombre, color):
        self._nombre = nombre
        self._color = color
        self._construida = True   # marca de que Figura.__init__ realmente corrió

    # >>> getters preventivos SIN lógica (ceremonia de Java) <<<
    def getNombre(self):
        return self._nombre

    def getColor(self):
        return self._color

    def area(self):
        return 0.0


class Lado:
    def __init__(self, longitud):
        self._longitud = longitud

    # >>> getter/setter con lógica de validación (estilo Java bean) <<<
    def getLongitud(self):
        return self._longitud

    def setLongitud(self, valor):
        if valor <= 0:
            raise ValueError("La longitud debe ser positiva")
        self._longitud = valor


class Poligono(Figura):

    # >>> atributo de clase mutable: un "static" accidental compartido <<<
    catalogo = []

    # >>> argumento por defecto mutable (lados y observaciones) <<<
    def __init__(self, nombre, color, lados=[], observaciones=[]):
        # >>> super().__init__() olvidado: se re-asignan los atributos a mano <<<
        self._nombre = nombre
        self._color = color
        # >>> se guarda el ALIAS de la lista recibida, sin copiarla <<<
        self._lados = lados
        self._observaciones = observaciones
        Poligono.catalogo.append(self)

    def lados_esperados(self):
        return 0

    # >>> bucle acumulador manual en vez de comprehension <<<
    def perimetro(self):
        total = 0
        for l in self._lados:
            total = total + l.getLongitud()
        return total

    # >>> el type hint miente (-> int y devuelve str) y el "@Override" no existe <<<
    def area(self) -> int:
        return "area sin calcular"

    def agregar_observacion(self, texto):
        self._observaciones.append(texto)

    def getLados(self):
        # devuelve la lista interna tal cual (el llamador puede mutarla desde afuera)
        return self._lados


# >>> sobrecarga de constructor estilo Java: un __init__ con ramas isinstance <<<
class Triangulo(Poligono):
    def __init__(self, *args):
        if len(args) == 3:
            super().__init__(args[0], args[1], args[2])
        elif len(args) == 1 and isinstance(args[0], list):
            super().__init__("triángulo", "negro", args[0])
        else:
            super().__init__("triángulo", "negro", [])

    def lados_esperados(self):
        return 3


class Cuadrado(Poligono):
    def __init__(self, *args):
        if len(args) == 3:
            super().__init__(args[0], args[1], args[2])
        elif len(args) == 1 and isinstance(args[0], list):
            super().__init__("cuadrado", "negro", args[0])
        else:
            super().__init__("cuadrado", "negro", [])

    def lados_esperados(self):
        return 4


if __name__ == "__main__":
    activo = True
    if activo == True:                                      # ruido: == True
        t = Triangulo("Triángulo", "rojo", [Lado(3), Lado(4), Lado(5)]);   # ruido: ;
        c = Cuadrado("Cuadrado", "azul", [Lado(2), Lado(2), Lado(2), Lado(2)])
        print("Perímetro del triángulo: " + str(t.perimetro()))            # ruido: +
        print("Perímetro del cuadrado: " + str(c.perimetro()))
        t.agregar_observacion("revisar el vértice A")
        print("Figuras en el catálogo: " + str(len(Poligono.catalogo)))
        print("Nombre (via getter): " + t.getNombre())
