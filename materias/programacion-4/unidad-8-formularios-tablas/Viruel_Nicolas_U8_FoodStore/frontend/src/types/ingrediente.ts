export interface Ingrediente {
  id: number;
  nombre: string;
  descripcion: string | null;
  unidad_medida_id: number;
  created_at: string;
  updated_at: string;
  deleted_at: string | null;
}

export interface IngredienteInput {
  nombre: string;
  descripcion: string;
  unidad_medida_id: number;
}
