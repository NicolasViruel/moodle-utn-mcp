import type { Categoria } from "../types/categoria";
import { CategoriaCard } from "./CategoriaCard";

type Props = {
  categorias: Categoria[];
  onEdit: (categoria: Categoria) => void;
  onDelete: (id: number) => void;
};

export function CategoriaList({ categorias, onEdit, onDelete }: Props) {
  if (categorias.length === 0) {
    return (
      <p className="rounded-lg border border-dashed border-slate-300 bg-white p-8 text-center text-slate-500">
        No hay categorías cargadas. Creá la primera con el botón superior.
      </p>
    );
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {categorias.map((categoria) => (
        <CategoriaCard
          key={categoria.id}
          categoria={categoria}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
