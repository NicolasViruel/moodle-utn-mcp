import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { ColumnDef } from "@tanstack/react-table";
import { CategoriaModal } from "../components/CategoriaModal";
import { DataTable } from "../components/DataTable";
import { formatError } from "../lib/errors";
import {
  actualizarCategoria,
  categoriasKeys,
  crearCategoria,
  eliminarCategoria,
  listarCategorias,
} from "../services/categorias";
import type { Categoria, CategoriaInput } from "../types/categoria";

export function CategoriesPage() {
  const queryClient = useQueryClient();
  const [modalOpen, setModalOpen] = useState(false);
  const [selected, setSelected] = useState<Categoria | null>(null);
  const [formError, setFormError] = useState<string | null>(null);

  const query = useQuery({ queryKey: categoriasKeys.list(), queryFn: listarCategorias });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: categoriasKeys.all });

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
    setFormError(null);
    setModalOpen(true);
  };

  const openEdit = (categoria: Categoria) => {
    setSelected(categoria);
    setFormError(null);
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setSelected(null);
    setFormError(null);
  };

  const handleSubmit = (input: CategoriaInput) => {
    setFormError(null);
    if (selected) actualizarMutation.mutate({ id: selected.id, input });
    else crearMutation.mutate(input);
  };

  const columns = useMemo<ColumnDef<Categoria, unknown>[]>(
    () => [
      { accessorKey: "nombre", header: "Nombre" },
      {
        accessorKey: "descripcion",
        header: "Descripción",
        cell: (info) => info.getValue() || "—",
      },
      {
        id: "acciones",
        header: "Acciones",
        enableSorting: false,
        cell: ({ row }) => (
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => openEdit(row.original)}
              className="rounded-lg bg-amber-500 px-3 py-1 text-xs font-medium text-white hover:bg-amber-600"
            >
              Editar
            </button>
            <button
              type="button"
              onClick={() => {
                if (!window.confirm("¿Eliminar esta categoría?")) return;
                eliminarMutation.mutate(row.original.id);
              }}
              className="rounded-lg bg-rose-600 px-3 py-1 text-xs font-medium text-white hover:bg-rose-700"
            >
              Eliminar
            </button>
          </div>
        ),
      },
    ],
    [eliminarMutation],
  );

  const listError = query.error
    ? formatError(query.error)
    : eliminarMutation.error
      ? formatError(eliminarMutation.error)
      : null;

  return (
    <main className="mx-auto max-w-6xl space-y-6 px-4 py-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold">Categorías</h2>
          <p className="text-sm text-slate-600">TanStack Table + Form + Query</p>
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

      {query.isPending ? (
        <p className="text-slate-600">Cargando categorías…</p>
      ) : (
        <DataTable
          data={query.data?.items ?? []}
          columns={columns}
          emptyMessage="No hay categorías cargadas. Creá la primera con el botón “Nueva categoría”."
        />
      )}

      <CategoriaModal
        key={selected ? `edit-${selected.id}` : modalOpen ? "create" : "closed"}
        isOpen={modalOpen}
        selected={selected}
        isSaving={crearMutation.isPending || actualizarMutation.isPending}
        formError={formError}
        onClose={closeModal}
        onSubmit={handleSubmit}
      />
    </main>
  );
}
