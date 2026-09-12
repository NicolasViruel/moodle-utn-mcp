from pydantic import BaseModel, Field
from typing import Optional


class CategoriaBase(BaseModel):
    codigo: str = Field(..., pattern=r"^[A-Z]{3}-\d{2}$", example="MUE-01")
    descripcion: str = Field(..., min_length=3, example="Muebles de Oficina")
    activo: bool = True


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    codigo: Optional[str] = Field(None, pattern=r"^[A-Z]{3}-\d{2}$")
    descripcion: Optional[str] = Field(None, min_length=3)
    activo: Optional[bool] = None


class CategoriaRead(CategoriaBase):
    id: int
