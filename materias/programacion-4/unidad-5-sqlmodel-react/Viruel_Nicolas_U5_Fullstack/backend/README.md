# Backend — Gestor de Productos (SQLModel + PostgreSQL)

**Alumno:** Nicolás Viruel · Programación IV · Unidad 5

## Requisitos

- Python 3.12+
- Docker (PostgreSQL) o PostgreSQL local

## Puesta en marcha

Desde la carpeta **`backend`** (donde está este README y `.env.example`):

```powershell
cd "...\Viruel_Nicolas_U5_Fullstack\backend"
Copy-Item .env.example .env
docker compose up -d
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Documentación: http://127.0.0.1:8000/docs

## Capas

- `routers.py` — HTTP
- `services.py` — reglas de negocio (409 nombre duplicado, 404)
- `repository.py` — SQLModel Session
- `models.py` — tabla PostgreSQL
- `schemas.py` — Pydantic (422)

## Pruebas

- `tests/productos.http`
- `tests/postman_productos.json`
