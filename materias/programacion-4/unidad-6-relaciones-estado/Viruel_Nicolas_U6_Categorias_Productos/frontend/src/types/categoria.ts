export interface Categoria {
  id: number;
  nombre: string;
  descripcion: string;
}

export type CategoriaInput = Omit<Categoria, "id">;
