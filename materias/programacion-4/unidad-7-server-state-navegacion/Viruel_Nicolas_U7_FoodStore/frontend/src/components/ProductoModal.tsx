import type { FormEvent } from "react";
import type { Categoria } from "../types/categoria";

type Props = {
  isOpen: boolean;
  title: string;
  nombre: string;
  descripcion: string;
  precio: string;
  disponible: boolean;
  categoriaIds: number[];
  categorias: Categoria[];
  onNombreChange: (value: string) => void;
  onDescripcionChange: (value: string) => void;
  onPrecioChange: (value: string) => void;
  onDisponibleChange: (value: boolean) => void;
  onToggleCategoria: (id: number) => void;
  onClose: () => void;
  onSubmit: (event: FormEvent) => void;
  isSaving?: boolean;
};

export function ProductoModal({
  isOpen,
  title,
  nombre,
  descripcion,
  precio,
  disponible,
  categoriaIds,
  categorias,
  onNombreChange,
  onDescripcionChange,
  onPrecioChange,
  onDisponibleChange,
  onToggleCategoria,
  onClose,
  onSubmit,
  isSaving = false,
}: Props) {
  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-xl">
        <h2 className="text-lg font-bold text-slate-900">{title}</h2>
        <form className="mt-4 space-y-4" onSubmit={onSubmit}>
          <div>
            <label className="block text-sm font-medium text-slate-700" htmlFor="prod-nombre">
              Nombre
            </label>
            <input
              id="prod-nombre"
              required
              minLength={1}
              value={nombre}
              onChange={(e) => onNombreChange(e.target.value)}
              className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700" htmlFor="prod-desc">
              Descripción
            </label>
            <textarea
              id="prod-desc"
              rows={2}
              value={descripcion}
              onChange={(e) => onDescripcionChange(e.target.value)}
              className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700" htmlFor="prod-precio">
              Precio base
            </label>
            <input
              id="prod-precio"
              type="number"
              min={0}
              step="0.01"
              required
              value={precio}
              onChange={(e) => onPrecioChange(e.target.value)}
              className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
            />
          </div>
          <label className="flex items-center gap-2 text-sm text-slate-700">
            <input
              type="checkbox"
              checked={disponible}
              onChange={(e) => onDisponibleChange(e.target.checked)}
            />
            Disponible
          </label>
          <fieldset>
            <legend className="text-sm font-medium text-slate-700">Categorías (al menos una)</legend>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {categorias.map((c) => (
                <label key={c.id} className="flex items-center gap-2 text-sm text-slate-700">
                  <input
                    type="checkbox"
                    checked={categoriaIds.includes(c.id)}
                    onChange={() => onToggleCategoria(c.id)}
                  />
                  {c.nombre}
                </label>
              ))}
            </div>
          </fieldset>
          <div className="flex justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isSaving}
              className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 disabled:opacity-60"
            >
              {isSaving ? "Guardando…" : "Guardar"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
