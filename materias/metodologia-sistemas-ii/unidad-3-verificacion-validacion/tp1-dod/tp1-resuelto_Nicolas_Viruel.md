# TP1 – Gobernanza y Definition of Done

**Materia:** Metodología de Sistemas II  
**Unidad 3:** Verificación y Validación  
**Alumno:** Nicolás Viruel  

---

## Contexto del equipo

Equipo de cuatro desarrolladores sobre un producto web con API REST (Node.js/TypeScript), frontend React y base PostgreSQL. El flujo de trabajo usa ramas por feature, pull requests hacia `main`, pipeline de integración continua y revisiones obligatorias antes de fusionar. La DoD siguiente aplica a **cualquier cambio** que pretenda integrarse a la rama principal.

---

## 1. Definition of Done (DoD)

Un ítem de trabajo (historia, bugfix o refactor) se considera **terminado** solo cuando cumple **todos** los criterios siguientes. Si uno falla, el PR permanece abierto o vuelve a desarrollo.

### 1.1 Integridad de compilación

- El proyecto **compila o construye sin errores** en el entorno estándar del equipo (mismas versiones de runtime y dependencias declaradas en el lockfile).
- No se introducen warnings nuevos de compilación categorizados como error en CI.
- Migraciones de base de datos (si existen) aplican en limpio sobre el esquema de desarrollo.

**Evidencia:** job de CI `build` en verde en el commit del PR.

### 1.2 Validación de pruebas automatizadas

- La suite completa de pruebas automatizadas (unitarias e integración acordadas para el módulo tocado) **pasa al 100%** en CI.
- No se deshabilitan tests (`skip`, `@Ignore`) salvo incidencia registrada con plan de reactivación y fecha.
- Para correcciones de defectos, existe al menos **un test de regresión** que fallaba antes del fix y pasa después.

**Evidencia:** job `test` en verde; enlace al reporte de la ejecución en el PR.

### 1.3 Umbrales mínimos de cobertura de código

- Cobertura de **líneas** del módulo modificado: **≥ 80%**.
- Cobertura de **ramas** en código nuevo o alterado: **≥ 70%** (prioridad en condicionales y manejo de errores).
- Si el cambio es solo documentación o configuración sin lógica ejecutable, el responsable documenta en el PR la excepción y un revisor la valida.

**Evidencia:** reporte de cobertura adjunto en CI; diff de cobertura no empeora el baseline global del repositorio.

### 1.4 Revisión por pares obligatoria

- Mínimo **una aprobación** de un revisor distinto del autor.
- El revisor verifica requisitos funcionales, impacto en contratos públicos (API) y adherencia a esta DoD.
- Comentarios bloqueantes resueltos o convertidos en issues follow-up con etiqueta acordada.

**Evidencia:** aprobación registrada en la plataforma de código; conversación de revisión archivada en el PR.

### 1.5 Gobernanza de estilo

- Código formateado con la herramienta oficial del repo (p. ej. Prettier, Black) sin cambios manuales inconsistentes.
- Linter estático sin violaciones nuevas de severidad **error**; warnings nuevos justificados en el PR.
- Convenciones de nombres, estructura de carpetas y commits (Conventional Commits o estándar del equipo) respetadas.

**Evidencia:** jobs `lint` y `format-check` en verde.

### 1.6 Sustento de la documentación técnica

- Cambios en endpoints, modelos de datos o variables de entorno **actualizan** README técnico, OpenAPI/Swagger o runbook correspondiente.
- Decisiones de diseño no obvias quedan en ADR breve o sección “Notas” del PR.
- Changelog o release notes actualizados si el cambio es visible para usuarios o operaciones.

**Evidencia:** diff de documentación en el mismo PR o issue enlazado; enlace explícito en la descripción del PR.

### Declaración de cumplimiento (uso en PR)

El autor completa en cada pull request:

> Confirmo que este cambio cumple la DoD del equipo: build OK, tests OK, cobertura dentro de umbral, revisión obtenida, lint/format OK, documentación actualizada.

---

