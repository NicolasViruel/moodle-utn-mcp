# Backend — FOOD STORE (Catálogo de Productos)

**Alumno:** Nicolás Viruel — Programación IV — Unidad 7

API FastAPI con persistencia en memoria, borrado lógico y auditoría. Arquitectura
Models · Schemas · Service · Router.

## Requisitos

- Python 3.11+

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

## Ejecutar

Desde esta carpeta (`backend/`):

```bash
python -m fastapi dev app/main.py
```

- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health/

CORS habilitado para `http://localhost:5173` y `http://127.0.0.1:5173`.

## REST Client

`tests/productos.http` demuestra:

- CRUD de Productos (HU-06)
- Consulta de relaciones N:M Producto–Categoría y Producto–Ingrediente (HU-07)
- CRUD de Categorías e Ingredientes
- Catálogo de Unidades de Medida (solo GET)
- Validaciones 404 / 409 / 422

## Notas

- Las tablas «Catalog» (UnidadMedida) se cargan desde `app/core/seed.py`. No hay POST/PUT.
- El borrado es lógico (`deleted_at`). Nada se elimina físicamente de las tablas de negocio.
- Al reiniciar el servidor, el catálogo vuelve al estado del seed (RN-16).
