# IAD – Semana 10 · Unidad 4 (EDA)

**Alumno:** Nicolás Viruel · **Comisión:** 10 (Grupo J)  
**Ventana Moodle:** 5–11 oct 2026

## Hoja de ruta obligatoria

| Orden | Actividad | Qué hacer |
|------|-----------|-----------|
| 1 | **Act. 1** · Comparación entre grupos | Notebook NSFG · `S10-A1-SQL-Python.ipynb` (Moodle) |
| 2 | **Act. 2** · Interpretación y límites | Notebook NSFG · `S10-A2-SQL-Python.ipynb` |
| 3 | **Cuestionario** Act. 1 y 2 | 3 MC + 1 desarrollo (copiá/adaptá conclusión de Act. 2) |
| 4 | **TPI Entrega 4** | Subir notebook hotel (abajo) |
| 5 | **Autoevaluación** U4 | ≥ **90 %** |
| 6 | **Encuesta** cierre U4 | Obligatoria para **Semana 11** |

Para habilitar S11: intento completo del cuestionario + autoevaluación ≥90 % + encuesta.  
La corrección del desarrollo del cuestionario **no** bloquea el avance.

## TPI · Entrega 4 (evaluativa)

| Campo | Valor |
|-------|--------|
| Moodle | **S10 · TPI · Entrega 4** (assign cmid `17429`) |
| Archivo | `Viruel_Nicolas_10_Entrega4.ipynb` |
| Subir desde | `materias/iad/semana-10/` (copia ejecutada) o `../semana-9/notebooks/` |
| Formato | Un `.ipynb` ejecutable de punta a punta · SQL + Python |
| Aprobación | ≥ 6/10 · hasta 2 intentos |

Consigna completa: label **Presentación de la Entrega 4** en Moodle.

### Checklist rúbrica (antes de subir)

- [ ] Ejecuta desde cero con el CSV en `../datos/`
- [ ] Tres hipótesis claras (§7) + SQL + gráficos + interpretación (§8)
- [ ] Variables candidatas justificadas (§9.1)
- [ ] Tres hallazgos + ≥2 limitaciones (§9.2–9.3)
- [ ] No confundir asociación/causalidad ni “probabilidad” sin modelo

## Regenerar notebook TPI

```bash
cd materias/iad/semana-9
python build_semana9.py
cd notebooks
python -m jupyter nbconvert --to notebook --execute --inplace Viruel_Nicolas_10_Entrega4.ipynb
```
