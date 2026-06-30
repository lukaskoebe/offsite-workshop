import { useState } from "react"
import { createFileRoute, Link } from "@tanstack/react-router"
import { HugeiconsIcon } from "@hugeicons/react"
import {
  Clock02Icon,
  ChefIcon,
  FireIcon,
  Search01Icon,
} from "@hugeicons/core-free-icons"
import { listRecipes } from "@/lib/api"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"

export const Route = createFileRoute("/")({
  component: RecipeList,
  loader: () => listRecipes(),
})

function RecipeList() {
  const recipes = Route.useLoaderData()
  const [query, setQuery] = useState("")

  const q = query.trim().toLowerCase()
  const filtered = q
    ? recipes.filter(
        (recipe) =>
          recipe.title.toLowerCase().includes(q) ||
          recipe.description.toLowerCase().includes(q),
      )
    : recipes

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <header className="mb-8">
        <h1 className="font-heading text-4xl font-bold tracking-tight">Recipe Book</h1>
        <p className="mt-2 text-muted-foreground">Discover delicious recipes for every occasion</p>
      </header>

      <div className="relative mb-8 max-w-md">
        <HugeiconsIcon
          icon={Search01Icon}
          size={18}
          className="pointer-events-none absolute top-1/2 left-3 -translate-y-1/2 text-muted-foreground"
        />
        <Input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search recipes..."
          className="pl-10"
        />
      </div>

      {filtered.length === 0 ? (
        <p className="text-muted-foreground">No recipes match “{query}”.</p>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {filtered.map((recipe) => (
          <Link key={recipe.id} to="/recipes/$recipeId" params={{ recipeId: String(recipe.id) }}>
            <Card className="h-full cursor-pointer transition-shadow hover:shadow-md">
              {recipe.image && (
                <img
                  src={recipe.image}
                  alt={recipe.title}
                  className="aspect-[4/3] w-full object-cover"
                />
              )}
              <CardHeader>
                <CardTitle>{recipe.title}</CardTitle>
                <CardDescription>{recipe.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-3 text-xs text-muted-foreground">
                  <span className="inline-flex items-center gap-1">
                    <HugeiconsIcon icon={Clock02Icon} size={14} /> {recipe.prepTime + recipe.cookTime} min
                  </span>
                  <span className="inline-flex items-center gap-1">
                    <HugeiconsIcon icon={ChefIcon} size={14} /> {recipe.servings} servings
                  </span>
                  <Badge variant="secondary" className="text-xs">
                    <HugeiconsIcon icon={FireIcon} size={12} /> {recipe.difficulty}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </Link>
          ))}
        </div>
      )}
    </div>
  )
}
