export interface ProductoIngrediente {
  ingrediente_id: number;
  cantidad: string | number;
}

export interface Producto {
  id: number;
  nombre: string;
  descripcion: string | null;
  precio_base: string | number;
  imagenes_url: string[];
  disponible: boolean;
  categoria_ids: number[];
  ingredientes: ProductoIngrediente[];
  created_at: string;
  updated_at: string;
  deleted_at: string | null;
}

export interface ProductoInput {
  nombre: string;
  descripcion: string;
  precio_base: number;
  imagenes_url: string[];
  disponible: boolean;
  categoria_ids: number[];
}
