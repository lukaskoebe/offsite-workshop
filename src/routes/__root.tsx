import type { ErrorComponentProps } from "@tanstack/react-router"
import { Link, Outlet, createRootRoute } from "@tanstack/react-router"
import { TanStackRouterDevtoolsPanel } from "@tanstack/react-router-devtools"
import { TanStackDevtools } from "@tanstack/react-devtools"
import { AppLayout } from "@/components/app-layout"
import { Button } from "@/components/ui/button"

export const Route = createRootRoute({
  component: RootComponent,
  errorComponent: RootErrorComponent,
  notFoundComponent: () => (
    <main className="mx-auto max-w-md px-4 py-24 text-center">
      <h1 className="font-heading text-3xl font-bold">404</h1>
      <p className="mt-2 text-muted-foreground">
        The page you're looking for doesn't exist.
      </p>
      <Button asChild className="mt-6">
        <Link to="/">Back to recipes</Link>
      </Button>
    </main>
  ),
})

function RootErrorComponent({ error, reset }: ErrorComponentProps) {
  return (
    <main className="mx-auto max-w-md px-4 py-24 text-center">
      <h1 className="font-heading text-3xl font-bold">Something went wrong</h1>
      <p className="mt-2 text-muted-foreground">
        The app hit an unexpected error. You can try again, or head back to the
        recipe list.
      </p>
      {import.meta.env.DEV && (
        <pre className="mt-4 overflow-x-auto rounded-lg bg-muted p-3 text-left text-xs text-muted-foreground">
          {error.message}
        </pre>
      )}
      <div className="mt-6 flex justify-center gap-3">
        <Button onClick={() => reset()}>Try again</Button>
        <Button asChild variant="outline">
          <Link to="/">Back to recipes</Link>
        </Button>
      </div>
    </main>
  )
}

function RootComponent() {
  return (
    <>
      <AppLayout>
        <Outlet />
      </AppLayout>
      <TanStackDevtools
        config={{
          position: "bottom-right",
        }}
        plugins={[
          {
            name: "Tanstack Router",
            render: <TanStackRouterDevtoolsPanel />,
          },
        ]}
      />
    </>
  )
}