## 2. Plantilla de incidencia (Issue Template)

La plantilla está en **`plantilla_incidencia.md`** (formato Markdown compatible con GitHub/GitLab). Resume los campos exigidos para eliminar ambigüedad:

| Campo | Propósito |
|-------|-----------|
| Título | Identificación rápida con prefijo de tipo |
| Descripción técnica | Alcance, componente y severidad |
| Pasos para reproducir | Secuencia verificable por un tercero |
| Comportamiento observado vs esperado | Contrato claro de “fallo” |
| Evidencias adjuntas | Logs, capturas, datos de entorno |
| Checklist del reportero | Calidad mínima del reporte |

**Ubicación sugerida en el repositorio del producto:** `.github/ISSUE_TEMPLATE/incidencia.md` (o equivalente en GitLab).

### Texto completo de la plantilla

1. **Título:** `[TIPO] Breve descripción del problema`
2. **Descripción técnica:** componente, capa afectada, impacto.
3. **Pasos exactos para reproducir:** lista numerada verificable.
4. **Comportamiento observado:** hechos medibles y mensajes de error.
5. **Comportamiento esperado:** según requisito o contrato.
6. **Evidencias adjuntas:** tabla con capturas, logs, commit, entorno.
7. **Contexto adicional:** versión, rama, entorno, enlace a PR.
8. **Checklist del reportero:** reproducción confirmada, sin duplicados, label asignada.

(Archivo editable listo para importar: `plantilla_incidencia.md`.)

---

## 3. Matriz de categorización (Labels)

Sistema mínimo de etiquetas para auditar cumplimiento de la DoD **antes** de integrar código. Cada PR debe llevar **al menos una** etiqueta de tipo de trabajo; los bugs críticos no se fusionan sin etiqueta `bug` y test de regresión.

| Label | Definición | Uso típico | Relación con la DoD pre-merge |
|-------|------------|------------|-------------------------------|
| `bug` | Comportamiento incorrecto respecto a requisito o contrato existente | Regresiones, errores 5xx, cálculos erróneos | Exige **1.2** (tests + regresión) y **1.1**; revisión **1.4** enfocada en impacto |
| `feature` | Nueva capacidad visible o endpoint | Historias de usuario, ampliación de API | Exige **1.3** cobertura en código nuevo, **1.6** documentación de contrato |
| `documentation` | Solo docs, comentarios técnicos o ADR | Manuales, Swagger, README | **1.6** obligatorio; **1.3** puede exceptuarse con justificación en PR |
| `technical-debt` | Mejora interna sin cambio funcional directo | Refactors, deuda de diseño, performance | **1.5** y **1.3** estrictos; no bajar cobertura global; **1.2** intacto |

### Etiquetas auxiliares (recomendadas)

| Label | Función en auditoría |
|-------|----------------------|
| `blocked-dod` | PR marcado automáticamente si falla CI; impide merge hasta retirar la etiqueta |
| `needs-tests` | Falta regresión o cobertura; bloquea revisión favorable |
| `ready-for-review` | Autor declara DoD cumplida; habilita asignación de revisor |

### Flujo de auditoría antes de integrar

1. Al abrir el PR, el autor asigna label de tipo (`bug` / `feature` / `documentation` / `technical-debt`).
2. CI ejecuta build, tests, lint, format y cobertura (**criterios 1.1–1.3 y 1.5**).
3. Si algo falla, se aplica `blocked-dod`; el merge queda deshabilitado por política de rama.
4. Revisor verifica trazabilidad PR ↔ issue, documentación (**1.4 y 1.6**) y etiquetas coherentes.
5. Solo con CI verde, aprobación humana y checklist DoD marcada, se permite el merge a `main`.

---

## Cierre

La DoD convierte criterios de calidad en **condiciones verificables**; la plantilla de incidencias asegura **trazabilidad del defecto**; las labels permiten **filtrar y auditar** qué exigencias aplican a cada cambio antes de integrarlo. Juntos forman la gobernanza mínima para un desarrollo profesional en equipo.
