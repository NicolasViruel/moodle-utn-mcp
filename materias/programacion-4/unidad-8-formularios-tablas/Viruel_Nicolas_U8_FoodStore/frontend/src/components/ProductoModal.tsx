import { useForm } from "@tanstack/react-form";
import type { Categoria } from "../types/categoria";
import type { Ingrediente } from "../types/ingrediente";
import type { Producto, ProductoInput } from "../types/producto";

type Props = {
  isOpen: boolean;
  selected: Producto | null;
  categorias: Categoria[];
  ingredientes: Ingrediente[];
  isSaving: boolean;
  formError: string | null;
  onClose: () => void;
  onSubmit: (input: ProductoInput) => void;
};

export function ProductoModal({
  isOpen,
  selected,
  categorias,
  ingredientes,
  isSaving,
  formError,
  onClose,
  onSubmit,
}: Props) {
  const form = useForm({
    defaultValues: {
      nombre: selected?.nombre ?? "",
      descripcion: selected?.descripcion ?? "",
      precio_base: String(selected?.precio_base ?? "0"),
      disponible: selected?.disponible ?? true,
      categoria_ids: selected?.categoria_ids ?? ([] as number[]),
      ingrediente_ids: selected?.ingredientes.map((i) => i.ingrediente_id) ?? ([] as number[]),
    },
    onSubmit: ({ value }) => {
      onSubmit({
        nombre: value.nombre.trim(),
        descripcion: value.descripcion.trim(),
        precio_base: Number(value.precio_base),
        imagenes_url: selected?.imagenes_url ?? [],
        disponible: value.disponible,
        categoria_ids: value.categoria_ids,
        ingredientes: value.ingrediente_ids.map((id) => ({ ingrediente_id: id, cantidad: 1 })),
      });
    },
  });

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
      <div className="max-h-[90vh] w-full max-w-lg overflow-y-auto rounded-xl bg-white p-6 shadow-xl">
        <h2 className="text-lg font-bold text-slate-900">
          {selected ? "Editar producto" : "Nuevo producto"}
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
              onChange: ({ value }) => (!value.trim() ? "El nombre es obligatorio." : undefined),
            }}
          >
            {(field) => (
              <div>
                <label className="block text-sm font-medium text-slate-700">Nombre</label>
                <input
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
                <label className="block text-sm font-medium text-slate-700">Descripción</label>
                <textarea
                  rows={2}
                  value={field.state.value}
                  onChange={(e) => field.handleChange(e.target.value)}
                  className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
                />
              </div>
            )}
          </form.Field>
          <form.Field
            name="precio_base"
            validators={{
              onChange: ({ value }) =>
                Number(value) < 0 ? "El precio no puede ser negativo." : undefined,
            }}
          >
            {(field) => (
              <div>
                <label className="block text-sm font-medium text-slate-700">Precio base</label>
                <input
                  type="number"
                  min={0}
                  step="0.01"
                  value={field.state.value}
                  onChange={(e) => field.handleChange(e.target.value)}
                  className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
                />
                {field.state.meta.errors[0] && (
                  <p className="mt-1 text-xs text-rose-600">{field.state.meta.errors[0]}</p>
                )}
              </div>
            )}
          </form.Field>
          <form.Field name="disponible">
            {(field) => (
              <label className="flex items-center gap-2 text-sm text-slate-700">
                <input
                  type="checkbox"
                  checked={field.state.value}
                  onChange={(e) => field.handleChange(e.target.checked)}
                />
                Disponible
              </label>
            )}
          </form.Field>
          <form.Field
            name="categoria_ids"
            validators={{
              onChange: ({ value }) =>
                value.length < 1 ? "Seleccioná al menos una categoría." : undefined,
            }}
          >
            {(field) => (
              <fieldset>
                <legend className="text-sm font-medium text-slate-700">Categorías</legend>
                <div className="mt-2 grid grid-cols-2 gap-2">
                  {categorias.map((c) => (
                    <label key={c.id} className="flex items-center gap-2 text-sm">
                      <input
                        type="checkbox"
                        checked={field.state.value.includes(c.id)}
                        onChange={() => {
                          const next = field.state.value.includes(c.id)
                            ? field.state.value.filter((id) => id !== c.id)
                            : [...field.state.value, c.id];
                          field.handleChange(next);
                        }}
                      />
                      {c.nombre}
                    </label>
                  ))}
                </div>
                {field.state.meta.errors[0] && (
                  <p className="mt-1 text-xs text-rose-600">{field.state.meta.errors[0]}</p>
                )}
              </fieldset>
            )}
          </form.Field>
          <form.Field name="ingrediente_ids">
            {(field) => (
              <fieldset>
                <legend className="text-sm font-medium text-slate-700">Ingredientes asociados</legend>
                <div className="mt-2 grid grid-cols-2 gap-2">
                  {ingredientes.map((ing) => (
                    <label key={ing.id} className="flex items-center gap-2 text-sm">
                      <input
                        type="checkbox"
                        checked={field.state.value.includes(ing.id)}
                        onChange={() => {
                          const next = field.state.value.includes(ing.id)
                            ? field.state.value.filter((id) => id !== ing.id)
                            : [...field.state.value, ing.id];
                          field.handleChange(next);
                        }}
                      />
                      {ing.nombre}
                    </label>
                  ))}
                </div>
              </fieldset>
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
              className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isSaving}
              className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-60"
            >
              {isSaving ? "Guardando…" : "Guardar"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
