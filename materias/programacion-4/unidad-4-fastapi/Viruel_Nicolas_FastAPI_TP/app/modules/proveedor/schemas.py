from typing import Optional

from pydantic import BaseModel, Field


class ProveedorBase(BaseModel):
    codigo: str = Field(..., min_length=1, example="PROV-001")
    razon_social: str = Field(..., min_length=3, example="Distribuidora Norte SA")
    cuit: str = Field(..., min_length=11, max_length=15, example="30-71234567-8")
    email: str = ""
    telefono: str = ""
    activo: bool = True


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorRead(ProveedorBase):
    id: int


class ProveedorUpdate(BaseModel):
    codigo: Optional[str] = Field(None, min_length=1)
    razon_social: Optional[str] = Field(None, min_length=3)
    cuit: Optional[str] = Field(None, min_length=11, max_length=15)
    email: Optional[str] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None
