# Backend — FOOD STORE (Unidad 8)

**Alumno:** Nicolás Viruel — Programación IV — Unidad 8

FastAPI con persistencia en memoria. El módulo **Pedido** usa la arquitectura
Models · Schemas · Repository · Unit of Work · Service · Router.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m fastapi dev app/main.py
```

- Docs: http://127.0.0.1:8000/docs
- CORS: `http://localhost:5173`

## REST Client

- `tests/pedidos.http` — CRUD Pedido + DetallePedido (HU-07)
- `tests/productos.http` — catálogo (categorías, productos, ingredientes)

## Notas

- Un pedido exige al menos un detalle (RN-12).
- PUT `/pedido/{id}` actualiza el **estado**.
- Los datos viven en memoria (RN-15): al reiniciar vuelve el seed.
