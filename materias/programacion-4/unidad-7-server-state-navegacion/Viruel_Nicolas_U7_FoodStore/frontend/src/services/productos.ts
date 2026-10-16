import type { PaginatedResponse } from "../types/categoria";
import type { Producto, ProductoInput } from "../types/producto";
import { apiFetch } from "./api";

export const productosKeys = {
  all: ["productos"] as const,
  list: () => [...productosKeys.all, "list"] as const,
};

export function listarProductos() {
  return apiFetch<PaginatedResponse<Producto>>("/productos/?limit=100");
}

export function crearProducto(input: ProductoInput) {
  return apiFetch<Producto>("/productos/", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function actualizarProducto(id: number, input: ProductoInput) {
  return apiFetch<Producto>(`/productos/${id}`, {
    method: "PUT",
    body: JSON.stringify(input),
  });
}

export function eliminarProducto(id: number) {
  return apiFetch<void>(`/productos/${id}`, { method: "DELETE" });
}
