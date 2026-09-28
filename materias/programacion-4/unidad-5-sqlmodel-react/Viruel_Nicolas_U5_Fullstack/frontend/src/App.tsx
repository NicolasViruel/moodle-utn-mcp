import { Footer } from "./components/Footer";
import { Navbar } from "./components/Navbar";
import { ProductoForm } from "./components/ProductoForm";
import { ProductoList } from "./components/ProductoList";
import type { Producto } from "./types/producto";

const productosDemo: Producto[] = [
  {
    id: 1,
    nombre: "Notebook Dev 14",
    descripcion: "16 GB RAM, SSD 512 GB, ideal para desarrollo.",
    precio: 899.0,
  },
  {
    id: 2,
    nombre: "Mouse ergonómico",
    descripcion: "Inalámbrico, sensor de precisión.",
    precio: 45.5,
  },
  {
    id: 3,
    nombre: "Hub USB-C",
    descripcion: "3 puertos USB-A y salida HDMI.",
    precio: 32.0,
  },
];

export default function App() {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <Navbar />
      <main className="mx-auto max-w-6xl space-y-10 px-4 py-8">
        <div>
          <h2 className="text-2xl font-bold">Catálogo</h2>
          <p className="mt-1 text-slate-600">Vista de catálogo con datos de ejemplo.</p>
        </div>
        <ProductoList productos={productosDemo} />
        <ProductoForm />
      </main>
      <Footer />
    </div>
  );
}
