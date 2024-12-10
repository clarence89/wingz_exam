// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    "@nuxt/ui",
    "@pinia/nuxt",
    "@pinia-plugin-persistedstate/nuxt",
    "@nuxtjs/tailwindcss",
    "@nuxtjs/color-mode",
  ],
  tailwindcss: {
    config: {
      theme: {
        extend: {
          colors: {
            mmwgh: "#05981c",
          },
        },
      },
    },
  },
  colorMode: {
    classSuffix: "",
  },
  runtimeConfig: {
    public: {
      baseURL: process.env.NUXT_PUBLIC_BASE_URL || "http://localhost:8000",
    },
  },
  target: "static",
  ssr: false,
  server: {
    host: "0",
    port: "3000", // optional
  },
});
