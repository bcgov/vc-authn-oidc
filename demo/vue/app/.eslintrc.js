module.exports = {
  root: true,
  env: {
    commonjs: true,
    es6: true,
    jest: true,
    node: true
  },
  extends: ['eslint:recommended'],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly',
    _: false
  },
  parserOptions: {
    ecmaVersion: 9
  },
  rules: {
    'eol-last': ['error', 'always'],
    indent: ['error', 2, {
      'SwitchCase': 1
    }],
    'linebreak-style': ['error', 'unix'],
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'warn',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'warn',
    quotes: ['error', 'single'],
    semi: ['error', 'always']
  },
  overrides: [
    {
      files: [
        '**/__tests__/*.{j,t}s?(x)',
        '**/tests/unit/**/*.spec.{j,t}s?(x)'
      ],
      env: {
        jest: true
      }
    }
  ]
};
