from pydantic import BaseModel, ConfigDict


class UnidadMedidaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    simbolo: str
    tipo: str


class UnidadMedidaListResponse(BaseModel):
    items: list[UnidadMedidaRead]
    total: int
