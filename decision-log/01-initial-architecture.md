# Initial Architecture Decisions

## Stack

- **Framework**: TanStack React Start (TanStack Router + Vite)
- **Styling**: Tailwind CSS v4 with shadcn/ui (Radix Rhea style)
- **Icons**: HugeIcons
- **Database**: SQLite via `better-sqlite3` with Drizzle ORM
- **Package Manager**: pnpm

## Database

- Single `recipes` table with JSON columns for `ingredients` and `instructions` arrays
- Seed data provides 6 sample recipes across difficulty levels
- DB connection is a lazy singleton, initialized on first server function call
- Auto-creates table (CREATE IF NOT EXISTS) and seeds on first access

## Data Flow

- All DB queries run inside `createServerFn()` from `@tanstack/react-start` (server-only)
- No client-side data fetching library; server functions handle data fetching
- Recipe list retrieves only metadata (no ingredients/instructions) for performance
- Recipe detail retrieves full row and deserializes JSON arrays

## Routing

- `/` — Recipe list (card grid)
- `/recipes/$recipeId` — Recipe detail page

## Design Rationale

- SQLite chosen for zero-setup local data; sufficient for a recipe book app
- JSON columns for arrays avoid join tables for this simple schema
- Server functions provide type-safe RPC without a separate API layer
- No client-side state management needed; route data is the source of truth
