import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
const proxyHost = process.env.VITE_PROXY_HOST || "127.0.0.1";
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5183,
    strictPort: true,
    proxy: {
      "/api/auth": process.env.IDENTITY_PROXY_URL || `http://${proxyHost}:8181`,
      "/api/providers":
        process.env.CATALOG_PROXY_URL || `http://${proxyHost}:8182`,
      "/api/inquiries":
        process.env.INQUIRIES_PROXY_URL || `http://${proxyHost}:8183`,
      "/api/notifications":
        process.env.NOTIFICATIONS_PROXY_URL || `http://${proxyHost}:8184`,
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    restoreMocks: true,
    coverage: {
      provider: "v8",
      reporter: ["text", "lcov"],
      include: ["src/**/*.{ts,tsx}"],
      exclude: [
        "src/**/*.test.{ts,tsx}",
        "src/test/**",
        "src/main.tsx",
        "src/types/**",
      ],
    },
  },
});
