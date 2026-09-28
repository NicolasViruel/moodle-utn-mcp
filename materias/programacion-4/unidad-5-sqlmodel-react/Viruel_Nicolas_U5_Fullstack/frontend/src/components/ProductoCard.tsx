import type { Producto } from "../types/producto";

export interface ProductoCardProps {
  producto: Producto;
}

export function ProductoCard({ producto }: ProductoCardProps) {
  return (
    <article className="flex flex-col rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:shadow-md">
      <h3 className="text-lg font-semibold text-slate-900">{producto.nombre}</h3>
      <p className="mt-2 flex-1 text-sm text-slate-600">{producto.descripcion}</p>
      <p className="mt-4 text-2xl font-bold text-emerald-600">
        ${producto.precio.toFixed(2)}
      </p>
    </article>
  );
}
