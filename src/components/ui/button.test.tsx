import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"
import { Button } from "./button"

describe("Button", () => {
  it("renders its children", () => {
    render(<Button>Save Recipe</Button>)
    expect(screen.getByRole("button", { name: "Save Recipe" })).toBeTruthy()
  })

  it("reflects the variant via data-variant", () => {
    render(<Button variant="destructive">Delete</Button>)
    expect(screen.getByRole("button").dataset.variant).toBe("destructive")
  })
})
