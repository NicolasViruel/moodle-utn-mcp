# Código de partida — TP Integrador Unidad 3 (POO)

Este es el **punto de partida** del trabajo práctico. Sin este material no se puede
resolver la Parte 1.

## Qué hay adentro

| Archivo | Qué es | ¿Se modifica? |
|---|---|---|
| `parte1_diagnostico.py` | El dominio Figura / Polígono / Lado funcionando, pero escrito «con acento de Java». Es el objeto de trabajo: lo vas a diagnosticar y corregir. | **Sí** |
| `libreria_externa.py` | La clase `PlanoCAD` de un tercero. No hereda de nada tuyo y **no se modifica nunca**. Es el centro de la Parte 4. | **No. Nunca.** |

## Cómo ejecutarlo

```
python parte1_diagnostico.py
```

Corre de punta a punta sin lanzar un solo error. **No tiene bugs de sintaxis: tiene
acento.** Lo que hay que encontrar son decisiones de diseño heredadas de Java, no
excepciones.

## Lo que tenés que encontrar

- **Exactamente 8 java-ismos de diseño.** Ni 7 ni 9: ocho. Siete están en el checklist
  de la Actividad 4; el octavo no, y esa es justo la diferencia entre *aplicar una lista*
  y *haber entendido el criterio*.
- **Ruido sintáctico** (punto y coma al final de línea, comparaciones contra `True`,
  concatenación con `+` donde va un f-string). También se limpia, pero **no cuenta**
  dentro de los 8.

Seguí las consignas completas en el PDF del TP.
