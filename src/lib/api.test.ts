import { afterEach, describe, expect, it, vi } from "vitest"
import { createRecipe, deleteRecipe, getRecipe, listRecipes } from "./api"
import type { RecipeInput } from "./api"

function mockFetch(opts: { ok?: boolean; status?: number; body?: unknown }) {
  return vi.fn().mockResolvedValue({
    ok: opts.ok ?? true,
    status: opts.status ?? 200,
    json: async () => opts.body,
  })
}

const INPUT: RecipeInput = {
  title: "Test",
  description: "",
  image: "",
  prepTime: 1,
  cookTime: 1,
  servings: 1,
  difficulty: "easy",
  ingredients: [],
  instructions: [],
}

afterEach(() => vi.unstubAllGlobals())

describe("api client", () => {
  it("listRecipes calls GET /api/recipes", async () => {
    const fetchMock = mockFetch({ body: [{ id: 1, title: "A" }] })
    vi.stubGlobal("fetch", fetchMock)

    const data = await listRecipes()

    expect(fetchMock).toHaveBeenCalledWith("/api/recipes")
    expect(data).toHaveLength(1)
  })

  it("getRecipe returns null on 404", async () => {
    vi.stubGlobal("fetch", mockFetch({ ok: false, status: 404 }))
    expect(await getRecipe(99)).toBeNull()
  })

  it("createRecipe POSTs JSON and returns the recipe", async () => {
    const fetchMock = mockFetch({ status: 201, body: { id: 7 } })
    vi.stubGlobal("fetch", fetchMock)

    const result = await createRecipe(INPUT)

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/recipes",
      expect.objectContaining({ method: "POST" }),
    )
    expect(result.id).toBe(7)
  })

  it("deleteRecipe throws on a failed response", async () => {
    vi.stubGlobal("fetch", mockFetch({ ok: false, status: 500 }))
    await expect(deleteRecipe(1)).rejects.toThrow()
  })
})
