// ESLint flat config with type-checked rules for the Fastify starter.
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config({ ignores: ["dist/", "test/"] }, js.configs.recommended, {
  files: ["src/**/*.ts"],
  extends: tseslint.configs.recommendedTypeChecked,
  languageOptions: {
    parserOptions: { project: "./tsconfig.json", tsconfigRootDir: import.meta.dirname },
  },
  rules: {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-floating-promises": "error",
  },
});
