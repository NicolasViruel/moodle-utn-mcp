# Frontend — FOOD STORE

**Alumno:** Nicolás Viruel — Programación IV — Unidad 7

React + TypeScript (Vite) + TanStack Query + React Router + Tailwind CSS.

## Requisitos

- Node.js 20+
- Backend corriendo en `http://127.0.0.1:8000`

## Instalación y arranque

```bash
npm install
npm run dev
```

La app abre en http://localhost:5173 y arranca en `/categorias`.

## Estructura

```
src/
  App.tsx                 # solo rutas + Navbar
  pages/
    CategoriasPage.tsx    # useQuery / useMutation + modal
    ProductsPage.tsx
  components/             # CategoriaList, CategoriaModal, Navbar, ...
  types/                  # Categoria, Producto
  services/               # fetch hacia FastAPI
```
