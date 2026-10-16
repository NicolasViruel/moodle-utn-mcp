import type { FormEvent } from "react";

type Props = {
  isOpen: boolean;
  title: string;
  nombre: string;
  descripcion: string;
  onNombreChange: (value: string) => void;
  onDescripcionChange: (value: string) => void;
  onClose: () => void;
  onSubmit: (event: FormEvent) => void;
  isSaving?: boolean;
};

export function CategoriaModal({
  isOpen,
  title,
  nombre,
  descripcion,
  onNombreChange,
  onDescripcionChange,
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
            <label className="block text-sm font-medium text-slate-700" htmlFor="nombre">
              Nombre
            </label>
            <input
              id="nombre"
              required
              minLength={1}
              value={nombre}
              onChange={(e) => onNombreChange(e.target.value)}
              className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700" htmlFor="descripcion">
              Descripción (opcional)
            </label>
            <textarea
              id="descripcion"
              rows={3}
              value={descripcion}
              onChange={(e) => onDescripcionChange(e.target.value)}
              className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
            />
          </div>
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
