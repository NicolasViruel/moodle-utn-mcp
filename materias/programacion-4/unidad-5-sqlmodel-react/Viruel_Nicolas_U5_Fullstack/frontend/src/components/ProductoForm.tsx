export function ProductoForm() {
  return (
    <section className="rounded-xl border border-dashed border-slate-300 bg-slate-50 p-6">
      <h2 className="mb-4 text-lg font-semibold text-slate-800">Alta de producto</h2>
      <form className="grid gap-4 md:grid-cols-2">
        <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
          Nombre
          <input
            type="text"
            placeholder="Nombre del producto"
            className="rounded-lg border border-slate-300 px-3 py-2"
          />
        </label>
        <label className="flex flex-col gap-1 text-sm font-medium text-slate-700">
          Precio
          <input
            type="number"
            placeholder="0.00"
            className="rounded-lg border border-slate-300 px-3 py-2"
          />
        </label>
        <label className="flex flex-col gap-1 text-sm font-medium text-slate-700 md:col-span-2">
          Descripción
          <textarea
            rows={3}
            placeholder="Descripción breve"
            className="rounded-lg border border-slate-300 px-3 py-2"
          />
        </label>
        <button
          type="button"
          className="md:col-span-2 rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white"
        >
          Guardar
        </button>
      </form>
    </section>
  );
}
