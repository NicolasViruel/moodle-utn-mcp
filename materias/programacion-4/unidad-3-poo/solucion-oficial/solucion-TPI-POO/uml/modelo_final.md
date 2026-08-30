# Diagrama UML final — Solución de referencia

Refleja las decisiones de las Partes 3 y 4: **`PoligonoRegular` ya no existe como clase**
(se reemplazó por el `@classmethod regular(...)`), y `Exportable` es un `Protocol` que
`Poligono` y `PlanoCAD` cumplen —este último sin heredar de nada.

Pegá el bloque en https://mermaid.live para verlo renderizado.

```mermaid
classDiagram
    class Exportable {
        <<Protocol>>
        +exportar() str
    }
    class Figura {
        <<abstract>>
        #_nombre str
        #_color str
        +nombre str
        +color str
        +area()* float
    }
    class Poligono {
        <<abstract>>
        #_lados list~Lado~
        +lados_esperados()* int
        +area() float
        +perimetro() float
        +lados() tuple~Lado~
        +exportar() str
        +regular(nombre, color, longitud)$ Poligono
    }
    class Lado {
        #_longitud float
        #_etiqueta Etiqueta
        +longitud float
        +etiqueta Etiqueta
        +etiquetar(etiqueta)
        +escalar(factor)
    }
    class Etiqueta {
        <<frozen dataclass>>
        +texto str
    }
    class Taller {
        #_poligonos list~Poligono~
        +recibir(poligono)
        +restaurar(poligono) Poligono
        +inventario() tuple~Poligono~
    }
    class Triangulo {
        +lados_esperados() int
    }
    class Cuadrado {
        +lados_esperados() int
    }
    class Pentagono {
        +lados_esperados() int
    }
    class Hexagono {
        +lados_esperados() int
    }
    class PlanoCAD {
        <<librería externa>>
        +exportar() str
    }

    Figura <|-- Poligono : herencia
    Poligono <|-- Triangulo
    Poligono <|-- Cuadrado
    Poligono <|-- Pentagono
    Poligono <|-- Hexagono
    Poligono "1" *-- "3..*" Lado : composición
    Lado "1" --> "0..1" Etiqueta : asociación
    Taller "1" o-- "0..*" Poligono : agregación
    Poligono ..|> Exportable : cumple
    PlanoCAD ..|> Exportable : cumple sin saberlo
```

## Coherencia diagrama ↔ código

- `Poligono` es abstracta (`ABC`) y su único abstracto es `lados_esperados()`; `area()`
  es un método **concreto** heredado por todas las subclases.
- La composición `*--` se implementa fabricando los `Lado` dentro del constructor de
  `Poligono`; la agregación `o--` se implementa recibiéndolos ya hechos en `Taller`.
- No aparece `PoligonoRegular`: quedó como el constructor de clase `Poligono.regular(...)`.
