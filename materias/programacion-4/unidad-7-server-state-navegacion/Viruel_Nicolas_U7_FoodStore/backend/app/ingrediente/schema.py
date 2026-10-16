from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.core.schemas import AuditRead, PaginatedResponse


class IngredienteBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=120, examples=["Muzzarella"])
    descripcion: str | None = Field(default=None, max_length=2000)
    unidad_medida_id: int = Field(gt=0, examples=[2])

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El nombre no puede estar vacío ni contener solo espacios")
        return value


class IngredienteCreate(IngredienteBase):
    pass


class IngredienteUpdate(IngredienteBase):
    pass


class IngredienteRead(IngredienteBase, AuditRead):
    id: int


class IngredientePaginatedResponse(PaginatedResponse[IngredienteRead]):
    pass


class IngredienteDeProductoRead(IngredienteRead):
    """Ingrediente asociado a un producto, con la cantidad usada."""

    cantidad: Decimal
