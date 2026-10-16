export interface Categoria {
  id: number;
  nombre: string;
  descripcion: string;
  created_at: string;
  updated_at: string;
  deleted_at: string | null;
}

export interface CategoriaInput {
  nombre: string;
  descripcion: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  offset: number;
  limit: number;
}
