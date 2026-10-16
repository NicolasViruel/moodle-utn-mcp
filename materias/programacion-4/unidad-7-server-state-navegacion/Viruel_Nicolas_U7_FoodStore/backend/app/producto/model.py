"""Models «Table» Producto, «Link» ProductoCategoria y «Link» ProductoIngrediente.

Producto
| id            | BIGSERIAL     | PK                        |
| nombre        | VARCHAR(150)  | NN (no único, RN-06)      |
| descripcion   | TEXT          |                           |
| precio_base   | DECIMAL(10,2) | NN, CHECK >= 0 (RN-07)    |
| imagenes_url  | TEXT[]        | (RN-09)                   |
| disponible    | BOOLEAN       | NN, DEFAULT true (RN-08)  |
| created_at / updated_at / deleted_at (auditoría, soft delete)

ProductoCategoria (PK compuesta)
| producto_id | BIGINT | PK, FK -> Producto.id  |
| categoria_id| BIGINT | PK, FK -> Categoria.id |
| es_principal| BOOLEAN| NN, DEFAULT false      |
| created_at  | TIMESTAMPTZ | NN                |

ProductoIngrediente (PK compuesta)
| producto_id   | BIGINT        | PK, FK -> Producto.id    |
| ingrediente_id| BIGINT        | PK, FK -> Ingrediente.id |
| cantidad      | DECIMAL(10,3) | NN, CHECK > 0            |
| created_at    | TIMESTAMPTZ   | NN                       |
"""

from app.core.database import ProductoCategoriaRow, ProductoIngredienteRow, ProductoRow

__all__ = ["ProductoRow", "ProductoCategoriaRow", "ProductoIngredienteRow"]
