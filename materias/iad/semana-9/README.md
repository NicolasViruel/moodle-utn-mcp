# IAD – Semana 9 / 10 · TPI Entrega 4 (EDA)

**Alumno:** Nicolás Viruel · **Comisión:** 10 (Grupo J)

## Entrega Moodle

| Item | Detalle |
|------|---------|
| Actividad | **S10 · TPI · Entrega 4** · Análisis exploratorio (cmid `17429`) |
| Archivo | `Viruel_Nicolas_10_Entrega4.ipynb` |
| Formato | Un solo `.ipynb` ejecutable de punta a punta |

## Contenido del notebook

- **Secciones 1–7:** avance Semana 9 (EDA univariado, SQL + Python, sin comparar grupos por cancelación salvo frecuencias de `is_canceled`).
- **Secciones 8–9:** cierre Semana 10 (comparaciones, tasas, gráficos, hallazgos y limitaciones).

## Estructura

```
semana-9/
├── README.md
├── build_semana9.py
├── datos/hotel_booking_TPI_grupo_J.csv
└── notebooks/Viruel_Nicolas_10_Entrega4.ipynb
```

## Regenerar y probar

```bash
cd materias/iad/semana-9
python build_semana9.py
cd notebooks
python -m jupyter nbconvert --to notebook --execute --inplace Viruel_Nicolas_10_Entrega4.ipynb
```

Requisitos: `pandas`, `duckdb`, `matplotlib`, `seaborn`, `jupyter`.

Antes de subir a Moodle: ejecutar todo el notebook y revisar que los gráficos y tablas se vean bien.
