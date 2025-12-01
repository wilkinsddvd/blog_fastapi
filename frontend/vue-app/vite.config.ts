import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      "/auth": "http://127.0.0.1:8000",
      "/users": "http://127.0.0.1:8000",
      "/blogs": "http://127.0.0.1:8000",
      "/follows": "http://127.0.0.1:8000",
      "/messages": "http://127.0.0.1:8000"
    }
  }
});