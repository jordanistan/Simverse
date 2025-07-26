import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react({
    // This is a workaround to disable React Fast Refresh, which is causing the WebGL context error.
    babel: {
      plugins: [],
    },
  })],
})
