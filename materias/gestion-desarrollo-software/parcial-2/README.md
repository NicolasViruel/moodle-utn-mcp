# GDS — Evaluación Parcial 2 (caso LogiExpress)

- **Moodle:** curso 54, sección "Evaluaciones", assign cmid **21911** "GDS - Segundo parcial".
- **Ventana:** 16/10/2026 08:00 → **16/10/2026 23:00** (apertura = cierre el mismo día).
- **Entrega:** 1 archivo **.pdf**, máx. 2 MB. Individual. Habilita la "Constancia Segundo Parcial" al marcarse como realizada.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `consigna.pdf` / `consigna.txt` | Enunciado oficial (GDS-PARCIAL2.pdf) y su texto extraído. |
| `parcial-2_Nicolas_Viruel.md` | Resolución completa en Markdown (fuente). |
| `parcial-2_Nicolas_Viruel.pdf` | **Archivo a subir** (4 páginas, ~39 KB). |
| `build_pdf.py` | Genera el PDF desde el .md con fpdf2 (tablas en grilla). |
| `assign-meta.json` | Metadatos del assign (fechas, restricciones de archivo). |

Regenerar: `PYTHONPATH=/tmp/pypkgs python3 build_pdf.py` (o `pip install fpdf2` y ejecutar directo).

## Resumen de respuestas

- **P1 CPM:** duración 16 días; ruta crítica A→B→C→E→F; H(D) = 2. Elem. 1 entregable interno, Elem. 2 hito, Elem. 3 entregable externo.
- **P2:** métrica Lead Time / tiempo sin cambios de estado vs. historial (más Velocity); Crash Costing = comprimir agregando recursos a tareas críticas al menor costo; criterios: seniority/especialidad y gestión de restricciones/disponibilidad.
- **P3:** src/, docs/, tests/, README.md; pilar CI/CD.
- **P4:** A → manual de instalación; B → manual de usuario; riesgos IA: inventa pasos (alucinaciones) y omite advertencias críticas / desconoce contexto interno.
