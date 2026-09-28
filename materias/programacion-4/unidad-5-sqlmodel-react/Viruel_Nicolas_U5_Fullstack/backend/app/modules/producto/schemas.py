from pydantic import BaseModel, Field, field_validator


class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, examples=["Teclado mecánico"])
    descripcion: str = Field(default="", examples=["Switch rojo, layout ES"])
    precio: float = Field(..., ge=0, examples=[89.99])

    @field_validator("nombre")
    @classmethod
    def nombre_sin_solo_espacios(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("El nombre no puede estar vacío ni contener solo espacios")
        return trimmed


class ProductoUpdate(BaseModel):
    nombre: str = Field(..., min_length=1)
    descripcion: str = Field(default="")
    precio: float = Field(..., ge=0)

    @field_validator("nombre")
    @classmethod
    def nombre_sin_solo_espacios(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("El nombre no puede estar vacío ni contener solo espacios")
        return trimmed


class ProductoRead(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float

    model_config = {"from_attributes": True}
