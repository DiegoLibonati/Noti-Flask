import js from "@eslint/js";
import typescript from "typescript-eslint";
import prettier from "eslint-plugin-prettier";
import prettierConfig from "eslint-config-prettier";
import globals from "globals";

export default [
  // Archivos ignorados
  {
    ignores: ["dist/**", "node_modules/**", "coverage/**", "*.config.js"],
  },

  // Reglas base de JS (aplica a .js y .ts)
  js.configs.recommended,

  // Reglas de TypeScript: limitadas a archivos .ts para que el parser con
  // parserOptions.project no se aplique a JS de scripts/.
  ...typescript.configs.recommended.map((c) => ({ ...c, files: ["**/*.ts"] })),
  ...typescript.configs.strictTypeChecked.map((c) => ({
    ...c,
    files: ["**/*.ts"],
  })),
  ...typescript.configs.stylisticTypeChecked.map((c) => ({
    ...c,
    files: ["**/*.ts"],
  })),

  // Desactiva reglas que conflictúan con Prettier
  prettierConfig,

  // Configuración global para TypeScript
  {
    files: ["**/*.ts"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.es2022,
      },
      parserOptions: {
        project: ["./tsconfig.app.json", "./tsconfig.test.json"],
        tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: {
      prettier,
    },
    rules: {
      // Prettier como regla de ESLint
      "prettier/prettier": "error",

      // TypeScript
      "@typescript-eslint/explicit-function-return-type": "error",
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
      "@typescript-eslint/restrict-template-expressions": "off",
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/consistent-type-imports": [
        "error",
        { prefer: "type-imports" },
      ],
      "@typescript-eslint/consistent-type-definitions": ["error", "interface"],
      "@typescript-eslint/no-non-null-assertion": "off",

      // General
      "no-console": "warn",
      "no-debugger": "error",
      "prefer-const": "error",
      "no-var": "error",
      eqeqeq: ["error", "always"],
    },
  },

  // Reglas específicas para tests (más permisivas)
  {
    files: ["**/__tests__/**/*.ts", "**/*.test.ts", "**/*.spec.ts"],
    languageOptions: {
      globals: {
        ...globals.jest,
      },
    },
    rules: {
      "@typescript-eslint/no-explicit-any": "off",
      "@typescript-eslint/no-non-null-assertion": "off",
      "@typescript-eslint/unbound-method": "off",
      "@typescript-eslint/no-unsafe-assignment": "off",
      "@typescript-eslint/no-unsafe-member-access": "off",
      "@typescript-eslint/no-unsafe-call": "off",
      "@typescript-eslint/no-unsafe-argument": "off",
      "no-console": "off",
    },
  },

  // Scripts folder: utilidades Node.js en JS plano, fuera del proyecto TS.
  // Se coloca al final para que ningún config posterior sobrescriba el parser.
  {
    files: ["scripts/**/*.js"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        ...globals.node,
      },
    },
    rules: {
      "no-console": "off",
    },
  },
];
