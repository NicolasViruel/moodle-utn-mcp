import type { PaginatedResponse } from "../types/categoria";
import type { Ingrediente, IngredienteInput } from "../types/ingrediente";
import { apiFetch } from "./api";

export const ingredientesKeys = {
  all: ["ingredientes"] as const,
  list: () => [...ingredientesKeys.all, "list"] as const,
};

export function listarIngredientes() {
  return apiFetch<PaginatedResponse<Ingrediente>>("/ingredientes/?limit=100");
}

export function crearIngrediente(input: IngredienteInput) {
  return apiFetch<Ingrediente>("/ingredientes/", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export function actualizarIngrediente(id: number, input: IngredienteInput) {
  return apiFetch<Ingrediente>(`/ingredientes/${id}`, {
    method: "PUT",
    body: JSON.stringify(input),
  });
}

export function eliminarIngrediente(id: number) {
  return apiFetch<void>(`/ingredientes/${id}`, { method: "DELETE" });
}
