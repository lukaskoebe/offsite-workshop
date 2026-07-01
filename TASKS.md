# Workshop Task Backlog

> **How to use this file.** This is a *menu of exercises* for workshop
> participants to pick from and hand to the coding agent — **not** a to-do list
> for the agent to work through on its own. Implement an item only when a person
> explicitly asks for it. Pick one, phrase it as a request, and see how far the
> agent gets. After each change, run `pnpm verify`.

Most tasks touch two layers: an endpoint in `backend/main.py` + a function in
`src/lib/api.ts`, then UI in `src/routes/`. See [AGENTS.md](./AGENTS.md) for
conventions.

## Starter

Single layer, or a small change across the stack — good for a first try.

- [ ] **Edit a recipe** — new route `/recipes/$recipeId/edit` + `PUT /api/recipes/{id}`, reusing the new-recipe form.
- [ ] **Sort the list** — dropdown to sort by total time, difficulty, or name.
- [ ] **Difficulty filter** — easy/medium/hard chips next to the search box.
- [ ] **Dark-mode toggle** — the theme tokens already exist in `src/styles.css`.
- [ ] **Total-time badge** — show prep + cook time prominently on each card.
- [ ] **Empty state** — a friendlier message + illustration when there are no recipes.

## Intermediate

Crosses the API boundary or adds a new interaction.

- [ ] **Server-side search** — `GET /api/recipes?q=` with a debounced input.
- [ ] **Favorites** — a `favorite` column + toggle, with a "Favorites" filter.
- [ ] **Tags / categories** — many recipes → tags, filterable in the list.
- [ ] **Image upload** — accept a file instead of a URL (multipart endpoint + static serving).
- [ ] **Ratings** — 1–5 stars per recipe, averaged on the card.
- [ ] **Servings scaler** — recalculate ingredient quantities for a chosen serving count.
- [ ] **Form validation** — add zod + react-hook-form to the recipe form.

## Advanced

New subsystems — a stretch goal for the session.

- [ ] **Auth + per-user recipes** — sign in, and scope recipes to the signed-in user.
- [ ] **Full-text search** — SQLite FTS5 over titles, descriptions, ingredients.
- [ ] **Meal planner** — assign recipes to days of the week (new entity end-to-end).
- [ ] **Shopping list** — combine ingredients from selected recipes.
- [ ] **Deploy it** — ship the app somewhere public.

## AI-native (showcases the coding agent itself)

- [ ] **Generate a recipe** — "give me a recipe from these ingredients" via an LLM call in the backend.
- [ ] **Transform a recipe** — "make this vegetarian" / "scale to 6 servings" with an LLM.
- [ ] **Import from a URL** — paste a recipe link; scrape and pre-fill the form.
- [ ] **TDD with the agent** — write the failing test first, then ask the agent to make it pass.
- [ ] **Refactor drill** — "extract a shared `RecipeForm` used by both add and edit."
