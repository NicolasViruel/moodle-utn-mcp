# Solución de referencia — TP Integrador Unidad 3 (POO)

Implementación profesional del TP. **La programación ofrece múltiples caminos**: esta es
*una* forma correcta, no la única. La entrega de un estudiante puede ser igualmente válida
si cumple los requisitos, aplica buenas prácticas y funciona.

## Qué resuelve cada archivo

| Archivo | Qué contiene |
|---|---|
| `figuras.py` | Dominio completo resuelto (Partes 1 a 4): ABC, Protocol, composición, agregación, asociación, copia defensiva. |
| `parte1_diagnostico.py` | El código de partida **ya corregido**: los 8 java-ismos desactivados y el ruido limpio. |
| `demo_sintomas.py` | Demostración reproducible de 2 síntomas (default mutable y atributo de clase mutable), antes/después. |
| `libreria_externa.py` | `PlanoCAD`, la clase de un tercero. **Sin modificar** (idéntica a la del código de partida). |
| `main.py` | Demo ejecutable: taller con 4 polígonos, etiquetas, `exportar_todo`, inventario, y a la vista composición / agregación / falla temprana. |
| `informe.md` | Informe modelo: tabla de los 8 java-ismos, equivalencias y respuestas a las preguntas obligatorias. |
| `uml/modelo_final.md` | Diagrama de clases final (Mermaid), coherente con el código. |

## Cómo ejecutarlo

```
python main.py            # demo completa
python demo_sintomas.py   # los 2 síntomas de la Parte 1
python parte1_diagnostico.py
```

Requiere solo Python 3.12+ (biblioteca estándar: `abc`, `dataclasses`, `typing`, `math`).
No usa dependencias externas.

## Puntos clave

- Los **8 java-ismos** corregidos, cada uno con la inversión conceptual que lo explica.
- `@property` aplicado **solo donde hay lógica** (la validación de `Lado.longitud`).
- Composición, agregación y asociación distinguidas **por ciclo de vida**, no por sintaxis.
- Copia defensiva en `Poligono.lados()` y `Taller.inventario()`.
- `Poligono` como **ABC con falla temprana** al construir.
- `Etiqueta` como `@dataclass(frozen=True)`.
- Contrato `Exportable` como **Protocol**: `PlanoCAD` lo cumple sin heredar.
- `PoligonoRegular` **rediseñado**: reemplazado por el `@classmethod regular(...)`.
