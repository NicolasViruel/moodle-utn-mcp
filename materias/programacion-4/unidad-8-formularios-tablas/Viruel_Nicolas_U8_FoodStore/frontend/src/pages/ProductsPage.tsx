import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { ColumnDef } from "@tanstack/react-table";
import { DataTable } from "../components/DataTable";
import { ProductoModal } from "../components/ProductoModal";
import { formatError } from "../lib/errors";
import { categoriasKeys, listarCategorias } from "../services/categorias";
import { ingredientesKeys, listarIngredientes } from "../services/ingredientes";
import {
  actualizarProducto,
  crearProducto,
  eliminarProducto,
  listarProductos,
  productosKeys,
} from "../services/productos";
import type { Producto, ProductoInput } from "../types/producto";

export function ProductsPage() {
  const queryClient = useQueryClient();
  const [modalOpen, setModalOpen] = useState(false);
  const [selected, setSelected] = useState<Producto | null>(null);
  const [formError, setFormError] = useState<string | null>(null);

  const productosQuery = useQuery({ queryKey: productosKeys.list(), queryFn: listarProductos });
  const categoriasQuery = useQuery({ queryKey: categoriasKeys.list(), queryFn: listarCategorias });
  const ingredientesQuery = useQuery({ queryKey: ingredientesKeys.list(), queryFn: listarIngredientes });

  const invalidate = () => queryClient.invalidateQueries({ queryKey: productosKeys.all });

  const crearMutation = useMutation({
    mutationFn: crearProducto,
    onSuccess: () => {
      void invalidate();
      closeModal();
    },
    onError: (err: Error) => setFormError(formatError(err)),
  });

  const actualizarMutation = useMutation({
    mutationFn: ({ id, input }: { id: number; input: ProductoInput }) =>
      actualizarProducto(id, input),
    onSuccess: () => {
      void invalidate();
      closeModal();
    },
    onError: (err: Error) => setFormError(formatError(err)),
  });

  const eliminarMutation = useMutation({
    mutationFn: eliminarProducto,
    onSuccess: () => void invalidate(),
  });

  const openCreate = () => {
    setSelected(null);
    setFormError(null);
    setModalOpen(true);
  };

  const openEdit = (producto: Producto) => {
    setSelected(producto);
    setFormError(null);
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setSelected(null);
    setFormError(null);
  };

  const handleSubmit = (input: ProductoInput) => {
    setFormError(null);
    if (selected) actualizarMutation.mutate({ id: selected.id, input });
    else crearMutation.mutate(input);
  };

  const columns = useMemo<ColumnDef<Producto, unknown>[]>(
    () => [
      { accessorKey: "nombre", header: "Nombre" },
      {
        accessorKey: "descripcion",
        header: "Descripción",
        cell: (info) => info.getValue() || "—",
      },
      {
        accessorKey: "precio_base",
        header: "Precio",
        cell: (info) => `$${Number(info.getValue()).toLocaleString("es-AR")}`,
      },
      {
        id: "ingredientes",
        header: "Ingredientes",
        enableSorting: false,
        cell: ({ row }) =>
          row.original.ingredientes.length === 0
            ? "—"
            : row.original.ingredientes.map((i) => `#${i.ingrediente_id}`).join(", "),
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
                if (!window.confirm("¿Eliminar este producto?")) return;
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

  const listError = productosQuery.error
    ? formatError(productosQuery.error)
    : eliminarMutation.error
      ? formatError(eliminarMutation.error)
      : null;

  return (
    <main className="mx-auto max-w-6xl space-y-6 px-4 py-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold">Productos</h2>
          <p className="text-sm text-slate-600">TanStack Table + Form + Query</p>
        </div>
        <button
          type="button"
          onClick={openCreate}
          className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700"
        >
          + Nuevo producto
        </button>
      </div>
      {listError && (
        <div className="rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800">{listError}</div>
      )}
      {productosQuery.isPending ? (
        <p className="text-slate-600">Cargando productos…</p>
      ) : (
        <DataTable
          data={productosQuery.data?.items ?? []}
          columns={columns}
          emptyMessage="No hay productos. Creá el primero con el botón superior."
        />
      )}
      <ProductoModal
        key={selected ? `edit-${selected.id}` : modalOpen ? "create" : "closed"}
        isOpen={modalOpen}
        selected={selected}
        categorias={categoriasQuery.data?.items ?? []}
        ingredientes={ingredientesQuery.data?.items ?? []}
        isSaving={crearMutation.isPending || actualizarMutation.isPending}
        formError={formError}
        onClose={closeModal}
        onSubmit={handleSubmit}
      />
    </main>
  );
}
