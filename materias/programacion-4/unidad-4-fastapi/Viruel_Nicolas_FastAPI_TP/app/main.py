from fastapi import FastAPI

from app.modules.categoria.routers import router as categoria_router
from app.modules.producto.routers import router as producto_router
from app.modules.proveedor.routers import router as proveedor_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="API Integradora - Unidad 4",
        description="Catálogo con Categorías, Productos y Proveedores.",
        version="1.0.0",
    )

    app.include_router(categoria_router)
    app.include_router(producto_router)
    app.include_router(proveedor_router)

    return app

app = create_app()
