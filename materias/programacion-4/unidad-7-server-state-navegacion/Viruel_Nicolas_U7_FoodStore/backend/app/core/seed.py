"""Carga inicial de datos.

Las tablas «Catalog» (UnidadMedida) SOLO se cargan desde acá: la API no expone
operaciones de escritura sobre ellas. Además se cargan algunas categorías,
ingredientes y productos de ejemplo para poder probar el frontend de inmediato.
"""

from decimal import Decimal

from app.core import database as db

UNIDADES_MEDIDA = [
    (1, "kilogramo", "kg", "masa"),
    (2, "gramo", "g", "masa"),
    (3, "litro", "L", "volumen"),
    (4, "mililitro", "mL", "volumen"),
    (5, "pieza", "u", "unidad"),
    (6, "docena", "doc", "unidad"),
    (7, "metro cuadrado", "m²", "area"),
]


def _categoria(nombre: str, descripcion: str = "") -> db.CategoriaRow:
    row = db.CategoriaRow(id=db.seq_categoria.next(), nombre=nombre, descripcion=descripcion)
    db.categorias.append(row)
    return row


def _ingrediente(nombre: str, unidad_medida_id: int, descripcion: str | None = None) -> db.IngredienteRow:
    row = db.IngredienteRow(
        id=db.seq_ingrediente.next(),
        nombre=nombre,
        descripcion=descripcion,
        unidad_medida_id=unidad_medida_id,
    )
    db.ingredientes.append(row)
    return row


def _producto(
    nombre: str,
    precio: str,
    categoria_ids: list[int],
    ingredientes: list[tuple[int, str]],
    descripcion: str | None = None,
) -> db.ProductoRow:
    row = db.ProductoRow(
        id=db.seq_producto.next(),
        nombre=nombre,
        descripcion=descripcion,
        precio_base=Decimal(precio),
    )
    db.productos.append(row)
    for index, categoria_id in enumerate(categoria_ids):
        db.producto_categorias.append(
            db.ProductoCategoriaRow(
                producto_id=row.id, categoria_id=categoria_id, es_principal=index == 0
            )
        )
    for ingrediente_id, cantidad in ingredientes:
        db.producto_ingredientes.append(
            db.ProductoIngredienteRow(
                producto_id=row.id, ingrediente_id=ingrediente_id, cantidad=Decimal(cantidad)
            )
        )
    return row


def run() -> None:
    db.reset()

    for id_, nombre, simbolo, tipo in UNIDADES_MEDIDA:
        db.unidades_medida.append(db.UnidadMedidaRow(id=id_, nombre=nombre, simbolo=simbolo, tipo=tipo))

    pizzas = _categoria("Pizzas", "Pizzas a la piedra, masa madre")
    bebidas = _categoria("Bebidas", "Gaseosas, aguas y jugos")
    _categoria("Postres", "Dulces para cerrar la comida")
    veggie = _categoria("Vegetariano", "Sin carne")

    harina = _ingrediente("Harina 000", 1, "Harina de trigo")
    muzza = _ingrediente("Muzzarella", 2)
    tomate = _ingrediente("Salsa de tomate", 4)
    agua = _ingrediente("Agua mineral", 3)

    _producto(
        "Pizza Muzzarella",
        "8500.00",
        [pizzas.id, veggie.id],
        [(harina.id, "0.35"), (muzza.id, "250"), (tomate.id, "120")],
        "Clásica de 8 porciones",
    )
    _producto("Agua sin gas 500 mL", "1500.00", [bebidas.id], [(agua.id, "0.5")])
