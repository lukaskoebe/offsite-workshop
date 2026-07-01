# Workflow Directives

## Development

- The frontend dev server runs inside a Docker container (`recipes`) at http://recipes:3000
- The backend (FastAPI) runs inside the `backend` container at port 8001; Vite proxies `/api` to it
- Source code is edited on the host; changes are picked up automatically (Vite HMR for the frontend, uvicorn `--reload` for the backend)
- Interactive API docs (Swagger) are at http://localhost:3000/api/docs

## Verifying your changes

- **Always run `pnpm verify` after making changes.** It runs typecheck, lint,
  frontend tests (Vitest), and backend tests (pytest) — this is the definition
  of "done". Fix anything it reports before considering a task complete.
- Add or update tests when you change behavior: frontend tests live next to the
  code as `*.test.ts(x)`; backend tests are in `backend/test_main.py`.
- `pnpm test:backend` needs Python + `uv` available in the environment.

## Environment

- Copy `example.env` to `.env` and set `ASKAI_API_TOKEN` (provided for the
  workshop). `.env` is gitignored — never commit secrets.
- Reset the database to its sample recipes with `cd backend && uv run python seed.py`.

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

- The app is a recipe book: browse/search a recipe list, view recipe detail, add a recipe, and delete a recipe
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
| `pnpm verify` | **Typecheck + lint + frontend tests + backend tests.** Run before finishing. |
| `pnpm dev` | Start frontend dev server (port 3000) |
| `pnpm test` | Frontend tests (Vitest) |
| `pnpm test:backend` | Backend tests (pytest, needs `uv`) |
| `pnpm build` | Production build |
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

### AI Integration

Workshop AI features call the **ask-ai** API, which is **OpenAI-compatible**
(chat completions). Use the helper — do not hand-roll the HTTP request.

- **Helpers (in `backend/ai.py`):**
  - `ask_ai(prompt, *, system=None, model=None) -> str` — free-text reply.
  - `ask_ai_json(prompt, ...) -> Any` — **structured output**: requests JSON mode
    and parses the reply into Python (with a fallback for fenced/prose output).
  - Both raise `HTTPException`, so failures surface cleanly from a route.
- **Worked examples in `backend/main.py`:**
  - Free text: `POST /api/ai/recipe-ideas` (ingredients → suggestions).
  - **Structured:** `POST /api/ai/generate-recipe` (idea → a full recipe). This
    is the pattern for JSON output: `ask_ai_json()` → **validate against a
    Pydantic model** (`RecipeInput.model_validate(...)`) → return typed JSON.
    Bad output fails with 502 instead of reaching the client malformed.
  - Copy either shape for new AI features: Pydantic input → prompt → `ask_ai`/
    `ask_ai_json` → typed response.
- **The call it makes:** `POST {ASKAI_API_BASE_URL}/chat/completions` with an
  OpenAI-style body `{"model", "messages": [{"role", "content"}], "temperature"}`;
  the reply text is `choices[0].message.content`.
- **Token handling (important):** the token is held by **one** service, the
  `ai-proxy` (Caddy, `ai-proxy/Caddyfile`), which injects the
  `Authorization` header. **The backend and opencode never receive
  `ASKAI_API_TOKEN`** — under Docker they point at the proxy
  (`ASKAI_API_BASE_URL=http://ai-proxy:8080/api`). So don't add the token to the
  backend or read it in code; just call `ask_ai()`.
- **Environment:**
  - `ASKAI_API_TOKEN` — held only by the `ai-proxy` service (from `.env`, see
    `example.env`). Not present in the backend. For native dev that calls the API
    directly (no proxy), export it and `ask_ai` will send it.
  - `ASKAI_API_BASE_URL` — Docker sets it to `http://ai-proxy:8080/api`; default
    is `https://ask-ai.smartclip.net/api`.
  - `ASKAI_MODEL` — optional; default `vllm/generic` (also `vllm/coding`,
    `vllm/deepseek`).
- **Testing:** mock `ask_ai` (see `test_ai_recipe_ideas`) — never call the live
  API in tests.

### Routes

- `/` — Recipe list page (with search)
- `/recipes/new` — Add recipe form
- `/recipes/$recipeId` — Recipe detail page (with delete)

### Layout

- `src/components/app-layout.tsx` wraps all routes: a desktop sidebar (`md:` and up) and a mobile bottom nav.

### Where things live

| Path | What |
|------|------|
| `src/routes/` | Pages (file-based routing). `__root.tsx` is the shell. |
| `src/lib/api.ts` | Typed `fetch` client — the only place the frontend talks to the backend. |
| `src/components/ui/` | shadcn/ui primitives (generated — prefer the CLI over editing). |
| `src/components/app-layout.tsx` | Sidebar + bottom-nav layout. |
| `src/styles.css` | Tailwind v4 theme tokens (colors, fonts, radius). |
| `backend/main.py` | FastAPI app + all endpoints. |
| `backend/ai.py` | `ask_ai()` helper for the ask-ai API (AI features). |
| `backend/seed.py` | Sample data + DB reset script. |
| `backend/test_main.py` | Backend API tests. |
| `data/recipes.db` | SQLite database (gitignored). |
| `src/routeTree.gen.ts` | **Generated — never edit by hand.** |

### Conventions

- **Adding a feature usually spans two layers:** an endpoint in `backend/main.py`
  and a matching function in `src/lib/api.ts`, then UI in a route. Keep the
  `RecipeInput`/`Recipe` types in `api.ts` in sync with the Pydantic models.
- **All database access goes through the FastAPI backend** — never read/write
  SQLite from the frontend.
- Fetch route data in the route's `loader`; after a create/update/delete, call
  `router.invalidate()` so loaders refetch.
- Use the `@/` import alias for `src/` (e.g. `@/lib/api`), not deep relative paths.
- Use shadcn/ui components and HugeIcons; keep UIs responsive and mobile-first.

### Example prompts

Good, well-scoped requests for the coding agent:

- "Add an *edit recipe* page at `/recipes/$recipeId/edit` with a `PUT /api/recipes/{id}` endpoint, reusing the form from the new-recipe page."
- "Add a `difficulty` filter (easy/medium/hard) to the recipe list, next to the search box."
- "Add a backend test for creating a recipe with an empty ingredients list."

### Decision Log

Design decisions are documented in `./decision-log/`.

- [01-initial-architecture.md](./decision-log/01-initial-architecture.md) — Original stack/data-flow (historical; superseded)
- [02-migrate-to-fastapi-backend.md](./decision-log/02-migrate-to-fastapi-backend.md) — Move to TanStack Router SPA + FastAPI backend (current architecture)
