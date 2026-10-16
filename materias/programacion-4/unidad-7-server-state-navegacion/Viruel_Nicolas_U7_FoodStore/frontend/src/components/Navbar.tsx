import { NavLink } from "react-router-dom";

const linkClass = ({ isActive }: { isActive: boolean }) =>
  [
    "rounded-lg px-3 py-1.5 text-sm font-medium transition",
    isActive ? "bg-indigo-600 text-white" : "text-slate-600 hover:bg-slate-100",
  ].join(" ");

export function Navbar() {
  return (
    <header className="border-b border-slate-200 bg-white shadow-sm">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4">
        <h1 className="text-xl font-bold text-indigo-700">FOOD STORE</h1>
        <nav className="flex items-center gap-2">
          <NavLink to="/categorias" className={linkClass}>
            Categorías
          </NavLink>
          <NavLink to="/productos" className={linkClass}>
            Productos
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
