# Informe — TP Integrador U3 POO

**Alumno:** Nicolás Viruel

## Tabla de 8 java-ismos

| # | Java-ismo | Dónde | Inversión | Síntoma observable |
|---|-----------|-------|-----------|-------------------|
| 1 | Getters sin lógica (`getNombre`, `getColor`) | `Figura` | Compilador → acuerdo (`@property`) | Código cliente atado a `getX()` innecesario |
| 2 | Bean getter/setter (`getLongitud`/`setLongitud`) | `Lado` | Declaración → runtime con `@property` | Cliente usa métodos en vez de atributo validado |
| 3 | Atributo de clase mutable (`catalogo = []`) | `Poligono` | Static Java → estado de instancia/módulo | Todas las instancias comparten catálogo |
| 4 | Argumentos por defecto mutables | `Poligono.__init__` | Compilador → acuerdo (usar `None`) | `p1._observaciones is p2._observaciones` |
| 5 | `super().__init__()` omitido | `Poligono.__init__` | Herencia nominal → inicialización explícita | Atributos de `Figura` reasignados a mano |
| 6 | Alias de lista externa (`self._lados = lados`) | `Poligono.__init__` | Copia defensiva | Mutar afuera altera estado interno |
| 7 | Bucle acumulador manual | `Poligono.perimetro` | Estilo idiomático (`sum`) | Código verboso y propenso a error |
| 8 | Sin copia defensiva de entrada/salida | `Poligono.__init__` y `getLados()` | El todo debe controlar su estado | Mutar la lista externa altera el polígono |

## Getter convertido en @property (Parte 1)

El único getter con lógica era `Lado.getLongitud` / `setLongitud`.

**Antes:** `lado.getLongitud()` y `lado.setLongitud(5)`  
**Después:** `lado.longitud` y `lado.longitud = 5` (misma interfaz de uso, con validación)

El cliente no cambia: sigue leyendo y escribiendo como atributo, pero ahora con `@property`.

## Equivalencias en mi código

| Elemento en Java | Cómo quedó | ¿Traducción o rediseño? | Por qué |
|------------------|------------|-------------------------|---------|
| `private` + getter | `_nombre` + `@property nombre` | Traducción con convención | Python no tiene `private` |
| `interface Exportable` | `Protocol Exportable` | Rediseño | `PlanoCAD` no puede heredar |
| `abstract class Poligono` | `ABC` + `@abstractmethod` | Traducción directa | Misma intención, falla temprana |
| `List<Lado>` expuesta | `tuple` en `lados()` | Rediseño | Copia defensiva |
| `PoligonoRegular extends Poligono` | `crear_poligono_regular()` | Rediseño | No hay «es-un» real en dominio |
| Bean setter longitud | `@property` con validación | Traducción mejorada | Cliente no cambia (`lado.longitud = 3`) |

## Tres relaciones (Parte 2)

La sintaxis `self._algo = algo` es igual; la diferencia está en **quién crea** y **quién controla el ciclo de vida**:

- **Composición Poligono—Lado:** en `Poligono.__init__`, línea `self._lados = list(lados or [])`. El polígono crea/copia sus lados; no existen sin él.
- **Agregación Taller—Poligono:** en `Taller.recibir`, línea `self._poligonos.append(poligono)`. El taller no construye el polígono; solo lo guarda y puede devolverlo con `restaurar`.
- **Asociación Lado—Etiqueta:** en `Lado.__init__`, línea `self._etiqueta = etiqueta`. La etiqueta puede existir sola; el lado solo la referencia (0..1).

## PoligonoRegular (Parte 3)

No usé herencia artificial `PoligonoRegular extends Poligono`. En Python no necesito un tipo intermedio para meter figuras en una lista: alcanza con `list[Poligono]`. Agregué `Pentagono` y `Hexagono` porque el dominio sí afirma «es-un» polígono concreto. Para N lados genéricos dejé `crear_poligono_regular()` como fábrica, no como subclase.

## ABC vs Protocol (Parte 4)

**¿Lo decide el lenguaje o el dominio?** Lo decide el **dominio y quién controla el código**. Para `Poligono` (nuestro código) conviene `ABC` porque queremos falla temprana y herencia explícita. Para `PlanoCAD` (tercero, no editable) solo sirve `Protocol`: cumple `exportar()` sin conocer nuestro contrato. Una ABC exigiría modificar la librería externa.

## Cierre

**Cambió al pasar a Python:** getters ceremoniales, catálogo estático compartido, herencia solo para tipar listas, devolver colecciones mutables internas.

**Se mantuvo:** el modelo Figura/Poligono/Lado, validación de longitud, polimorfismo por subclases concretas y separación entre dominio propio y librería externa.
