import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // This proxy forwards any request starting with /api to http://localhost:5001
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
        // Optionally rewrite the path if necessary (e.g., remove /api prefix)
        // rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})