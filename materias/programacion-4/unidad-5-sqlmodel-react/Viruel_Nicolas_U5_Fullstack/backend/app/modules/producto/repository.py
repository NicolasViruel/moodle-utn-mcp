from sqlmodel import Session, select

from app.modules.producto.models import Producto


class ProductoRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, producto: Producto) -> Producto:
        self.session.add(producto)
        self.session.commit()
        self.session.refresh(producto)
        return producto

    def list(self, skip: int = 0, limit: int = 50) -> list[Producto]:
        statement = select(Producto).offset(skip).limit(limit)
        return list(self.session.exec(statement).all())

    def get_by_id(self, producto_id: int) -> Producto | None:
        return self.session.get(Producto, producto_id)

    def get_by_nombre(self, nombre: str) -> Producto | None:
        statement = select(Producto).where(Producto.nombre == nombre)
        return self.session.exec(statement).first()

    def update(self, producto: Producto) -> Producto:
        self.session.add(producto)
        self.session.commit()
        self.session.refresh(producto)
        return producto

    def delete(self, producto: Producto) -> None:
        self.session.delete(producto)
        self.session.commit()
