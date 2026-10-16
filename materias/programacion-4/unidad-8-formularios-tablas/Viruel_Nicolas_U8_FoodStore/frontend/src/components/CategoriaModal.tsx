import { useForm } from "@tanstack/react-form";
import type { Categoria, CategoriaInput } from "../types/categoria";

type Props = {
  isOpen: boolean;
  selected: Categoria | null;
  isSaving: boolean;
  formError: string | null;
  onClose: () => void;
  onSubmit: (input: CategoriaInput) => void;
};

export function CategoriaModal({ isOpen, selected, isSaving, formError, onClose, onSubmit }: Props) {
  const form = useForm({
    defaultValues: {
      nombre: selected?.nombre ?? "",
      descripcion: selected?.descripcion ?? "",
    },
    onSubmit: ({ value }) => {
      onSubmit({
        nombre: value.nombre.trim(),
        descripcion: value.descripcion.trim(),
      });
    },
  });

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-xl">
        <h2 className="text-lg font-bold text-slate-900">
          {selected ? "Editar categoría" : "Nueva categoría"}
        </h2>
        <form
          className="mt-4 space-y-4"
          onSubmit={(e) => {
            e.preventDefault();
            e.stopPropagation();
            void form.handleSubmit();
          }}
        >
          <form.Field
            name="nombre"
            validators={{
              onChange: ({ value }) =>
                !value.trim() ? "El nombre es obligatorio y no puede contener solo espacios." : undefined,
            }}
          >
            {(field) => (
              <div>
                <label className="block text-sm font-medium text-slate-700" htmlFor={field.name}>
                  Nombre
                </label>
                <input
                  id={field.name}
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
                />
                {field.state.meta.errors[0] && (
                  <p className="mt-1 text-xs text-rose-600">{field.state.meta.errors[0]}</p>
                )}
              </div>
            )}
          </form.Field>
          <form.Field name="descripcion">
            {(field) => (
              <div>
                <label className="block text-sm font-medium text-slate-700" htmlFor={field.name}>
                  Descripción (opcional)
                </label>
                <textarea
                  id={field.name}
                  rows={3}
                  value={field.state.value}
                  onBlur={field.handleBlur}
                  onChange={(e) => field.handleChange(e.target.value)}
                  className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
                />
              </div>
            )}
          </form.Field>
          {formError && (
            <p className="rounded-lg border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-800">
              {formError}
            </p>
          )}
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
