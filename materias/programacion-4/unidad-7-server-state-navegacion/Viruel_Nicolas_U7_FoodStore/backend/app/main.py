from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.categoria.router import router as categoria_router
from app.core.seed import run as seed_run
from app.health.router import router as health_router
from app.ingrediente.router import router as ingrediente_router
from app.producto.router import router as producto_router
from app.unidad_medida.router import router as unidad_medida_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    seed_run()
    yield


app = FastAPI(
    title="FOOD STORE — Catálogo de Productos",
    description=(
        "API del TP Unidad 7 (Programación IV). "
        "CRUD de Categorías, Productos e Ingredientes; catálogo de Unidades de Medida "
        "(solo lectura). Persistencia en memoria con borrado lógico y auditoría."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(ingrediente_router)
app.include_router(unidad_medida_router)
