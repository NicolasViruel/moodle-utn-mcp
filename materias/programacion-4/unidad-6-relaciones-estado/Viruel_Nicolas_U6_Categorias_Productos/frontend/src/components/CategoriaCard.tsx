import type { Categoria } from "../types/categoria";

type Props = {
  categoria: Categoria;
  onEdit: (categoria: Categoria) => void;
  onDelete: (id: number) => void;
};

export function CategoriaCard({ categoria, onEdit, onDelete }: Props) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="text-lg font-semibold text-slate-900">{categoria.nombre}</h3>
      <p className="mt-2 text-sm text-slate-600">{categoria.descripcion}</p>
      <div className="mt-4 flex gap-2">
        <button
          type="button"
          onClick={() => onEdit(categoria)}
          className="rounded-lg bg-amber-500 px-3 py-1.5 text-sm font-medium text-white hover:bg-amber-600"
        >
          Editar
        </button>
        <button
          type="button"
          onClick={() => onDelete(categoria.id)}
          className="rounded-lg bg-rose-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-rose-700"
        >
          Eliminar
        </button>
      </div>
    </article>
  );
}
