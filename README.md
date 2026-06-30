# Recipe Book

A recipe book app with a TanStack Router (SPA) frontend, a FastAPI backend, and SQLite, styled with shadcn/ui.

## Development

Run both the frontend and the backend. The Vite dev server proxies `/api` to the backend.

```bash
# Frontend (port 3000)
pnpm dev

# Backend (port 8001)
cd backend && uv run uvicorn main:app --reload --port 8001
```

Or run both together with Docker (frontend + backend, hot reload):

```bash
docker compose up recipes backend
```

Other scripts:

```bash
pnpm build     # Production build
pnpm test      # Run tests
pnpm lint      # Run ESLint
pnpm typecheck # TypeScript type checking
```

## Architecture

See [decision-log/](./decision-log/) for design decisions.
See [AGENTS.md](./AGENTS.md) for workflow directives and architecture details.

## Adding shadcn/ui Components

```bash
pnpm dlx shadcn add <component-name>
```
