import type { ReactNode } from "react"
import { Link } from "@tanstack/react-router"
import { HugeiconsIcon } from "@hugeicons/react"
import { Home01Icon, Add01Icon, ChefHatIcon } from "@hugeicons/core-free-icons"

const navItems = [
  { to: "/", label: "Recipes", icon: Home01Icon },
  { to: "/recipes/new", label: "Add Recipe", icon: Add01Icon },
] as const

function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 z-30 hidden w-64 flex-col border-r border-sidebar-border bg-sidebar px-4 py-6 md:flex">
      <Link to="/" className="mb-8 flex items-center gap-2 px-2">
        <HugeiconsIcon icon={ChefHatIcon} className="size-6 text-primary" />
        <span className="font-heading text-xl font-bold">Recipe Book</span>
      </Link>
      <nav className="flex flex-col gap-1">
        {navItems.map((item) => (
          <Link
            key={item.to}
            to={item.to}
            activeOptions={{ exact: item.to === "/" }}
            className="flex items-center gap-3 rounded-2xl px-3 py-2 text-sm font-medium transition-colors"
            inactiveProps={{
              className:
                "text-sidebar-foreground/70 hover:bg-sidebar-accent hover:text-sidebar-foreground",
            }}
            activeProps={{ className: "bg-sidebar-accent text-sidebar-foreground" }}
          >
            <HugeiconsIcon icon={item.icon} className="size-5" />
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  )
}

function BottomNav() {
  return (
    <nav className="fixed inset-x-0 bottom-0 z-30 flex border-t border-border bg-background/95 backdrop-blur md:hidden">
      {navItems.map((item) => (
        <Link
          key={item.to}
          to={item.to}
          activeOptions={{ exact: item.to === "/" }}
          className="flex flex-1 flex-col items-center gap-1 py-3 text-xs font-medium transition-colors"
          inactiveProps={{ className: "text-muted-foreground" }}
          activeProps={{ className: "text-primary" }}
        >
          <HugeiconsIcon icon={item.icon} className="size-5" />
          {item.label}
        </Link>
      ))}
    </nav>
  )
}

export function AppLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-svh">
      <Sidebar />
      <main className="pb-24 md:pb-0 md:pl-64">{children}</main>
      <BottomNav />
    </div>
  )
}
