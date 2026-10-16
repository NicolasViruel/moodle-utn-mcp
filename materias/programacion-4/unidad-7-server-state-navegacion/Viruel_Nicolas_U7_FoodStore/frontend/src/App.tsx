import { Navigate, Route, Routes } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import { CategoriasPage } from "./pages/CategoriasPage";
import { ProductsPage } from "./pages/ProductsPage";

export default function App() {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/categorias" replace />} />
        <Route path="/categorias" element={<CategoriasPage />} />
        <Route path="/productos" element={<ProductsPage />} />
      </Routes>
    </div>
  );
}
