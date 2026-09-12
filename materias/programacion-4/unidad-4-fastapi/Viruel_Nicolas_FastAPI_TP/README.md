# API de catálogo — Módulo Proveedores

**Alumno:** Nicolás Viruel  
**Materia:** Programación IV · Unidad 4

API REST en FastAPI que extiende el proyecto integrador con gestión de proveedores en memoria.

## Requisitos

- Python 3.12+
- Dependencias en `requirements.txt`

## Instalación y ejecución

```bash
pip install -r requirements.txt
fastapi dev app/main.py
```

Documentación interactiva: http://127.0.0.1:8000/docs

## Estructura

```
app/
├── main.py
└── modules/
    ├── categoria/
    ├── producto/
    └── proveedor/    ← módulo agregado
tests/
├── test_api.http
└── proveedores.http
```

## Endpoints de proveedores

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/proveedores/` | Alta de proveedor |
| GET | `/proveedores/` | Listado con paginación y filtro `activo` |
| GET | `/proveedores/{id}` | Detalle por ID |
| PUT | `/proveedores/{id}` | Actualización total |
| PUT | `/proveedores/{id}/desactivar` | Baja lógica |

## Pruebas

Los archivos `.http` en `tests/` cubren casos exitosos y de error (422, 404, 409).
