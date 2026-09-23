# Metodología de Sistemas II – Unidad 3: Verificación y Validación

**Curso Moodle:** Metodología de Sistemas II (id 52)  
**Sección:** Práctica → *Trabajo Práctico – Verificación y Validación*

Son **3 entregas** (documentos / evidencias según cada consigna), no un solo ZIP como en U2.

| TP | Consigna local | Entrega en Moodle |
|----|----------------|-------------------|
| Semana 1 – DoD y gobernanza | `tp1-dod/consigna.pdf` | [Entrega TP Nº 1 – DoD](https://tup.sied.utn.edu.ar/mod/assign/view.php?id=17628) |
| Semana 2 – Testing y contratos | `tp2-testing-contratos/consigna.pdf` | [Entrega TP Nº 2 – Testing](https://tup.sied.utn.edu.ar/mod/assign/view.php?id=20416) |
| Semana 3 – Automatización y blindaje | `tp3-automatizacion/consigna.pdf` | [Entrega TP Nº 3 – Calidad](https://tup.sied.utn.edu.ar/mod/assign/view.php?id=20417) |

Texto extraído del PDF: `consigna.txt` en cada carpeta.

## Qué pide cada práctica (resumen)

### TP 1 – Gobernanza y Definition of Done

1. Redactar una **DoD** formal con 6 criterios: compilación/integridad, pruebas automatizadas, umbral de cobertura, revisión por pares, gobernanza de estilo, documentación técnica.
2. **Plantilla de Issue** en Markdown (título, descripción, pasos para reproducir, esperado vs observado, evidencias).
3. **Sistema de labels** (mínimo bug, technical-debt, documentation, feature) con justificación técnica.

### TP 2 – Testing práctico y contratos

1. **Patrón AAA** (Arrange–Act–Assert) en tests unitarios sobre una función de tu sistema.
2. **Informe** Stub vs Mock en integración con API de pagos externa.
3. **Branch vs statement coverage** sobre un condicional complejo + casos para 100% branch coverage.

### TP 3 – Automatización de calidad y blindaje

1. **Pre-commit hook** que ejecute formatter, linter y tests; explicar qué pasa en consola si falla.
2. **Auditoría estática** sobre código de mala calidad (métricas, refactor, dependencias).
3. **Informe de Calidad en Verde**: PR↔Issue, logs del hook, reporte de cobertura, análisis estático.

## Estado

| TP | Estado |
|----|--------|
| TP 1 | ✅ `Viruel_Nicolas_TP1_DoD.zip` |
| TP 2 | ✅ `Viruel_Nicolas_TP2_Testing.zip` |
| TP 3 | ✅ `Viruel_Nicolas_TP3_Calidad.zip` |

Moodle también lista recursos *Ejemplo de Resolución* (TP 1–3); si no tienen archivo adjunto en REST, abrirlos desde la pestaña Práctica en el campus.
