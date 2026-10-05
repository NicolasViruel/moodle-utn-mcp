from pydantic import BaseModel, Field


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    descripcion: str = Field(min_length=1, max_length=500)
    precio_base: str = Field(min_length=1, max_length=32)
    imagen_url: list[str] = Field(default_factory=list)
    disponible: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class ProductoRead(ProductoBase):
    id: int


class ProductoCategoriaCreate(BaseModel):
    producto_id: int = Field(gt=0)
    categoria_id: int = Field(gt=0)


class ProductoCategoriaRead(ProductoCategoriaCreate):
    pass
