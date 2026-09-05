// ESLint flat config with type-checked rules for the Express starter.
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config({ ignores: ["dist/"] }, js.configs.recommended, {
  // Type-checked rules only apply where a tsconfig project exists.
  files: ["src/**/*.ts", "test/**/*.ts"],
  extends: tseslint.configs.recommendedTypeChecked,
  languageOptions: {
    parserOptions: { project: "./tsconfig.eslint.json", tsconfigRootDir: import.meta.dirname },
  },
  rules: {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-floating-promises": "error",
  },
});
