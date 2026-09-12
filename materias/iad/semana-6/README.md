# IAD – Semana 6 (Unidad 3 – Visualización de datos)

**Alumno:** Nicolás Viruel · **Comisión:** 10 (Grupo J)

## Qué pide Moodle esta semana

| # | Actividad | Entrega | Estado |
|---|-----------|---------|--------|
| 1 | Actividades 1 y 2 + cuestionario refuerzo A1 | Quiz Moodle (≥ 6/10) | Pendiente – vos |
| 2 | Práctica S6 Python (Tips + insurance) | No se sube | Pendiente – notebook Moodle |
| 3 | Práctica 1 cuestionario | Quiz Moodle | Pendiente – vos |
| 4 | **TPI Entrega 3** · Visualización | Subir `.ipynb` | ✅ Listo |
| 5 | Encuesta cierre U3 | Moodle | Pendiente – vos |

**Plazo TPI Entrega 3:** domingo 13/09/2026 23:59  
**Archivo a subir:** `Viruel_Nicolas_10_Entrega3.ipynb`  
**Actividad Moodle:** S6 · TPI · Entrega 3 (assign cmid 17421)

## TPI Entrega 3 – contenido

Notebook independiente con:

1. Identificación, carga y preparación mínima del dataset hotelero
2. **3 visualizaciones** con pregunta, justificación del gráfico e interpretación:
   - Cancelaciones por tipo de hotel
   - `lead_time` vs `is_canceled` (boxplot)
   - Tasa de cancelación por `deposit_type` y `market_segment`
3. Cierre con **3 hallazgos** y **1 limitación**

## Estructura

```
semana-6/
├── README.md
├── build_semana6.py
├── datos/hotel_booking_TPI_grupo_J.csv
└── notebooks/Viruel_Nicolas_10_Entrega3.ipynb
```

## Regenerar y probar

```bash
cd materias/iad/semana-6
python build_semana6.py
cd notebooks
python -m jupyter nbconvert --to notebook --execute --inplace Viruel_Nicolas_10_Entrega3.ipynb
```
