import { FormEvent, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { ProductoList } from "../components/ProductoList";
import { ProductoModal } from "../components/ProductoModal";
import { ApiError } from "../services/api";
import { categoriasKeys, listarCategorias } from "../services/categorias";
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
  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [precio, setPrecio] = useState("0");
  const [disponible, setDisponible] = useState(true);
  const [categoriaIds, setCategoriaIds] = useState<number[]>([]);
  const [formError, setFormError] = useState<string | null>(null);

  const productosQuery = useQuery({
    queryKey: productosKeys.list(),
    queryFn: listarProductos,
  });

  const categoriasQuery = useQuery({
    queryKey: categoriasKeys.list(),
    queryFn: listarCategorias,
  });

  const invalidate = () =>
    queryClient.invalidateQueries({ queryKey: productosKeys.all });

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
    setNombre("");
    setDescripcion("");
    setPrecio("0");
    setDisponible(true);
    setCategoriaIds([]);
    setFormError(null);
    setModalOpen(true);
  };

  const openEdit = (producto: Producto) => {
    setSelected(producto);
    setNombre(producto.nombre);
    setDescripcion(producto.descripcion ?? "");
    setPrecio(String(producto.precio_base));
    setDisponible(producto.disponible);
    setCategoriaIds([...producto.categoria_ids]);
    setFormError(null);
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setSelected(null);
    setFormError(null);
  };

  const toggleCategoria = (id: number) => {
    setCategoriaIds((prev) =>
      prev.includes(id) ? prev.filter((cid) => cid !== id) : [...prev, id],
    );
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    const trimmed = nombre.trim();
    if (!trimmed) {
      setFormError("El nombre es obligatorio.");
      return;
    }
    if (categoriaIds.length < 1) {
      setFormError("Seleccioná al menos una categoría (RN-19).");
      return;
    }
    const input: ProductoInput = {
      nombre: trimmed,
      descripcion: descripcion.trim(),
      precio_base: Number(precio),
      imagenes_url: selected?.imagenes_url ?? [],
      disponible,
      categoria_ids: categoriaIds,
    };
    setFormError(null);
    if (selected) {
      actualizarMutation.mutate({ id: selected.id, input });
    } else {
      crearMutation.mutate(input);
    }
  };

  const handleDelete = (id: number) => {
    if (!window.confirm("¿Eliminar este producto?")) return;
    eliminarMutation.mutate(id);
  };

  const isSaving = crearMutation.isPending || actualizarMutation.isPending;
  const listError = productosQuery.error
    ? formatError(productosQuery.error)
    : eliminarMutation.error
      ? formatError(eliminarMutation.error)
      : null;

  return (
    <main className="mx-auto max-w-5xl space-y-6 px-4 py-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold">Productos</h2>
          <p className="text-sm text-slate-600">Listado y formulario con TanStack Query</p>
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
        <div className="rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800">
          {listError}
        </div>
      )}

      {productosQuery.isPending ? (
        <p className="text-slate-600">Cargando productos…</p>
      ) : (
        <ProductoList
          productos={productosQuery.data?.items ?? []}
          categorias={categoriasQuery.data?.items ?? []}
          onEdit={openEdit}
          onDelete={handleDelete}
        />
      )}

      <ProductoModal
        isOpen={modalOpen}
        title={selected ? "Editar producto" : "Nuevo producto"}
        nombre={nombre}
        descripcion={descripcion}
        precio={precio}
        disponible={disponible}
        categoriaIds={categoriaIds}
        categorias={categoriasQuery.data?.items ?? []}
        onNombreChange={setNombre}
        onDescripcionChange={setDescripcion}
        onPrecioChange={setPrecio}
        onDisponibleChange={setDisponible}
        onToggleCategoria={toggleCategoria}
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
