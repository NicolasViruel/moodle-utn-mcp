"""Schemas compartidos: auditoría, paginación y parámetros de consulta comunes."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class AuditRead(BaseModel):
    """Campos de auditoría presentes en todas las entidades de negocio."""

    model_config = ConfigDict(from_attributes=True)

    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Respuesta estandarizada para listados paginados."""

    items: list[T]
    total: int
    offset: int
    limit: int

    @property
    def has_more(self) -> bool:  # pragma: no cover - utilitario
        return self.offset + len(self.items) < self.total


class PaginationParams(BaseModel):
    """Parámetros comunes de paginación/filtro validados con Query()."""

    offset: int = 0
    limit: int = 10
    nombre: str | None = None
    incluir_inactivos: bool = False


def pagination_params(
    offset: Annotated[int, Query(ge=0, description="Desplazamiento para paginación")] = 0,
    limit: Annotated[int, Query(ge=1, le=100, description="Cantidad de resultados por página")] = 10,
    nombre: Annotated[str | None, Query(min_length=1, description="Filtro por nombre (búsqueda parcial)")] = None,
    incluir_inactivos: Annotated[bool, Query(description="Incluir registros eliminados (soft delete)")] = False,
) -> PaginationParams:
    return PaginationParams(offset=offset, limit=limit, nombre=nombre, incluir_inactivos=incluir_inactivos)


def paginate(rows: list[T], params: PaginationParams) -> tuple[list[T], int]:
    """Aplica offset/limit sobre una lista ya filtrada. Devuelve (página, total)."""
    total = len(rows)
    page = rows[params.offset : params.offset + params.limit]
    return page, total
