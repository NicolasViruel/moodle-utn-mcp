# IAD – Semana 12 · Unidad 5 (interpretación y primer modelo)

**Alumno:** Nicolás Viruel · **Comisión:** 10 (Grupo J)  
**Ventana Moodle:** 19–25 oct 2026

Recorrido elegido: **SQL + Python**.

## TPI · Entrega 5 (evaluativa)

| Campo | Valor |
|-------|--------|
| Moodle | **S12 · TPI · Entrega 5 · Primer modelo predictivo e interpretación inicial** (assign `17433`) |
| Plazo | domingo **25/10/2026 23:59** |
| Archivos | 2 · máx. 20 MB en total |
| 1 | `Viruel_Nicolas_10_Entrega5.ipynb` (copia ejecutada en la raíz de esta carpeta) |
| 2 | `Declaracion-uso-IA-TPI-IAD_Nicolas_Viruel.pdf` (misma carpeta; original en `tpi/`) |

### Checklist rúbrica (antes de subir)

- [x] Identifica estudiante, comisión 10 y dataset `hotel_booking_TPI_grupo_J.csv`
- [x] Ejecuta de punta a punta (SQL DuckDB + Python / sklearn)
- [x] Predictores justificados; exclusiones por fuga (`assigned_room_type`, `booking_changes`)
- [x] Train/test reproducible; imputación y dummies solo con train
- [x] `DecisionTreeClassifier(max_depth=3)`
- [x] Predicciones vs. resultado real visibles
- [x] Interpretación + ≥ 2 limitaciones
- [x] Sin métricas formales (Unidad 6)
- [x] Declaración de IA en PDF

## Material descargado

| Qué | Archivo |
|-----|---------|
| Apunte | `apuntes/S12-Apunte-interpretacion-generalizacion-limitaciones.pdf` |
| Actividad 1 | `actividades/S12-A1-Interpretacion-SQL-Python.ipynb` |
| Actividad 2 | `actividades/S12-A2-Limitaciones-SQL-Python.ipynb` |
| Práctica obligatoria | `practica/S12-Practica-Obligatoria-SQL-Python.ipynb` |

Las actividades y la práctica **no se suben** con el TPI; conviene completarlas en Moodle (cuestionario, autoevaluación ≥ 90 % y encuesta) para habilitar la semana siguiente.

## Estructura

```
semana-12/
├── README.md
├── build_semana12.py
├── Viruel_Nicolas_10_Entrega5.ipynb          # copia ejecutada para subir
├── datos/hotel_booking_TPI_grupo_J.csv
├── notebooks/Viruel_Nicolas_10_Entrega5.ipynb
├── tpi/Declaracion-uso-IA-TPI-IAD_Nicolas_Viruel.pdf
├── apuntes/
├── actividades/
└── practica/
```

## Regenerar y probar

```bash
cd materias/iad/semana-12
python build_semana12.py
cd notebooks
python -m jupyter nbconvert --to notebook --execute --inplace Viruel_Nicolas_10_Entrega5.ipynb
PYTHONPATH=/tmp/pypkgs python ../tpi/build_declaracion_ia.py
```
