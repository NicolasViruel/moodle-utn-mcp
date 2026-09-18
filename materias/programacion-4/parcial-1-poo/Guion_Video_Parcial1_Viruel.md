# Guion para el video — Parcial 1 POO

**Nicolás Viruel · Programación IV · Food Store**

Tiempo: entre **10 y 15 minutos** · Cámara **siempre encendida**

---

## Paso 0 — Antes de grabar (2 minutos)

1. Abrí la carpeta `Viruel_Nicolas_P1_POO` en VS Code.
2. Dejá la terminal abierta, lista para escribir `python main.py`.
3. Abrí estos archivos en pestañas:
   - `main.py`
   - `catalogo.py`
   - `uml/modelo_final.md`
   - `libreria_externa.py`
4. Probá micrófono y cámara. Si todo suena y se ve bien, arrancá.

**Tip:** Tené este guion en otra pantalla o impreso. No hace falta memorizarlo: leélo con naturalidad.

---

## Mapa — dónde está cada cosa

Usá esta tabla cuando el guion mencione un archivo o una línea.

| Qué es | Archivo | Líneas / sección |
|--------|---------|------------------|
| Demo que corre en terminal | `main.py` | todo el archivo |
| Crear productos, relaciones, precios, exportar | `catalogo.py` | clases y funciones del dominio |
| Librería externa (no se toca) | `libreria_externa.py` | `FichaPuntoDeVenta` |
| Diagrama UML (dibujo de clases) | `uml/modelo_final.md` | bloque `classDiagram` (no es código Python) |
| Composición ProductoCategoria | **`catalogo.py`** | líneas **80** y **120** |
| Agregación combo → componentes | **`catalogo.py`** línea **186** + **`main.py`** líneas **76-78** | |
| Asociación Producto ↔ UnidadMedida | `catalogo.py` 14-18, 65, 78, 100-103 · opcional `main.py` 43-45 y 51-56 | |
| DestacadoVidriera (sin herencia) | `catalogo.py` | 198-215 · demo en `main.py` línea 84 |
| Exportable Protocol | `catalogo.py` | 10-11 |
| exportar_catalogo | `catalogo.py` | 218 |
| Producto ABC + precio_final abstracto | `catalogo.py` | 57, 131-132 |
| Falla temprana TypeError | `main.py` | 18-39 |
| Precio del combo calculado | `catalogo.py` | **177** (no está en el .md del UML) |
| Stock propio del combo | `catalogo.py` | 166, 182, 186 |
| Formato exportar PROD\|... | `catalogo.py` | 134-135 |

**Importante:** cuando diga "línea 177" (o cualquier número de línea), casi siempre es **`catalogo.py`**. El archivo `modelo_final.md` solo tiene el diagrama (~90 líneas), no lógica de precios.

### Ver el UML como imagen

