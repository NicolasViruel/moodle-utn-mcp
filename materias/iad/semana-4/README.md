# IAD – Semana 4 (Unidad 2 – Diagnóstico y limpieza)

**Alumno:** Nicolás Viruel · **Comisión:** 10 (Grupo J)

## Estructura de carpetas

```
semana-4/
├── README.md
├── build_semana4.py          # Regenera notebooks (S4 autónoma + TPI E2)
├── datos/
│   ├── titanic.csv
│   ├── google-play-store-apps.csv
│   └── hotel_booking_TPI_grupo_J.csv
└── notebooks/
    ├── S4_Diagnostico_y_limpieza_Python.ipynb   # Práctica obligatoria
    ├── TPI_Entrega2_Nicolas_Viruel.ipynb         # TPI Entrega 2 (nuevo)
    └── TPI_Maestro_Nicolas_Viruel.ipynb          # Documento integrador (referencia)
```

## Checklist obligatorio

| # | Actividad | Archivo / Moodle | Estado |
|---|-----------|------------------|--------|
| 1 | Actividad · Reconocimiento y limpieza | Moodle (lectura ~20 min) | Pendiente – vos en campus |
| 2 | Cuestionario refuerzo (≥ 6/10) | Moodle quiz S4 | Pendiente – **bloquea Semana 5** |
| 3 | Práctica S4 – Diagnóstico y limpieza | `notebooks/S4_Diagnostico_y_limpieza_Python.ipynb` | ✅ Run All OK |
| 4 | TPI – Inicio Entrega 2 | `notebooks/TPI_Entrega2_Nicolas_Viruel.ipynb` | ✅ Run All OK (entrega formal Semana 5) |
| 5 | TPI Maestro sincronizado | `notebooks/TPI_Maestro_Nicolas_Viruel.ipynb` | ✅ Secciones 1–4 + Run All OK |

## Cómo ejecutar

Desde `notebooks/` (los CSV están en `../datos/`):

```bash
jupyter notebook S4_Diagnostico_y_limpieza_Python.ipynb
# o
jupyter notebook TPI_Entrega2_Nicolas_Viruel.ipynb
```

En Colab: subí la carpeta `datos/` y ajustá `DATA_DIR` si hace falta.

**Verificado localmente (Run All):** ambos notebooks ejecutan sin errores con Python 3.14 + pandas + matplotlib.

## Regenerar notebooks

```bash
python build_semana4.py      # S4 autónoma + TPI Entrega 2
python sync_tpi_maestro.py   # Integrar Entregas 1 y 2 en el Maestro
```

## Nota sobre Entrega 2 vs Maestro

- **TPI_Entrega2** = notebook independiente para la entrega parcial (Semana 5).
- **TPI_Maestro** = documento final integrado; las secciones 3–8 se completan progresivamente.
