from sqlmodel import Field, SQLModel


class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=1, max_length=120, index=True)
    descripcion: str = Field(default="", max_length=500)
    precio: float = Field(ge=0)
