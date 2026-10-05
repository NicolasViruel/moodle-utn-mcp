# GDS — Unidad 5 (Artefactos y documentación automatizada)

| Item | Detalle |
|------|---------|
| Moodle | **Unidad 5 - Práctica** (cmid `14969`, instance `694`) |
| Entrega | PDF único (`.pdf`, máx. 2 MB) |
| Entregable local | `tp-resuelto.pdf` |

## Material local

- `apuntes/` — PDFs de las tres actividades (descargados del aula).
- `consigna.pdf` / `consigna.txt` — se generan al desbloquear la tarea (ver abajo).

## Descargar consigna (después del cuestionario 3)

Desde la raíz del repo:

```bash
node tmp-fetch-gds-u5.mjs
```

Generar entrega:

```bash
python build_pdf.py
```

Entregable: `tp-resuelto.pdf`
