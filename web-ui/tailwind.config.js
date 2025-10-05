/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        quantum: {
          blue: '#0066ff',
          purple: '#8b5cf6',
          pink: '#ec4899',
        }
      }
    },
  },
  plugins: [],
}
