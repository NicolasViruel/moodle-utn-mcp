import { FormEvent, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { CategoriaList } from "../components/CategoriaList";
import { CategoriaModal } from "../components/CategoriaModal";
import { ApiError } from "../services/api";
import {
  actualizarCategoria,
  categoriasKeys,
  crearCategoria,
  eliminarCategoria,
  listarCategorias,
} from "../services/categorias";
import type { Categoria, CategoriaInput } from "../types/categoria";

export function CategoriasPage() {
  const queryClient = useQueryClient();
  const [modalOpen, setModalOpen] = useState(false);
  const [selected, setSelected] = useState<Categoria | null>(null);
  const [formNombre, setFormNombre] = useState("");
  const [formDescripcion, setFormDescripcion] = useState("");
  const [formError, setFormError] = useState<string | null>(null);

  const categoriasQuery = useQuery({
    queryKey: categoriasKeys.list(),
    queryFn: listarCategorias,
  });

  const invalidate = () =>
    queryClient.invalidateQueries({ queryKey: categoriasKeys.all });

  const crearMutation = useMutation({
    mutationFn: crearCategoria,
    onSuccess: () => {
      void invalidate();
      closeModal();
    },
    onError: (err: Error) => setFormError(formatError(err)),
  });

  const actualizarMutation = useMutation({
    mutationFn: ({ id, input }: { id: number; input: CategoriaInput }) =>
      actualizarCategoria(id, input),
    onSuccess: () => {
      void invalidate();
      closeModal();
    },
    onError: (err: Error) => setFormError(formatError(err)),
  });

  const eliminarMutation = useMutation({
    mutationFn: eliminarCategoria,
    onSuccess: () => void invalidate(),
  });

  const openCreate = () => {
    setSelected(null);
    setFormNombre("");
    setFormDescripcion("");
    setFormError(null);
    setModalOpen(true);
  };

  const openEdit = (categoria: Categoria) => {
    setSelected(categoria);
    setFormNombre(categoria.nombre);
    setFormDescripcion(categoria.descripcion);
    setFormError(null);
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setSelected(null);
    setFormNombre("");
    setFormDescripcion("");
    setFormError(null);
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    const nombre = formNombre.trim();
    if (!nombre) {
      setFormError("El nombre es obligatorio y no puede contener solo espacios.");
      return;
    }
    const input: CategoriaInput = { nombre, descripcion: formDescripcion.trim() };
    setFormError(null);
    if (selected) {
      actualizarMutation.mutate({ id: selected.id, input });
    } else {
      crearMutation.mutate(input);
    }
  };

  const handleDelete = (id: number) => {
    if (!window.confirm("¿Eliminar esta categoría?")) return;
    eliminarMutation.mutate(id);
  };

  const isSaving = crearMutation.isPending || actualizarMutation.isPending;
  const listError = categoriasQuery.error
    ? formatError(categoriasQuery.error)
    : eliminarMutation.error
      ? formatError(eliminarMutation.error)
      : null;

  return (
    <main className="mx-auto max-w-5xl space-y-6 px-4 py-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold">Categorías</h2>
          <p className="text-sm text-slate-600">CRUD con TanStack Query (useQuery / useMutation)</p>
        </div>
        <button
          type="button"
          onClick={openCreate}
          className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700"
        >
          + Nueva categoría
        </button>
      </div>

      {listError && (
        <div className="rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800">
          {listError}
        </div>
      )}

      {categoriasQuery.isPending ? (
        <p className="text-slate-600">Cargando categorías…</p>
      ) : (
        <CategoriaList
          categorias={categoriasQuery.data?.items ?? []}
          onEdit={openEdit}
          onDelete={handleDelete}
        />
      )}

      {formError && modalOpen && (
        <p className="sr-only">{formError}</p>
      )}

      <CategoriaModal
        isOpen={modalOpen}
        title={selected ? "Editar categoría" : "Nueva categoría"}
        nombre={formNombre}
        descripcion={formDescripcion}
        onNombreChange={setFormNombre}
        onDescripcionChange={setFormDescripcion}
        onClose={closeModal}
        onSubmit={handleSubmit}
        isSaving={isSaving}
      />

      {formError && modalOpen && (
        <div className="fixed inset-x-0 bottom-4 z-[60] mx-auto max-w-md rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800 shadow">
          {formError}
        </div>
      )}
    </main>
  );
}

function formatError(err: unknown): string {
  if (err instanceof ApiError) {
    return JSON.stringify({ detail: err.detail });
  }
  if (err instanceof Error) {
    return JSON.stringify({ detail: err.message });
  }
  return JSON.stringify({ detail: "Error desconocido" });
}
