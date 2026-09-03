import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  { ignores: [".svelte-kit/", "build/", "coverage/", "node_modules/"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ["src/**/*.ts"],
    languageOptions: {
      parserOptions: { project: "./tsconfig.json", tsconfigRootDir: import.meta.dirname },
    },
    rules: {
      ...tseslint.configs.recommendedTypeChecked.rules,
      "@typescript-eslint/no-explicit-any": "error",
    },
  },
);
