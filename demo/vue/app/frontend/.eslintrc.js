module.exports = {
  root: true,
  env: {
    es6: true,
    jest: true,
    node: true
  },
  extends: ['plugin:vue/essential', 'eslint:recommended'],
  plugins: ['vuetify'],
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly',
    _: false
  },
  parserOptions: {
    parser: 'babel-eslint',
    ecmaVersion: 8
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
    semi: ['error', 'always'],
    'vue/html-closing-bracket-newline': [
      'off',
      {
        singleline: 'never',
        multiline: 'never'
      }
    ],
    'vue/html-indent': [
      'error',
      2,
      {
        attribute: 1,
        baseIndent: 1,
        closeBracket: 0,
        alignAttributesVertically: true,
        ignores: []
      }
    ],
    'vue/max-attributes-per-line': [
      'off',
      {
        singleline: 1,
        multiline: {
          max: 1,
          allowFirstLine: true
        }
      }
    ],
    'vue/multi-word-component-names': 'off',
    'vue/no-multi-spaces': [
      'error',
      {
        ignoreProperties: false
      }
    ],
    'vue/no-spaces-around-equal-signs-in-attribute': ['error'],
    'vuetify/no-deprecated-classes': 'error',
    'vuetify/grid-unknown-attributes': 'error',
    'vuetify/no-legacy-grid': 'error'
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
