# TRABAJO PRÁCTICO – UNIDAD 4
## Planificación y calendarización de un proyecto de software

**Materia:** Gestión de Desarrollos de Software  
**Unidad 4:** Planificación, calendarización e iteraciones  
**Alumno:** Nicolás Viruel

---

## Caso (recordatorio)

Módulo con 6 actividades:

| Actividad | Duración (días) | Predecesoras |
|-----------|-----------------|--------------|
| A | 3 | — |
| B | 4 | A |
| C | 5 | B |
| D | 2 | A |
| E | 4 | C, D |
| F | 3 | E |

---

## 1. Hitos y entregables

### Hitos SMART (3)

| Hito | Día (fin de) | SMART | Ubicación en cronograma |
|------|--------------|-------|-------------------------|
| **H1 – Diseño validado** | 3 | **S:** aprobación del diseño funcional del módulo. **M:** acta firmada por responsable funcional. **A:** depende solo de A (3 d). **R:** habilita desarrollo B/C/D. **T:** día 3. | Al finalizar **A** |
| **H2 – Integración core** | 12 | **S:** módulos principales (B y C) integrados en ambiente de prueba. **M:** build estable + smoke tests OK. **A:** ruta A-B-C. **R:** desbloquea pruebas integradas E. **T:** día 12. | Al finalizar **C** |
| **H3 – Go-live** | 19 | **S:** módulo desplegado y aceptado. **M:** acta de aceptación del cliente interno. **A:** camino crítico completo. **R:** cierre del proyecto. **T:** día 19. | Al finalizar **F** |

### Entregables

| Entregable | Tipo | Justificación |
|------------|------|---------------|
| **Plan de pruebas + matriz trazabilidad requisitos–casos** | **Interno** | Sirve al equipo QA/dev para verificar el módulo; no se entrega al cliente final; mejora calidad del proceso (material: entregables de gestión interna). |
| **Paquete instalable del módulo + nota de versión** | **Externo** | Es el producto observable por el usuario/cliente del módulo; materializa el valor del proyecto hacia afuera (entregable externo). |

**Ubicación tentativa:** plan de pruebas al cierre de **B** (día 7); paquete instalable en **H3** (día 19).

---

## 2. CPM – Tiempos tempranos, tardíos y holguras

Convención: **IT/FT** = inicio/fin temprano; **IL/FL** = inicio/fin tardío; holgura = **IL − IT**.

| Actividad | Duración | Predecesoras | IT | FT | IL | FL | Holgura |
|-----------|----------|--------------|----|----|----|----|---------|
| A | 3 | — | 0 | 3 | 0 | 3 | **0** |
| B | 4 | A | 3 | 7 | 3 | 7 | **0** |
| C | 5 | B | 7 | 12 | 7 | 12 | **0** |
| D | 2 | A | 3 | 5 | 10 | 12 | **7** |
| E | 4 | C, D | 12 | 16 | 12 | 16 | **0** |
| F | 3 | E | 16 | 19 | 16 | 19 | **0** |

---

## 3. Camino crítico y holguras

- **Duración total del proyecto:** **19 días**.
- **Camino crítico:** **A → B → C → E → F** (3 + 4 + 5 + 4 + 3 = 19).
- **Holgura cero:** la actividad está en el camino crítico; cualquier retraso se traslada **1:1** a la fecha de fin del proyecto.
- **Actividad D (holgura 7):** puede iniciar hasta el día **10** (en lugar del día 3) y aun así terminar a tiempo para **E** (día 12). **Sí se puede retrasar** hasta 7 días sin mover la fecha final, porque D es paralela a la cadena B–C y es más corta que el tiempo disponible entre el fin de A y el inicio de E.

---

## 4. Diagrama de Gantt

Escala: días **0 a 19** (eje horizontal). Cada `█` = un día de trabajo. `|` = hito (H1, H2, H3).

```
Día:  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
      |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
A     █  █  █  H1
B              █  █  █  █
C                       █  █  █  █  █  H2
D              █  █
E                                    █  █  █  █
F                                              █  █  █  H3
```

**Dependencias respetadas:** B y D tras A; C tras B; E tras C y D; F tras E.

**Captura:** ver archivo **`gantt-u4.png`** (misma información, generado para adjuntar en Moodle si se pide imagen aparte).

---

## 5. Iteraciones ágiles y gestión dinámica con IA

### Hitos en marcos ágiles

En Agile los “hitos” se reparten en **releases** o **Sprints**: no suele haber un Gantt fijo de meses, sino **objetivos de incremento** por iteración. Los hitos SMART se **mapean a Sprint Goals** o revisiones de release (por ejemplo, H2 ≈ “incremento potencialmente entregable” al cierre del sprint que integra B+C). Al **final de cada Sprint** se evalúa el **Incremento** frente al **Definition of Done**: demo con stakeholders, feedback, burndown/velocity y decisión de priorizar el backlog siguiente.

### CPM en contextos ágiles

| | |
|--|--|
| **Beneficio** | Visualiza dependencias técnicas reales (p. ej. no probar E hasta integrar C y D) y anticipa el **tiempo mínimo** aunque el trabajo se reparta en sprints. |
| **Desafío** | El alcance cambia por sprint; un CPM estático **se desactualiza** y puede contradecir la flexibilidad del backlog si se usa como contrato rígido. |

### IA predictiva en el cronograma

La **IA predictiva** analiza histórico (velocity, cycle time, fallos en CI) para **reforecast** de fechas y detectar **cuellos de botella** antes de que ocurran. **Ejemplo (material):** si el equipo suele tardar 40 % más en tareas que tocan integración (como E), el sistema sugiere mover recursos de D (holgura 7) hacia C antes del día 10, o alerta que el Sprint objetivo para H2 es poco probable según la velocidad de los últimos tres sprints.

---
