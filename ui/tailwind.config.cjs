module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'vs-dark': '#1e1e1e',
        'oli':
        {
          DEFAULT: '#FFFFFF',
          50: '#F6F6F6',
          100: '#ECECEC',
          200: '#D0D0D0',
          300: '#B3B3B3',
          400: '#7A7A7A',
          500: '#404040',
          600: '#393939',
          700: '#262626',
          800: '#1C1C1C',
          900: '#131313'
        }
      },

    },
    plugins: []
  }
}