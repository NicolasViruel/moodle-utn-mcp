import type { Producto } from "../types/producto";
import { ProductoCard } from "./ProductoCard";

export interface ProductoListProps {
  productos: Producto[];
}

export function ProductoList({ productos }: ProductoListProps) {
  return (
    <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {productos.map((producto) => (
        <ProductoCard key={producto.id} producto={producto} />
      ))}
    </section>
  );
}
