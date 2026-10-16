import type { Categoria } from "../types/categoria";
import type { Producto } from "../types/producto";
import { ProductoCard } from "./ProductoCard";

type Props = {
  productos: Producto[];
  categorias: Categoria[];
  onEdit: (producto: Producto) => void;
  onDelete: (id: number) => void;
};

export function ProductoList({ productos, categorias, onEdit, onDelete }: Props) {
  if (productos.length === 0) {
    return (
      <p className="rounded-lg border border-dashed border-slate-300 bg-white p-8 text-center text-slate-500">
        No hay productos cargados. Creá el primero con el botón “Nuevo producto”.
      </p>
    );
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {productos.map((producto) => (
        <ProductoCard
          key={producto.id}
          producto={producto}
          categorias={categorias}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
