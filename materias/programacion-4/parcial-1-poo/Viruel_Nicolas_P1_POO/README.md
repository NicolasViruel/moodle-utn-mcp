# Parcial 1 — Food Store (POO)

**Alumno:** Nicolás Viruel  
**Materia:** Programación IV  
**Entrega:** `Viruel_Nicolas_P1_POO.zip`

## Archivos

| Archivo | Rol |
|---------|-----|
| `catalogo.py` | Dominio completo (Req. 1–4) |
| `libreria_externa.py` | Ficha de tercero — **no modificar** |
| `main.py` | Demo ejecutable (Req. 5) |
| `uml/modelo_final.md` | Diagrama Mermaid con decisión R3 |
| `link_video.txt` | Link al video de defensa (10–15 min) |

## Ejecución

```bash
cd Viruel_Nicolas_P1_POO
python main.py
```

Solo Python 3.12+ estándar. Sin dependencias externas.

## Decisiones de diseño

- **ProductoDestacado:** se rediseñó con `DestacadoVidriera` (asociación), porque destacar no implica un «es-un» Producto distinto; permite destacar simples, por peso o combos.
- **ProductoCombo.precio_base:** se deriva al construir como precio unitario del combo con descuento.
- **ProductoCombo.stock:** stock propio del combo (no se deriva de componentes).

