/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // Đảm bảo dòng này quét tất cả các file component của bạn
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'], // Định nghĩa Inter là font sans-serif mặc định
      },
    },
  },
  plugins: [],
};