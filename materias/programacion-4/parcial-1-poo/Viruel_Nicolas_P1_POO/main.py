"""Demo ejecutable del catálogo Food Store."""

from __future__ import annotations

from catalogo import (
    Categoria,
    DestacadoVidriera,
    Producto,
    ProductoCombo,
    ProductoPorPeso,
    ProductoSimple,
    UnidadMedida,
    exportar_catalogo,
)
from libreria_externa import FichaPuntoDeVenta


def _demostrar_falla_temprana() -> None:
    print("=== Falla temprana (ABC) ===")
    try:
        Producto(  # type: ignore[abstract]
            nombre="Abstracto",
            precio_base=1,
            categoria_principal=Categoria("Test"),
        )
    except TypeError as exc:
        print(f"OK Producto abstracto: {exc}")

    class ProductoIncompleto(Producto):
        pass

    try:
        ProductoIncompleto(
            nombre="Incompleto",
            precio_base=1,
            categoria_principal=Categoria("Test"),
        )
    except TypeError as exc:
        print(f"OK subclase sin precio_final: {exc}")


def main() -> None:
    unidad_unidad = UnidadMedida("unidad", "u", "unidad")
    unidad_kg = UnidadMedida("kilogramo", "kg", "masa")
    unidad_l = UnidadMedida("litro", "L", "volumen")

    bebidas = Categoria("Bebidas", "Bebidas frías y calientes")
    gaseosas = Categoria("Gaseosas")
    fiambreria = Categoria("Fiambrería")

    coca = ProductoSimple(
        nombre="Coca Cola 500ml",
        precio_base=1200.0,
        categoria_principal=bebidas,
        stock_cantidad=50,
        unidad_venta=unidad_unidad,
    )
    coca.clasificar_en(gaseosas)

    jamon = ProductoPorPeso(
        nombre="Jamón cocido",
        precio_base=8500.0,
        categoria_principal=fiambreria,
        stock_cantidad=12.5,
        unidad_venta=unidad_kg,
    )

    agua = ProductoSimple(
        nombre="Agua mineral 2L",
        precio_base=900.0,
        categoria_principal=bebidas,
        stock_cantidad=30,
        unidad_venta=unidad_l,
    )

    combo = ProductoCombo(
        nombre="Combo merienda",
        componentes=[coca, agua],
        descuento=0.10,
        categoria_principal=bebidas,
        stock_cantidad=20,
    )

    destacado = DestacadoVidriera(jamon, orden_vidriera=1)

    print("=== Precios finales ===")
    for producto, cantidad in [(coca, 3), (jamon, 0.35), (combo, 2)]:
        print(f"{producto.nombre}: {producto.precio_final(cantidad):.2f} (cantidad={cantidad})")

    print("\n=== Disponibilidad ===")
    print(f"{coca.nombre} disponible: {coca.disponible}")
    coca.deshabilitar()
    print(f"{coca.nombre} tras deshabilitar: {coca.disponible}")
    coca.habilitar()
    print(f"{coca.nombre} tras habilitar: {coca.disponible}")

    print("\n=== Composición / agregación ===")
    print(f"Clasificaciones de {coca.nombre}: {[v.categoria.nombre for v in coca.categorias()]}")
    print(f"Principal: {coca.categoria_principal().nombre}")
    tupla_componentes = combo.componentes()
    print(f"Componentes del combo: {[p.nombre for p in tupla_componentes]}")
    print("Los componentes existen fuera del combo:", coca.nombre, agua.nombre)

    print("\n=== Vidriera (rediseño sin herencia) ===")
    print(f"Destacado #{destacado.orden_vidriera}: {destacado.producto.nombre}")

    ficha = FichaPuntoDeVenta("POS-001", "Promo fin de semana")
    exportables: list = [coca, jamon, combo, agua, ficha]
    print("\n=== Exportación unificada ===")
    for linea in exportar_catalogo(exportables):
        print(linea)

    _demostrar_falla_temprana()


if __name__ == "__main__":
    main()
