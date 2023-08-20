module.exports = {
  mode: 'jit',
  content: ["./index.html", './src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'vs-dark': '#1e1e1e',
        'oli':
        {
          DEFAULT: '#FFFFFF',
          25: '#FAFAFA',
          50: '#F6F6F6',
          100: '#ECECEC',
          200: '#D0D0D0',
          300: '#B3B3B3',
          400: '#7A7A7A',
          500: '#404040',
          600: '#393939',
          700: '#262626',
          800: '#1E1E1E',
          900: '#131313'
        },
        'nilam': "#F6F8FA",
        'nilam-dark': "#232629",
      },
      dropShadow: {
        'sm-dark': '0 1px 2px rgba(0, 0, 0, 0.5)',
        'md-dark': '0 4px 6px rgba(0, 0, 0, 0.5)',
        'lg-dark': '0 10px 15px rgba(0, 0, 0, 0.5)',
        'xl-dark': '0 20px 25px rgba(0, 0, 0, 0.5)',
        '2xl-dark': '0 25px 50px rgba(0, 0, 0, 0.5)',
      },
    },
    plugins: []
  }

}
