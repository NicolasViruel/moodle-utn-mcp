from fastapi import APIRouter

from app.core import database as db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", summary="Liveness")
def health():
    return {"status": "ok"}


@router.get("/db", summary="Readiness: el catálogo en memoria está inicializado")
def health_db():
    return {
        "status": "ok",
        "unidades_medida": len(db.unidades_medida),
        "categorias": sum(1 for c in db.categorias if c.activo),
        "productos": sum(1 for p in db.productos if p.activo),
        "ingredientes": sum(1 for i in db.ingredientes if i.activo),
    }
