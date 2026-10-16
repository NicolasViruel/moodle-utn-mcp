"""Model «Table» Ingrediente (módulo Catálogo de Productos).

| id               | BIGSERIAL     | PK                    |
| nombre           | VARCHAR(120)  | NN                    |
| descripcion      | TEXT          |                       |
| unidad_medida_id | BIGINT        | FK -> UnidadMedida.id |
| created_at / updated_at / deleted_at (auditoría, soft delete)
"""

from app.core.database import IngredienteRow

__all__ = ["IngredienteRow"]
