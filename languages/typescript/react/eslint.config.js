import js from "@eslint/js";
import reactHooks from "eslint-plugin-react-hooks";
import tseslint from "typescript-eslint";

export default tseslint.config(
  { ignores: ["dist/", "test/"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    // Type-checked rules only apply where a tsconfig project exists.
    files: ["src/**/*.ts", "src/**/*.tsx"],
    languageOptions: {
      parserOptions: { project: "./tsconfig.json", tsconfigRootDir: import.meta.dirname },
    },
    plugins: { "react-hooks": reactHooks },
    rules: {
      ...reactHooks.configs.recommended.rules,
      ...tseslint.configs.recommendedTypeChecked.rules,
      "@typescript-eslint/no-explicit-any": "error",
    },
  },
);
