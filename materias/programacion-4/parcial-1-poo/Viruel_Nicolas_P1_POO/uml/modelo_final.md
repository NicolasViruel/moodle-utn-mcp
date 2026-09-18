# Diagrama UML final — Food Store

Decisión R3: **ProductoDestacado no hereda de Producto**. Se reemplaza por `DestacadoVidriera`, que asocia cualquier `Producto` con un orden de vidriera. Un producto destacado no es otro tipo de producto: es el mismo producto con metadata promocional.

```mermaid
classDiagram
    class Exportable {
        <<Protocol>>
        +exportar() str
    }
    class Producto {
        <<abstract>>
        -_nombre str
        -_precio_base float
        -_stock_cantidad float
        -_habilitado bool
        -_unidad_venta UnidadMedida
        -_clasificaciones list
        +nombre str
        +precio_base float
        +unidad_venta UnidadMedida
        +disponible bool
        +precio_publicado str
        +precio_final(cantidad) float
        +habilitar()
        +deshabilitar()
        +clasificar_en(categoria, es_principal)
        +categorias() tuple
        +categoria_principal() Categoria
        +exportar() str
    }
    class ProductoSimple {
        +precio_final(cantidad) float
    }
    class ProductoPorPeso {
        +precio_final(cantidad) float
    }
    class ProductoCombo {
        -_componentes list
        -_descuento float
        +componentes() tuple
        +precio_final(cantidad) float
    }
    class DestacadoVidriera {
        -_producto Producto
        -_orden_vidriera int
        +producto Producto
        +orden_vidriera int
    }
    class ProductoCategoria {
        -_categoria Categoria
        -_es_principal bool
        +categoria Categoria
        +es_principal bool
    }
    class Categoria {
        -_nombre str
        -_descripcion str
        +nombre str
        +descripcion str
    }
    class UnidadMedida {
        <<immutable>>
        +nombre str
        +simbolo str
        +tipo str
    }
    class FichaPuntoDeVenta {
        <<external>>
        +exportar() str
    }
    Producto <|-- ProductoSimple
    Producto <|-- ProductoPorPeso
    Producto <|-- ProductoCombo
    Producto "1" *-- "1..*" ProductoCategoria : composicion
    ProductoCombo "1" o-- "2..*" Producto : agregacion
    Producto "0..*" --> "0..1" UnidadMedida : asociacion
    ProductoCategoria "0..*" --> "1" Categoria
    DestacadoVidriera "1" --> "1" Producto : asociacion
    Producto ..|> Exportable
    FichaPuntoDeVenta ..|> Exportable
```
