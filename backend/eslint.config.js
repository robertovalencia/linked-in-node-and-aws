import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import globals from 'globals';
export default tseslint.config(
  { ignores: ['dist/**', 'dist-dev/**', 'coverage/**', 'test/logs/**', 'node_modules/**'] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  { languageOptions: { globals: globals.node } },
  {
    files: ['test/**/*.ts'],
    languageOptions: { globals: globals.jest },
    rules: { '@typescript-eslint/no-explicit-any': 'off' },
  },
);