1. Abrí `uml/modelo_final.md`.
2. Para **mermaid.live**: copiá **solo** desde `classDiagram` hasta el final de las flechas. **No copies** `` ```mermaid `` ni el título `# Diagrama UML...`.
3. Pegá en [mermaid.live](https://mermaid.live).
4. Si falla, revisá que no hayan quedado comillas ` ``` ` al principio o al final.

El error más común es pegar todo el markdown. Mermaid.live espera código puro, no el archivo entero.

---

## Paso 1 — Presentación (1 minuto)

**Qué hacer:** Mirá a la cámara. Todavía no compartas pantalla.

**Qué decir:**

> Hola, soy Nicolás Viruel.
>
> Este es el video del Parcial 1 de Programación IV.
>
> Hice el catálogo de Food Store en Python.
>
> Primero voy a correr el programa para que vean que funciona.
>
> Después voy a responder las cuatro preguntas del parcial, mostrando mi código.

---

## Paso 2 — Correr la demo (2 a 3 minutos)

**Qué hacer:** Compartí pantalla. En la terminal, escribí `python main.py` y Enter.

**Qué decir mientras corre** (andá leyendo lo que sale en pantalla):

> Arranco la demo.
>
> **Precios finales:** acá se ve que cada tipo de producto cobra distinto.
> La Coca se cobra por unidades —tres unidades—.
> El jamón se cobra por peso —0,35 kilos—.
> El combo suma Coca más Agua y le aplica el 10% de descuento.
> Eso pasa solo porque cada clase tiene su propio `precio_final`, sin usar if por tipo.

> **Disponibilidad:** la Coca está disponible porque tiene stock y está habilitada.
> La deshabilito... y aunque tenga stock, ya no está disponible.
> La vuelvo a habilitar... y otra vez está disponible.

> **Categorías:** la Coca está en Bebidas y también en Gaseosas, pero solo una es la principal.

> **Combo:** el combo tiene Coca y Agua adentro, pero esos productos siguen existiendo por separado. No desaparecen cuando creo el combo.

> **Vidriera:** acá destaco al jamón en el puesto 1. Eso lo hago con `DestacadoVidriera`, lo explico en la pregunta 2.

> **Exportación:** en una sola lista mando mis productos —líneas que empiezan con PROD— y también la ficha de la librería externa —línea POS—. No toqué `libreria_externa.py`.

> **Al final:** Python tira error si intento crear un Producto abstracto o una subclase sin `precio_final`. Eso es bueno: el error aparece al crear el objeto, no después cuando ya lo usé.

---

## Paso 3 — Pregunta 1: composición, agregación y asociación

**La pregunta del parcial:** En Python las tres relaciones se parecen mucho. ¿Cómo sabés cuál usaste? ¿Qué pasa con la parte cuando desaparece el todo?

**Qué hacer:** Casi todo está en `catalogo.py`. `main.py` solo para el combo y, si querés, un ejemplo de unidades.

**Qué decir (intro):**

> En Python casi todo se ve igual: una clase guarda otra adentro.
> Yo me fijo en **quién crea a quién** y **si la parte sigue viva cuando borro el todo**.

**Composición** — en `catalogo.py`, mostrá las líneas **80** y **120** (`ProductoCategoria` lo crea el Producto adentro).

> **Composición:** el Producto **crea** el vínculo ProductoCategoria. El cliente no instancia ProductoCategoria solo.
> Si desaparece el producto, desaparecen esas clasificaciones con él.

**Agregación** — en `main.py` líneas **76-78** (armás el combo con Coca y Agua que ya existían). Después en `catalogo.py` línea **186**.

> **Agregación:** los componentes viven **antes** del combo. Si borro el combo, Coca y Agua siguen existiendo.

**Asociación** — en `catalogo.py` líneas **14-18**, **65**, **78** y **100-103**. Opcional: en `main.py` **43-45** y **51-56** (creás la unidad aparte y se la pasás al producto).

> **Línea 65:** en el constructor de Producto, `unidad_venta` es un parámetro **opcional** (`UnidadMedida` o `None`). Quien crea el producto —por ejemplo en `main`— puede pasarme una unidad que **ya existía**; acá no instancio `UnidadMedida`.
>
> **Línea 78:** acá **guardo** esa referencia en `_unidad_venta`. Solo apunto al objeto de afuera; no lo creo ni lo destruyo con el producto.
>
> **Asociación:** Producto y UnidadMedida se **relacionan**, pero cada uno tiene vida propia. El producto **no es dueño** de la unidad como en composición.
> En la demo, cuando exportás, ves `/ u` o `/ kg`: eso sale de `precio_publicado` (líneas **100-103**).

---

## Paso 4 — Pregunta 2: ProductoDestacado

**La pregunta del parcial:** ¿ProductoDestacado queda como subclase o lo cambiás? ¿Por qué? ¿Con qué lo reemplazaste?

**Qué hacer:**
- **`catalogo.py`** líneas **198-215** (`DestacadoVidriera`)
- **`main.py`** línea **84** (ejemplo en demo)
- **`uml/modelo_final.md`** (diagrama)

**Qué decir:**

> Saqué `ProductoDestacado` como subclase de Producto.
>
> **¿Por qué?** Porque "destacado" no es un tipo de producto.
> Un producto **es** simple, **es** por peso o **es** combo.
> Pero "estar en la vidriera" es otra cosa: es ponerle un cartel a un producto que ya existe.
>
> Si hiciera una subclase, tendría que repetir lógica de precio y no podría destacar fácil un combo o un producto por peso.
>
> **¿Con qué lo reemplacé?** Con la clase `DestacadoVidriera`.
> Guarda el producto y el número de orden — en **`catalogo.py` línea 207** (`_orden_vidriera`).
> En **`main.py` línea 84** destaco al jamón en el puesto 1.
>
> Así cualquier producto puede destacarse sin inventar una subclase nueva.

---

## Paso 5 — Pregunta 3: Protocol vs ABC

**La pregunta del parcial:** Exportable se pide con Protocol. ¿Qué pasaría con una ABC? ¿Por qué Producto sí usa ABC?

**Qué hacer:**
1. En **`catalogo.py`**: `Exportable` (líneas 10-11) y `exportar_catalogo` (línea 218).
2. En **`libreria_externa.py`**: mostrá que no tiene cambios (ficha externa).

**Qué decir:**

> `Exportable` lo hice con **Protocol**.
> Eso significa: no hace falta heredar. Si la clase tiene el método `exportar()`, ya sirve.

> **¿Qué pasaría con una ABC y sin tocar la librería?**
> Mal. Porque `FichaPuntoDeVenta` está en `libreria_externa.py` y ese archivo **no se puede modificar**.
> Entonces esa ficha no podría heredar de mi ABC.
> No podría meter productos y fichas externas en la misma lista, y eso rompe el requerimiento.

> **¿Por qué Producto sí usa ABC?**
> Porque Producto es mío. Yo controlo esa jerarquía.
> En **`catalogo.py` líneas 57 y 131-132** dejo `precio_final` como método abstracto.
> Si alguien crea una subclase y olvida implementarlo, Python tira `TypeError` al instanciar —lo vimos al final de la demo—.
> El error aparece temprano, en el constructor.

> El Protocol me deja mezclar mis productos con objetos de afuera en **`catalogo.py` línea 218** (`exportar_catalogo`), sin forzar herencia.

---

## Paso 6 — Pregunta 4: diagrama vs decisiones propias

**La pregunta del parcial:** ¿Qué copiaste del diagrama y qué tuviste que decidir vos?

**Qué hacer:** Abrí **dos pestañas**:
1. **`uml/modelo_final.md`** — el dibujo UML (clases y flechas). Vista previa con `Ctrl + Shift + V` si querés verlo renderizado.
2. **`catalogo.py`** — donde está implementado el código. Acá vas a mostrar las decisiones concretas.

**Qué decir:**

> **Lo que está en el diagrama** (`uml/modelo_final.md`) **y también en el código** (`catalogo.py`):
> Producto abstracto, las tres subclases, ProductoCategoria, Categoria, UnidadMedida inmutable y DestacadoVidriera en lugar de ProductoDestacado.

> **Lo que el diagrama no detalla y yo resolví en código** — mostrás **`catalogo.py`**:

> **Decisión 1 — DestacadoVidriera**
> En el UML se ve la clase suelta, sin herencia de Producto.
> En código: **`catalogo.py` líneas 198 a 215**.

> **Decisión 2 — Precio del combo**
> El UML solo dice que existe ProductoCombo; no dice cómo se calcula el precio.
> En código: **`catalogo.py` línea 177** — sumo el precio de cada componente y aplico el descuento. No escribo un número fijo a mano.

> **Decisión 3 — Stock del combo**
> El UML no aclara si el combo tiene stock propio.
> En código: **`catalogo.py` líneas 166 y 182** — el combo recibe `stock_cantidad` aparte del stock de Coca y Agua.

> **Decisión 4 — Formato de exportar**
> El UML marca Exportable como Protocol, pero no el texto exacto.
> En código: **`catalogo.py` líneas 134 a 135** — formato `PROD|nombre|precio|disponible`.

> Cierro mostrando que **`uml/modelo_final.md`** y **`catalogo.py`** dicen lo mismo: el diagrama es el mapa, el código es la implementación.

---

## Paso 7 — Cierre (30 segundos)

**Qué hacer:** Dejá de compartir pantalla. Mirá a cámara.

**Qué decir:**

> Listo, eso es todo.
>
> El proyecto corre con Python común, sin librerías extra.
> No modifiqué `libreria_externa.py`.
>
> Gracias.

---

## Recordatorio rápido — orden del video

| Paso | Qué hacés | Tiempo aprox. |
|------|-----------|---------------|
| 0 | Preparar archivos y probar cámara | 2 min |
| 1 | Presentarte | 1 min |
| 2 | Correr `python main.py` y comentar | 2-3 min |
| 3 | Pregunta 1 — relaciones | 2-3 min |
| 4 | Pregunta 2 — ProductoDestacado | 2 min |
| 5 | Pregunta 3 — Protocol vs ABC | 2 min |
| 6 | Pregunta 4 — diagrama | 2 min |
| 7 | Despedida | 30 seg |

**Total:** entre 10 y 15 minutos.
