import type { Categoria, CategoriaInput, PaginatedResponse } from "../types/categoria";
import { apiFetch } from "./api";

export const categoriasKeys = {
  all: ["categorias"] as const,
  list: () => [...categoriasKeys.all, "list"] as const,
};

export function listarCategorias() {
  return apiFetch<PaginatedResponse<Categoria>>("/categorias/?limit=100");
}

export function crearCategoria(input: CategoriaInput) {
  return apiFetch<Categoria>("/categorias/", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function actualizarCategoria(id: number, input: CategoriaInput) {
  return apiFetch<Categoria>(`/categorias/${id}`, {
    method: "PUT",
    body: JSON.stringify(input),
  });
}

export function eliminarCategoria(id: number) {
  return apiFetch<void>(`/categorias/${id}`, { method: "DELETE" });
}
