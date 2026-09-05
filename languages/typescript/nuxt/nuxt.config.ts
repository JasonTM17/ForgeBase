export default defineNuxtConfig({
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      appName: "",
    },
  },
  // Ensure the build fails on type errors — production-oriented defaults.
  typescript: { strict: true },
  compatibilityDate: "2024-11-01",
});
