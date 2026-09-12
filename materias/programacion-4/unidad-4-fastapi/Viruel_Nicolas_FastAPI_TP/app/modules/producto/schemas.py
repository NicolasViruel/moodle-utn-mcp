from pydantic import BaseModel, Field
from typing import Optional


class ProductoBase(BaseModel):
    nombre: str = Field(..., example="Silla de Oficina")
    categoria: str = Field(..., pattern=r"^[A-Z]{3}-\d{2}$", example="MUE-01")
    precio: float = Field(gt=0, example=150.50)
    stock: int = Field(ge=0, example=20)
    stock_minimo: int = Field(ge=0, example=5)
    activo: bool = True


class ProductoCreate(ProductoBase):
    pass  # Exige todos los campos obligatorios de Base


class ProductoUpdate(BaseModel):
    # Opcional: Se usa si en el futuro se implementa PATCH (actualización parcial)
    nombre: Optional[str] = None
    categoria: Optional[str] = Field(None, pattern=r"^[A-Z]{3}-\d{2}$")
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    stock_minimo: Optional[int] = Field(None, ge=0)
    activo: Optional[bool] = None


class ProductoRead(ProductoBase):
    id: int  # Contrato de salida: siempre incluye el ID generado


class ProductoStockResponse(BaseModel):
    stock: int
    bajo_stock_minimo: bool
    activo: bool
