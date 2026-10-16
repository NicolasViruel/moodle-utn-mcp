import type { Categoria } from "../types/categoria";
import type { Producto } from "../types/producto";

type Props = {
  producto: Producto;
  categorias: Categoria[];
  onEdit: (producto: Producto) => void;
  onDelete: (id: number) => void;
};

export function ProductoCard({ producto, categorias, onEdit, onDelete }: Props) {
  const nombres = categorias
    .filter((c) => producto.categoria_ids.includes(c.id))
    .map((c) => c.nombre);

  return (
    <article className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-start justify-between gap-2">
        <h3 className="text-lg font-semibold text-slate-900">{producto.nombre}</h3>
        <span
          className={`rounded-full px-2 py-0.5 text-xs font-medium ${
            producto.disponible ? "bg-emerald-100 text-emerald-700" : "bg-slate-200 text-slate-600"
          }`}
        >
          {producto.disponible ? "Disponible" : "No disponible"}
        </span>
      </div>
      <p className="mt-2 text-sm text-slate-600">{producto.descripcion || "Sin descripción"}</p>
      <p className="mt-2 text-sm font-medium text-indigo-700">
        ${Number(producto.precio_base).toLocaleString("es-AR")}
      </p>
      <p className="mt-1 text-xs text-slate-500">
        {nombres.length > 0 ? nombres.join(" · ") : "Sin categorías"}
      </p>
      <div className="mt-4 flex gap-2">
        <button
          type="button"
          onClick={() => onEdit(producto)}
          className="rounded-lg bg-amber-500 px-3 py-1.5 text-sm font-medium text-white hover:bg-amber-600"
        >
          Editar
        </button>
        <button
          type="button"
          onClick={() => onDelete(producto.id)}
          className="rounded-lg bg-rose-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-rose-700"
        >
          Eliminar
        </button>
      </div>
    </article>
  );
}
