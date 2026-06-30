import { fileURLToPath } from "node:url"
import { defineConfig } from "vite"
import { devtools } from "@tanstack/devtools-vite"
import { tanstackRouter } from '@tanstack/router-plugin/vite'
import viteReact from "@vitejs/plugin-react"
import tailwindcss from "@tailwindcss/vite"

const config = defineConfig({
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  plugins: [devtools(), tailwindcss(), tanstackRouter({
      target: 'react',
      autoCodeSplitting: true,
    }), viteReact()],
  server: {
    // `true` allows any Host header — convenient for remote dev access.
    // Tighten to specific hostnames if this box is exposed to untrusted networks.
    allowedHosts: true,
    proxy: {
      // In Docker the backend is a separate container (see docker-compose.yaml);
      // for native dev it defaults to localhost.
      "/api": process.env.VITE_API_PROXY_TARGET ?? "http://localhost:8001",
    },
  }
})

export default config
