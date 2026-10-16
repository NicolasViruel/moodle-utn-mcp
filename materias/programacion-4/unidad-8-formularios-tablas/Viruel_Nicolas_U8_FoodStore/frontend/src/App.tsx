import { Navigate, Route, Routes } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import { CategoriesPage } from "./pages/CategoriesPage";
import { IngredientsPage } from "./pages/IngredientsPage";
import { ProductsPage } from "./pages/ProductsPage";

export default function App() {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/categories" replace />} />
        <Route path="/categories" element={<CategoriesPage />} />
        <Route path="/products" element={<ProductsPage />} />
        <Route path="/ingredients" element={<IngredientsPage />} />
      </Routes>
    </div>
  );
}
