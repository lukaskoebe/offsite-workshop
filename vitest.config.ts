import { fileURLToPath } from "node:url"
import { defineConfig } from "vitest/config"
import viteReact from "@vitejs/plugin-react"

// Standalone Vitest config so tests don't load the full app's Vite plugins
// (router codegen, tailwind, etc.). We still need the React plugin for JSX and
// the `@/` alias to match the app.
export default defineConfig({
  plugins: [viteReact()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    restoreMocks: true,
  },
})
