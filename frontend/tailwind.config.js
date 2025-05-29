/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./src/**/*.{js,jsx,ts,tsx}",
      "./index.html",
    ],
    theme: {
      extend: {
        colors: {
          'navy': {
            DEFAULT: '#001028',
            light: '#001a3d',
          },
          'brand': {
            green: '#4ade80',
            'green-hover': '#22c55e',
          },
          'slate': {
            light: '#e2e8f0',
            dark: '#475569',
          }
        },
        fontFamily: {
          'heading': ['Inter', 'sans-serif'],
          'body': ['Inter', 'sans-serif'],
        },
        boxShadow: {
          'popcorn': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        }
      },
    },
    plugins: [],
  }