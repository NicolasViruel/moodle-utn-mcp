# IAD – Semana 5 (Unidad 2 – Transformación de variables)

**Alumno:** Nicolás Viruel · **Comisión:** 10 (Grupo J)

## Qué pide Moodle esta semana

| # | Actividad | Entrega | Estado |
|---|-----------|---------|--------|
| 1 | Actividad · Transformación de variables (lectura + infografía) | Solo lectura en campus | Vos en Moodle |
| 2 | **Práctica S5** · Transformación de variables (**Python**) | No se sube; conservar notebook | ✅ Run All OK |
| 3 | **TPI Entrega 2** · Limpieza, preparación y transformación | Subir `.ipynb` | ✅ Listo |
| 4 | Autoevaluación U2 (≥ 90 %) | Quiz Moodle | Pendiente – vos |
| 5 | Encuesta de cierre U2 | Moodle | Pendiente – vos |

**Plazo TPI Entrega 2:** domingo 6/09/2026 23:59  
**Archivo a subir:** `Viruel_Nicolas_10_Entrega2.ipynb`  
**Actividad Moodle:** S5 · TPI · Entrega 2 (assign cmid 17419)

## Estructura

```
semana-5/
├── README.md
├── build_semana5.py
├── datos/
│   ├── diamonds.csv
│   ├── penguins.csv
│   └── hotel_booking_TPI_grupo_J.csv
├── materiales/
│   └── S5_Lectura.pdf
└── notebooks/
    ├── S5_Transformacion_de_Variables_Python.ipynb   # Práctica obligatoria
    └── Viruel_Nicolas_10_Entrega2.ipynb              # TPI Entrega 2
```

## Regenerar y probar

```bash
cd materias/iad/semana-5
python build_semana5.py
cd notebooks
python -m jupyter nbconvert --to notebook --execute --inplace S5_Transformacion_de_Variables_Python.ipynb
python -m jupyter nbconvert --to notebook --execute --inplace Viruel_Nicolas_10_Entrega2.ipynb
```

## Práctica S5 – consignas autónomas (Penguins)

1. Observación del dataset (filas, columnas, tipos, describe).
2. Limpieza **solo de nulos**.
3. Transformaciones:
   - `flipper_length_category` (4 cuantiles)
   - One-hot de `island` → `island_torgersen`, `island_biscoe`, `island_dream`
   - `bill_length_minmax` (Min-Max)
   - `body_mass_standard` (z-score)
   - `bill_ratio` = longitud / profundidad del pico
4. Bitácora con 4+ decisiones justificadas.

## TPI Entrega 2 – contenido obligatorio

- Identificación, carga reproducible, copia de trabajo
- Diagnóstico de calidad (faltantes, duplicados, inválidos, atípicos)
- Transformaciones: derivadas (`total_nights`, `total_guests`, `estimated_stay_amount`, `family_booking`), segmentos de `lead_time`, temporales, codificación categórica, Min-Max y estandarización
- Bitácora + dataset preparado documentado
