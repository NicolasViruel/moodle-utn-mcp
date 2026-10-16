"""Model «Table» Categoria (ver UML FOOD STORE).

| Columna      | Tipo         | Restricciones          |
|--------------|--------------|------------------------|
| id           | BIGSERIAL    | PK                     |
| nombre       | VARCHAR(100) | UQ, NN                 |
| descripcion  | TEXT         | NN, DEFAULT ""         |
| created_at   | TIMESTAMPTZ  | NN  (auditoría)        |
| updated_at   | TIMESTAMPTZ  | NN  (auditoría)        |
| deleted_at   | TIMESTAMPTZ  | NULL = activa (soft delete) |
"""

from app.core.database import CategoriaRow

__all__ = ["CategoriaRow"]
