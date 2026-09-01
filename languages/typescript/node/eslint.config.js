// ESLint flat config with type-checked rules for the Node starter.
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config({ ignores: ["dist/"] }, js.configs.recommended, {
  // Type-checked rules only apply where a tsconfig project exists; the
  // config file itself falls back to the base recommended rules.
  files: ["src/**/*.ts", "test/**/*.ts"],
  extends: tseslint.configs.recommendedTypeChecked,
  languageOptions: {
    parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
  },
  rules: {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-floating-promises": "error",
  },
});
