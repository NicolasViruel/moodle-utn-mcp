# Guion paso a paso — Video Parcial 1 POO

**Nicolás Viruel · Programación IV · Food Store**

---

## 1. Antes de grabar (5 min)

- Encendé cámara y micrófono.
- Abrí VS Code con `Viruel_Nicolas_P1_POO`.
- Terminal lista con `python main.py`.
- Archivos abiertos: `catalogo.py`, `main.py`, `uml/modelo_final.md`, `libreria_externa.py`.
- Duración: **10 a 15 minutos**.

---

## 2. Intro (1 min) — mirá a cámara

> Hola, soy Nicolás Viruel. Este es el video de defensa del Parcial 1 de Programación IV: el catálogo Food Store en Python. Voy a correr la demo y responder las cuatro preguntas del enunciado sobre mi código.

---

## 3. Demo (2 min) — pantalla

1. Ejecutá `python main.py`.
2. Mostrá **precios finales**: Coca (unidades), jamón (kg), combo (descuento).
3. Mostrá **disponibilidad**: deshabilitar / habilitar Coca.
4. Mostrá **clasificaciones**: Bebidas + Gaseosas.
5. Mostrá **combo**: componentes siguen existiendo afuera.
6. Mostrá **exportación**: PROD| y POS| en la misma lista.
7. Mostrá **falla temprana** TypeError al final.

---

## 4. Pregunta 1 — Relaciones (2-3 min)

Abrí `catalogo.py`.

**Composición** (Producto ↔ ProductoCategoria):
- Línea del `__init__` de Producto: `ProductoCategoria(self, ...)`.
- `clasificar_en` también crea el vínculo adentro.
- El cliente nunca instancia `ProductoCategoria` directo.

**Agregación** (ProductoCombo ↔ componentes):
- El combo recibe productos ya construidos.
- Sobreviven al combo (Coca y Agua siguen existiendo).

**Asociación** (Producto ↔ UnidadMedida):
- `unidad_venta` opcional (puede ser None).
- UnidadMedida es independiente e inmutable.

---

## 5. Pregunta 2 — ProductoDestacado (2-3 min)

- No mantuve herencia de `ProductoDestacado`.
- Criterio **es-un**: destacar no es otro tipo de producto.
- Usé `DestacadoVidriera`: guarda Producto + orden.
- Cualquier producto puede destacarse (simple, peso, combo).

---

## 6. Pregunta 3 — Protocol vs ABC (2-3 min)

- `Exportable` es **Protocol**; nadie hereda.
- `FichaPuntoDeVenta` es externa → no se puede hacer heredar ABC.
- `Producto` sí es **ABC** porque yo controlo las subclases.
- `precio_final` abstracto → falla al construir si falta.

---

## 7. Pregunta 4 — Diagrama vs decisiones (2 min)

**Tal cual:** Producto ABC, 3 subclases, ProductoCategoria, Categoria, UnidadMedida.

**Decisiones propias:**
1. ProductoDestacado → DestacadoVidriera
2. precio_base del combo derivado de componentes
3. stock propio del combo
4. formato libre de exportar()

---

## 8. Cierre (30 seg)

> Proyecto con Python estándar, sin dependencias. Gracias.

---

## 9. Entrega Moodle

1. Subir video → pegar link en `link_video.txt`
2. ZIP `Viruel_Nicolas_P1_POO.zip` (sin `.venv` ni `__pycache__`)
3. Subir en **Evaluaciones → Entrega Parcial 1**
