/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.html'],
  theme: {
    extend: {
      colors: { accent: '#2A2420', cream: '#FAFAF8', stone: '#ECEBE7', ink: '#131110', dark: '#130F0B' },
      fontFamily: {
        serif: ['"Fraunces"', 'Georgia', 'serif'],
        sans:  ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
