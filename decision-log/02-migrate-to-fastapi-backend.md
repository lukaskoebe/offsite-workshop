# Migrate to a TanStack Router SPA + FastAPI Backend

> Supersedes parts of [01-initial-architecture.md](./01-initial-architecture.md)
> (the framework and data-layer decisions).

## Context

The app was originally built on **TanStack React Start** (full-stack React with
server functions) and a TypeScript data layer (`better-sqlite3` + Drizzle ORM)
called via `createServerFn()`. During workshop prep we found the DeepSeek coding
agent struggled with the TanStack Start abstractions (server functions, the
SSR/shell model, framework-specific files), which made agent-driven changes
unreliable.

We wanted an architecture that is **easier for a coding agent to reason about**:
a clear client/server split with a conventional HTTP API and a familiar backend
language.

## Decision

Split the app into a plain SPA frontend and a separate Python backend.

### Frontend — TanStack Router SPA (Vite)

- Dropped `@tanstack/react-start`; now a standard Vite SPA using
  `@tanstack/react-router` only.
- Added a root `index.html` entry that mounts `#app` and loads `src/main.tsx`.
- The root route (`src/routes/__root.tsx`) renders an `<Outlet/>` instead of a
  Start `shellComponent`.
- The `@/` path alias is provided by `resolve.alias` in `vite.config.ts`
  (TanStack Start previously supplied it).
- `src/lib/api.ts` is a typed `fetch` client (`listRecipes`, `getRecipe`,
  `createRecipe`, `deleteRecipe`). Route loaders call it; mutations call
  `router.invalidate()` to refetch.

### Backend — FastAPI (Python)

- `backend/main.py` exposes `GET /api/recipes`, `GET /api/recipes/{id}`,
  `POST /api/recipes`, `DELETE /api/recipes/{id}`.
- Reads/writes the same SQLite database (`data/recipes.db`) using the Python
  **stdlib `sqlite3`** module — no ORM.
- `ingredients` / `instructions` stay as JSON-encoded text columns, parsed on
  read and dumped on write. Request bodies are validated with Pydantic.
- Managed with **uv** (`backend/pyproject.toml`).

### Wiring

- The Vite dev server proxies `/api` to the backend. The target is
  `VITE_API_PROXY_TARGET` (defaults to `http://localhost:8001` for native dev;
  set to `http://backend:8001` in Docker). Using a proxy avoids CORS entirely.
- `docker compose` runs `recipes` (frontend) and `backend` (FastAPI with
  `uvicorn --reload`) side by side, both with hot reload.

## Consequences

- **Two processes** now instead of one — managed together via `docker compose`.
- The data layer is **language-agnostic**: the backend can grow independently of
  the UI, and the API surface is explicit and inspectable (FastAPI's `/docs`).
- Removed dependencies: `@tanstack/react-start`,
  `@tanstack/react-router-ssr-query`, `drizzle-orm`, `better-sqlite3`, `sqlite3`.
- Simpler mental model for the coding agent: edit a React component, or edit a
  FastAPI endpoint — no framework-specific RPC layer in between.

## Features added alongside the migration

Recipe **search** (client-side filter), **add recipe** (`/recipes/new` form →
`POST`), **delete recipe** (confirm dialog → `DELETE`), and a **responsive
layout** (desktop sidebar + mobile bottom nav) in `src/components/app-layout.tsx`.
