# Informe — TP Integrador Unidad 3 (POO) · Solución de referencia

> Modelo de informe para corrección. La consigna pide **máximo 1 carilla**: esta versión
> es más larga a propósito, para servir de guía al tutor.

## 1. Tabla de los 8 java-ismos (Parte 1)

| # | Java-ismo | Dónde (clase.método) | Inversión que lo explica | Síntoma observable |
|---|-----------|----------------------|--------------------------|--------------------|
| 1 | Getters preventivos sin lógica | `Figura.getNombre/getColor`, `Lado.getLongitud` | Declaración → acceso por atributo: en Python el getter vacío sobra | El cliente escribe `fig.getNombre()`; 3 líneas de ceremonia por atributo |
| 2 | Argumento por defecto mutable | `Poligono.__init__(lados=[], observaciones=[])` | Runtime: el default se evalúa una sola vez y se comparte | `p1._observaciones is p2._observaciones` → `True` (ver demo_sintomas) |
| 3 | Atributo de clase mutable (static accidental) | `Poligono.catalogo = []` | Runtime: vive en la clase, no en la instancia | Instancias sin relación comparten y llenan la misma lista |
| 4 | `super().__init__()` olvidado | `Poligono.__init__` | Herencia: la cadena de init NO es automática | Se re-asignan atributos a mano; lo que Figura hacía se saltea |
| 5 | Type hint que miente / `@Override` inexistente | `Poligono.area(self) -> int` devuelve `str` | Declaración → runtime: el hint no valida nada solo | `area()` devuelve `"area sin calcular"` pese a `-> int` |
| 6 | Sobrecarga de constructor estilo Java | `Triangulo.__init__(*args)` con `isinstance` | Acuerdo: en Python la sobrecarga se resuelve con `@classmethod` | `__init__` ilegible con ramas; frágil ante nuevos casos |
| 7 | Bucle acumulador manual | `Poligono.perimetro` | Estilo idiomático: comprehension / `sum` | `total = total + ...`; verboso y propenso a error |
| 8 | **(fuera del checklist)** Sin copia defensiva de **entrada**: se guarda el alias de la lista recibida | `Poligono.__init__: self._lados = lados` y `getLados()` la devuelve | Ciclo de vida / *ownership*: el «todo» no controla su parte | El llamador conserva la lista interna y la muta desde afuera |

**Por qué el #8 no está en el checklist.** El checklist y los videos enseñan la copia
defensiva de **salida** (que `lados()` devuelva una copia). El #8 es el mismo criterio
—que el objeto controle su estado— aplicado a la **entrada**, donde no te lo mostraron.
Quien aplica la lista lo pasa por alto; quien entendió el criterio lo ve.

**Ruido sintáctico (no cuenta dentro de los 8):** punto y coma al final de línea,
`if activo == True:` y concatenación con `+ str(...)` donde va un f-string. Limpiado.

## 2. El getter que sí correspondía convertir en @property (Parte 1.4)

```python
# ANTES (atributo público):  lado.longitud = 5     # nada valida el valor
# DESPUÉS (@property con validación):
@property
def longitud(self) -> float:
    return self._longitud

@longitud.setter
def longitud(self, valor: float) -> None:
    self._longitud = self._validar(valor)   # ahora sí valida
```

El código cliente **no cambia una línea**: sigue siendo `lado.longitud` para leer y
`lado.longitud = 7` para escribir. Se cambió la implementación sin tocar la interfaz.

## 3. Tabla de equivalencias sobre el propio código

