from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.core.schemas import AuditRead, PaginatedResponse


class ProductoIngredienteInput(BaseModel):
    """Ingrediente asociado a un producto con su cantidad (en la unidad del ingrediente)."""

    ingrediente_id: int = Field(gt=0)
    cantidad: Decimal = Field(gt=0, max_digits=10, decimal_places=3, examples=["250"])


class ProductoIngredienteRead(ProductoIngredienteInput):
    pass


class ProductoCategoriaRead(BaseModel):
    producto_id: int
    categoria_id: int
    es_principal: bool


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=150, examples=["Pizza Napolitana"])
    descripcion: str | None = Field(default=None, max_length=2000)
    # RN-07: precio >= 0
    precio_base: Decimal = Field(ge=0, max_digits=10, decimal_places=2, examples=["9500.00"])
    # RN-09: lista de cadenas, puede estar vacía
    imagenes_url: list[str] = Field(default_factory=list)
    # RN-08
    disponible: bool = True

    @field_validator("nombre")
    @classmethod
    def nombre_no_vacio(cls, value: str) -> str:
        # RN-06
        value = value.strip()
        if not value:
            raise ValueError("El nombre no puede estar vacío ni contener solo espacios")
        return value


class ProductoCreate(ProductoBase):
    # RN-19: obligatorio y con al menos una categoría.
    categoria_ids: list[int] = Field(min_length=1, examples=[[1]])
    # RN-20: opcional.
    ingredientes: list[ProductoIngredienteInput] = Field(default_factory=list)

    @field_validator("categoria_ids")
    @classmethod
    def sin_duplicados(cls, value: list[int]) -> list[int]:
        return list(dict.fromkeys(value))


class ProductoUpdate(ProductoBase):
    """PUT: datos completos; categoria_ids / ingredientes reemplazan TODAS las relaciones si se envían (RN-12, RN-21)."""

    categoria_ids: list[int] | None = Field(default=None, min_length=1)
    ingredientes: list[ProductoIngredienteInput] | None = None

    @field_validator("categoria_ids")
    @classmethod
    def sin_duplicados(cls, value: list[int] | None) -> list[int] | None:
        return None if value is None else list(dict.fromkeys(value))


class ProductoRead(ProductoBase, AuditRead):
    id: int
    categoria_ids: list[int]
    ingredientes: list[ProductoIngredienteRead]


class ProductoPaginatedResponse(PaginatedResponse[ProductoRead]):
    pass
