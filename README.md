# Recipe Book

A recipe book app with a TanStack Router (SPA) frontend, a FastAPI backend, and SQLite, styled with shadcn/ui.

> New here? Non-developers should follow the friendly, illustrated
> [setup guide](https://lukaskoebe.github.io/offsite-workshop/) instead.

## First run

1. **Set up your environment file.** Copy the template and paste in the API
   token you were given for the workshop:

   ```bash
   cp example.env .env
   # then open .env and set ASKAI_API_TOKEN=<your token>
   ```

2. **Start everything with Docker** (frontend + backend + coding agent, all with
   hot reload):

   ```bash
   docker compose up
   ```

3. Open the app at **http://localhost:3000**.

## Development

The Vite dev server proxies `/api` to the backend, so run both. You can use
Docker (above), or run them natively:

```bash
# Frontend (port 3000)
pnpm dev

# Backend (port 8001)
cd backend && uv run uvicorn main:app --reload --port 8001
```

Interactive API docs (Swagger) are served at **http://localhost:3000/api/docs**.

Reset the database back to its sample recipes at any time:

```bash
cd backend && uv run python seed.py
```

## Scripts

```bash
pnpm verify    # typecheck + lint + frontend tests + backend tests (run before committing)
pnpm test      # Frontend tests (Vitest)
pnpm test:backend  # Backend tests (pytest)
pnpm build     # Production build
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
