from pydantic import BaseModel, Field, field_validator

from app.core.schemas import AuditRead, PaginatedResponse


class CategoriaBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100, examples=["Pizzas"])
    # RN-03: descripción opcional, se almacena como cadena vacía si se omite.
    descripcion: str = Field(default="", max_length=2000, examples=["Pizzas a la piedra"])

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, value: str) -> str:
        # RN-01: no puede quedar vacío ni contener solo espacios.
        value = value.strip()
        if not value:
            raise ValueError("El nombre no puede estar vacío ni contener solo espacios")
        return value

    @field_validator("descripcion")
    @classmethod
    def descripcion_trim(cls, value: str) -> str:
        return value.strip()


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    """PUT = reemplazo total, por eso exige los mismos campos que el alta."""


class CategoriaRead(CategoriaBase, AuditRead):
    id: int


class CategoriaPaginatedResponse(PaginatedResponse[CategoriaRead]):
    pass
