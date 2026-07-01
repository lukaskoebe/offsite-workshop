import { createFileRoute, Link, useNavigate, useRouter } from "@tanstack/react-router"
import { HugeiconsIcon } from "@hugeicons/react"
import {
  Clock02Icon,
  ChefIcon,
  FireIcon,
  ArrowLeft01Icon,
  Time01Icon,
  Delete02Icon,
} from "@hugeicons/core-free-icons"
import { deleteRecipe, getRecipe } from "@/lib/api"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"

export const Route = createFileRoute("/recipes/$recipeId")({
  component: RecipeDetail,
  loader: async ({ params: { recipeId } }) => {
    return await getRecipe(Number(recipeId))
  },
  pendingComponent: RecipeDetailPending,
  notFoundComponent: () => (
    <div className="mx-auto max-w-3xl px-4 py-16 text-center">
      <h1 className="font-heading text-2xl font-bold">Recipe not found</h1>
      <p className="mt-2 text-muted-foreground">The recipe you're looking for doesn't exist.</p>
      <Button asChild className="mt-6">
        <Link to="/">Back to recipes</Link>
      </Button>
    </div>
  ),
})

function RecipeDetailPending() {
  return (
    <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6">
      <Skeleton className="h-5 w-32" />
      <Skeleton className="mt-6 aspect-[2/1] w-full rounded-[24px]" />
      <Skeleton className="mt-8 h-10 w-2/3" />
      <Skeleton className="mt-3 h-6 w-full" />
      <div className="mt-6 flex gap-4">
        <Skeleton className="h-5 w-24" />
        <Skeleton className="h-5 w-24" />
        <Skeleton className="h-5 w-24" />
      </div>
      <Skeleton className="mt-10 h-7 w-40" />
      <div className="mt-4 space-y-2">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-4 w-full" />
        ))}
      </div>
    </div>
  )
}

function RecipeDetail() {
  const recipe = Route.useLoaderData()
  const router = useRouter()
  const navigate = useNavigate()

  if (!recipe) return "no recipe found"

  async function handleDelete() {
    await deleteRecipe(recipe!.id)
    await router.invalidate()
    navigate({ to: "/" })
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6">
      <div className="mb-6 flex items-center justify-between">
        <Link
          to="/"
          className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground"
        >
          <HugeiconsIcon icon={ArrowLeft01Icon} size={16} /> Back to recipes
        </Link>

        <AlertDialog>
          <AlertDialogTrigger asChild>
            <Button variant="destructive" size="sm">
              <HugeiconsIcon icon={Delete02Icon} size={16} /> Delete
            </Button>
          </AlertDialogTrigger>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Delete this recipe?</AlertDialogTitle>
              <AlertDialogDescription>
                “{recipe.title}” will be permanently removed. This cannot be undone.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogAction onClick={handleDelete}>Delete</AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
      </div>

      {recipe.image && (
        <img
          src={recipe.image}
          alt={recipe.title}
          className="mb-8 aspect-[2/1] w-full rounded-[24px] object-cover"
        />
      )}

      <h1 className="font-heading text-4xl font-bold tracking-tight">{recipe.title}</h1>
      <p className="mt-2 text-lg text-muted-foreground">{recipe.description}</p>

      <div className="mt-6 flex flex-wrap gap-4">
        <span className="inline-flex items-center gap-1.5 text-sm text-muted-foreground">
          <HugeiconsIcon icon={Clock02Icon} size={18} /> Prep: {recipe.prepTime} min
        </span>
        <span className="inline-flex items-center gap-1.5 text-sm text-muted-foreground">
          <HugeiconsIcon icon={Time01Icon} size={18} /> Cook: {recipe.cookTime} min
        </span>
        <span className="inline-flex items-center gap-1.5 text-sm text-muted-foreground">
          <HugeiconsIcon icon={ChefIcon} size={18} /> {recipe.servings} servings
        </span>
        <Badge variant="secondary">
          <HugeiconsIcon icon={FireIcon} size={14} /> {recipe.difficulty}
        </Badge>
      </div>

      <section className="mt-10">
        <h2 className="font-heading text-2xl font-semibold">Ingredients</h2>
        <ul className="mt-4 space-y-2">
          {recipe.ingredients.map((ingredient, i) => (
            <li key={i} className="flex items-start gap-2 text-sm">
              <span className="mt-1.5 block size-1.5 shrink-0 rounded-full bg-primary" />
              {ingredient}
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-10">
        <h2 className="font-heading text-2xl font-semibold">Instructions</h2>
        <ol className="mt-4 space-y-4">
          {recipe.instructions.map((step, i) => (
            <li key={i} className="flex gap-4 text-sm">
              <span className="flex size-7 shrink-0 items-center justify-center rounded-full bg-primary text-xs font-medium text-primary-foreground">
                {i + 1}
              </span>
              <span className="pt-1">{step}</span>
            </li>
          ))}
        </ol>
      </section>
    </div>
  )
}
