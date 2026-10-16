# Programación IV — Unidad 7 (Server State y Navegación)

| Item | Detalle |
|------|---------|
| Moodle | **Entrega TP Unidad 7** (assign `16201`) |
| Consigna | `consigna.pdf` / `consigna.txt` |
| UML | `UML_FOOD_STORE.svg` |

## Entrega

**Un solo archivo `.zip`** (máx. 2 MB) con dos carpetas adentro:

- `frontend/` — React + TypeScript + TanStack Query + React Router
- `backend/` — FastAPI (Models–Schemas–Service–Router)

Nombre sugerido: `Viruel_Nicolas_U7_FoodStore.zip`

Antes de comprimir: **sin** `node_modules`, **sin** `.venv`, **sin** `__pycache__`, **sin** `dist`.

El zip listo para Moodle está en esta carpeta.

## Cómo correrlo

```bash
# Backend
cd Viruel_Nicolas_U7_FoodStore/backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m fastapi dev app/main.py

# Frontend (otra terminal)
cd Viruel_Nicolas_U7_FoodStore/frontend
npm install
npm run dev
```

App en http://localhost:5173 → abre en `/categorias`.
API en http://127.0.0.1:8000/docs.
REST Client: `backend/tests/productos.http`.
