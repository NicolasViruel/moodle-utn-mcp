# Programación IV — Unidad 4 FastAPI

## Entrega TP (subir a Moodle)

**Carpeta:** `Viruel_Nicolas_FastAPI_TP/`  
**ZIP:** `Viruel_Nicolas.zip` (nombre y apellido, sin `.venv`)

**Moodle:** Práctica → Entrega proyecto FastApi

### Contenido del ZIP

- `app/modules/proveedor/` (routers, schemas, services)
- `app/main.py` con router registrado
- `tests/proveedores.http` + `tests/test_api.http`
- `requirements.txt`
- `README.md`

### Probar local

```bash
cd Viruel_Nicolas_FastAPI_TP
pip install -r requirements.txt
fastapi dev app/main.py
```

Swagger: http://127.0.0.1:8000/docs

### Endpoints proveedores

| Metodo | Ruta | Codigo |
|--------|------|--------|
| POST | /proveedores/ | 201 |
| GET | /proveedores/ | 200 |
| GET | /proveedores/{id} | 200 / 404 |
| PUT | /proveedores/{id} | 200 / 404 / 409 |
| PUT | /proveedores/{id}/desactivar | 200 / 404 / 409 |

Reglas: RN-01 a RN-05 (unicidad codigo, 422, 404, 409 desactivar duplicado).
