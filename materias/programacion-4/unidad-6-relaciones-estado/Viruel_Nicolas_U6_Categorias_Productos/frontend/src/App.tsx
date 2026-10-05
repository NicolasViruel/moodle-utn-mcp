import { FormEvent, useCallback, useEffect, useState } from "react";
import { CategoriaList } from "./components/CategoriaList";
import { CategoriaModal } from "./components/CategoriaModal";
import { Navbar } from "./components/Navbar";
import type { Categoria, CategoriaInput } from "./types/categoria";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export default function App() {
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [selected, setSelected] = useState<Categoria | null>(null);
  const [formNombre, setFormNombre] = useState("");
  const [formDescripcion, setFormDescripcion] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const loadCategorias = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE}/categorias/`);
      if (!response.ok) {
        throw new Error(`Error al listar (${response.status})`);
      }
      const data: Categoria[] = await response.json();
      setCategorias(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo conectar con la API");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadCategorias();
  }, [loadCategorias]);

  const openCreate = () => {
    setSelected(null);
    setFormNombre("");
    setFormDescripcion("");
    setModalOpen(true);
  };

  const openEdit = (categoria: Categoria) => {
    setSelected(categoria);
    setFormNombre(categoria.nombre);
    setFormDescripcion(categoria.descripcion);
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setSelected(null);
    setFormNombre("");
    setFormDescripcion("");
  };

  const handleCreate = async (input: CategoriaInput) => {
    const response = await fetch(`${API_BASE}/categorias/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input),
    });
    if (!response.ok) {
      throw new Error("No se pudo crear la categoría");
    }
    await loadCategorias();
  };

  const handleUpdate = async (id: number, input: CategoriaInput) => {
    const response = await fetch(`${API_BASE}/categorias/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input),
    });
    if (!response.ok) {
      throw new Error("No se pudo actualizar la categoría");
    }
    await loadCategorias();
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm("¿Eliminar esta categoría?")) {
      return;
    }
    const response = await fetch(`${API_BASE}/categorias/${id}`, { method: "DELETE" });
    if (!response.ok && response.status !== 204) {
      setError("No se pudo eliminar la categoría");
      return;
    }
    await loadCategorias();
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    const input: CategoriaInput = {
      nombre: formNombre.trim(),
      descripcion: formDescripcion.trim(),
    };
    try {
      if (selected) {
        await handleUpdate(selected.id, input);
      } else {
        await handleCreate(input);
      }
      closeModal();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al guardar");
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <Navbar />
      <main className="mx-auto max-w-5xl space-y-6 px-4 py-8">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold">Categorías</h2>
            <p className="text-sm text-slate-600">CRUD con fetch nativo hacia FastAPI</p>
          </div>
          <button
            type="button"
            onClick={openCreate}
            className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700"
          >
            + Nueva categoría
          </button>
        </div>

        {error && (
          <div className="rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800">
            {error}
          </div>
        )}

        {loading ? (
          <p className="text-slate-600">Cargando categorías…</p>
        ) : (
          <CategoriaList categorias={categorias} onEdit={openEdit} onDelete={handleDelete} />
        )}
      </main>

      <CategoriaModal
        isOpen={modalOpen}
        title={selected ? "Editar categoría" : "Nueva categoría"}
        nombre={formNombre}
        descripcion={formDescripcion}
        onNombreChange={setFormNombre}
        onDescripcionChange={setFormDescripcion}
        onClose={closeModal}
        onSubmit={handleSubmit}
      />
    </div>
  );
}
