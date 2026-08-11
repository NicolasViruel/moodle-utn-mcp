# Contenido para notebooks TPI – Semana 2

Copiá cada bloque en **celdas Markdown** de Google Colab.  
Creá **dos notebooks** con el mismo contenido base (entrega 1 y maestro).

---

## Celda 1 – Título

```markdown
# TPI – Cancelaciones en reservas hoteleras
**Integrante:** Nicolás Viruel  
**Materia:** Introducción al Análisis de Datos  
**Semana 2:** Organización inicial del trabajo
```

---

## Celda 2 – Descripción del problema

```markdown
## 1. Descripción del problema

Un hotel (o cadena hotelera) necesita entender **por qué los clientes cancelan sus reservas** antes del check-in.

Las cancelaciones generan:
- Pérdida de ingresos esperados
- Habitaciones que quedan vacías sin tiempo de revenderlas
- Dificultad para planificar personal y stock

El objetivo del TPI es **analizar datos históricos de reservas** para identificar patrones asociados a las cancelaciones y, más adelante, apoyar decisiones como políticas de depósito, overbooking o campañas de retención.
```

---

## Celda 3 – Variable objetivo

```markdown
## 2. Variable objetivo: `is_canceled`

- **`is_canceled = 1`** → la reserva **fue cancelada** antes de la estadía.
- **`is_canceled = 0`** → la reserva **no fue cancelada** (el huésped se presentó o completó la estadía según corresponda).

Es una variable **cualitativa binaria** (también se puede tratar como indicador 0/1).

Todo el análisis predictivo del TPI gira en torno a anticipar si una nueva reserva terminará con `is_canceled = 1`.
```

---

## Celda 4 – Preguntas iniciales de análisis

```markdown
## 3. Preguntas iniciales de análisis

1. ¿Qué **porcentaje** de reservas se cancela en el dataset?
2. ¿Las cancelaciones varían según el **tipo de deposito**, **canal de reserva** o **anticipación** (lead time)?
3. ¿Hay diferencias por **temporada**, **tipo de habitación** o **país** del cliente?
4. ¿Clientes **repetidos** cancelan menos que clientes nuevos?
5. ¿Qué variables parecen más relacionadas con `is_canceled` en una primera exploración?
6. ¿Qué decisiones concretas podría tomar el hotel si confirma ciertos patrones?
```

---

## Celda 5 – Organización del trabajo

```markdown
## 4. Organización del notebook

| Notebook | Propósito |
|----------|-----------|
| **Entrega 1** | Documento específico para la primera entrega del TPI |
| **Maestro** | Registro completo de avances, decisiones y resultados de todo el cuatrimestre |

### Próximos pasos (Semana 3)
- Cargar el dataset asignado
- Primer reconocimiento: dimensiones, tipos de variables, valores faltantes
- Estadística descriptiva de `is_canceled` y variables clave

> **Semana 2:** no se carga ni analiza el dataset todavía.
```

---

## Checklist antes de dar por terminado

- [ ] Dos notebooks creados en Colab con nombres claros
- [ ] Contenido en celdas Markdown, ordenado y legible
- [ ] Guardados en carpeta de Drive y abren correctamente
- [ ] Práctica 1 (cuestionario) enviada en Moodle
