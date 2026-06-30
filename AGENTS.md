# Workflow Directives

## Development

- The frontend dev server runs inside a Docker container (`recipes`) at http://recipes:3000
- The backend (FastAPI) runs inside the `backend` container at port 8001; Vite proxies `/api` to it
- Source code is edited on the host; changes are picked up automatically (Vite HMR for the frontend, uvicorn `--reload` for the backend)

## shadcn/ui Components

- This project uses shadcn/ui with the **Radix Rhea** style
- Component configuration is in `components.json`
- Base color: **mauve**
- Icon library: **hugeicons**
- When adding new components, always use the shadcn CLI:
  ```bash
  pnpm dlx shadcn add <component-name>
  ```
- Do not write shadcn components manually; always use the CLI

## Recipe Book App

- The app is a recipe book with recipe list and recipe detail pages
- File-based routing via TanStack Router in `src/routes/`
- Components live in `src/components/ui/`
- Utilities in `src/lib/`
- Build responsive, mobile-first UIs
- Use shadcn/ui components whenever possible
- Use HugeIcons for icons (`@hugeicons/react`)
- Styles use Tailwind CSS v4 with design tokens from `src/styles.css`

## Available Scripts

| Script | Description |
|--------|-------------|
| `pnpm dev` | Start dev server (port 3000) |
| `pnpm build` | Production build |
| `pnpm test` | Run tests (Vitest) |
| `pnpm lint` | Run ESLint |
| `pnpm typecheck` | TypeScript type checking |
| `pnpm format` | Format with Prettier |

## Package Manager

- Always use `pnpm` for package management. Never use `npm` or `yarn`.

## Architecture

The frontend is a TanStack Router SPA (Vite). The backend is a FastAPI app. They communicate over HTTP; the Vite dev server proxies `/api` to the backend.

### Data Layer

- **Backend:** FastAPI in `backend/main.py`, reading SQLite at `data/recipes.db` via the stdlib `sqlite3` module. Managed with `uv` (`backend/pyproject.toml`).
- Endpoints: `GET /api/recipes`, `GET /api/recipes/{id}`, `POST /api/recipes`, `DELETE /api/recipes/{id}`.
- **Frontend:** `src/lib/api.ts` is a typed `fetch` client (`listRecipes`, `getRecipe`, `createRecipe`, `deleteRecipe`). Route loaders call it; mutations call `router.invalidate()` to refetch.

### Routes

- `/` — Recipe list page (with search)
- `/recipes/new` — Add recipe form
- `/recipes/$recipeId` — Recipe detail page (with delete)

### Layout

- `src/components/app-layout.tsx` wraps all routes: a desktop sidebar (`md:` and up) and a mobile bottom nav.

### Decision Log

Design decisions are documented in `./decision-log/`.

- [01-initial-architecture.md](./decision-log/01-initial-architecture.md) — Stack, database, data flow, routing decisions
