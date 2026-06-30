export type Recipe = {
  id: number
  title: string
  description: string
  image: string
  prepTime: number
  cookTime: number
  servings: number
  difficulty: "easy" | "medium" | "hard"
  ingredients: string[]
  instructions: string[]
}

export type RecipeSummary = Omit<Recipe, "ingredients" | "instructions">

export type RecipeInput = Omit<Recipe, "id">

const API_BASE = "/api"

export async function listRecipes(): Promise<RecipeSummary[]> {
  const res = await fetch(`${API_BASE}/recipes`)
  if (!res.ok) throw new Error(`Failed to load recipes: ${res.status}`)
  return res.json()
}

export async function getRecipe(id: number): Promise<Recipe | null> {
  const res = await fetch(`${API_BASE}/recipes/${id}`)
  if (res.status === 404) return null
  if (!res.ok) throw new Error(`Failed to load recipe ${id}: ${res.status}`)
  return res.json()
}

export async function createRecipe(input: RecipeInput): Promise<Recipe> {
  const res = await fetch(`${API_BASE}/recipes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  })
  if (!res.ok) throw new Error(`Failed to create recipe: ${res.status}`)
  return res.json()
}

export async function deleteRecipe(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/recipes/${id}`, { method: "DELETE" })
  if (!res.ok) throw new Error(`Failed to delete recipe ${id}: ${res.status}`)
}