| Elemento en Java | Cómo quedó en Python | ¿Directa o rediseño? | Por qué |
|---|---|---|---|
| `private double longitud` + get/set | `_longitud` + `@property longitud` | Rediseño | El getter solo se justifica por la validación; si no, sería un atributo |
| `List<Lado> getLados()` | `lados() -> tuple[Lado, ...]` | Rediseño | La tupla es la copia defensiva de salida |
| Constructor sobrecargado | `@classmethod regular(...)` | Rediseño | Python no tiene sobrecarga; el classmethod nombra la intención |
| `abstract class Figura` | `class Figura(ABC)` + `@abstractmethod` | Directa | Mismo concepto, otra sintaxis |
| `interface Exportable` | `class Exportable(Protocol)` | Rediseño | El Protocol permite tipar a `PlanoCAD` sin que herede |
| `final` (value object) | `@dataclass(frozen=True) Etiqueta` | Directa | Inmutabilidad declarativa |
| `for` con acumulador | `sum(l.longitud for l in ...)` | Directa | Mismo cálculo, idioma Python |

## 4. La pregunta de las tres relaciones (Parte 2)

La sintaxis de guardar la referencia es idéntica (`self._algo = algo`). La diferencia
**no vive en la sintaxis, vive en el ciclo de vida y se lee en el constructor**:

- **Composición** `Poligono — Lado`: en `Poligono.__init__` los lados se **fabrican
  adentro** (`self._lados = [Lado(l) for l in longitudes]`). Los `Lado` no existían
  antes y no sobreviven al polígono. Línea que lo delata: la que hace `Lado(...)`.
- **Agregación** `Taller — Poligono`: en `Taller.recibir(poligono)` el polígono **entra
  ya construido por parámetro** (`self._poligonos.append(poligono)`). Le sobrevive al
  taller. Línea que lo delata: la firma `recibir(self, poligono)`.
- **Asociación** `Lado — Etiqueta`: la `Etiqueta` se crea aparte y se pasa
  (`lado.etiquetar(etiqueta)`); es el vínculo más débil, 0..1. Línea que lo delata:
  `self._etiqueta = etiqueta`, con la etiqueta viniendo de afuera y pudiendo ser `None`.

## 5. Decisión sobre PoligonoRegular (Parte 3)

**Se rediseña: PoligonoRegular NO va por herencia.** En el código de partida heredaba de
`Poligono` solo para compartir el tipo en una lista — una necesidad del compilador de
Java. En Python el duck typing hace innecesario ese «tipo común». Se reemplaza por un
**`@classmethod regular(...)`** (y los `equilatero` / `regular` de las subclases): un
constructor alternativo que arma un polígono de lados iguales sin inventar una jerarquía.
La jerarquía que **se queda** es `Figura → Poligono → Triangulo/Cuadrado/Pentagono/
Hexagono`, porque ahí sí el dominio afirma «un triángulo **es un** polígono».

Falla temprana verificada en `main.py`: instanciar `Poligono(...)` directo lanza
`TypeError` al construir, no al usar.

## 6. ¿Lo decide el lenguaje o el dominio? (Parte 4)

Lo decide **el dominio**, y el lenguaje solo pone el mecanismo. Para `Poligono` elegimos
**ABC**: es nuestra clase, queremos que las subclases **declaren** que son polígonos y
que falle temprano si no implementan `lados_esperados()` (contrato nominal). Para
`PlanoCAD` no hay opción: es de un tercero, no podemos hacerla heredar, así que el
contrato `Exportable` tiene que ser **estructural** → `Protocol`. Las Partes 3 y 4
pedían la misma decisión desde dos caminos: la herencia (¿es-un?) y el contrato
(¿quién debe conocerlo?). El criterio único: **usás herencia/ABC cuando el que cumple el
contrato debe conocerlo; Protocol cuando alcanza con que tenga los métodos.**

## 7. Cierre: qué cambió y qué se mantuvo

Se **mantuvo idéntico** el modelo UML: las clases, sus relaciones y multiplicidades son
las mismas que dibujarías en Java. Lo que **cambió** fue cómo el lenguaje materializa
esas decisiones: los getters se volvieron acceso por atributo, la interfaz se volvió
Protocol, `final` se volvió `frozen=True`, y la sobrecarga se volvió `@classmethod`. El
diseño no se tradujo: se volvió a pensar dónde Java imponía y Python deja elegir.
