/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      backgroundColor: {
        'primary': '#000000',
        'secondary': '#B0FFA3',
        //'accent': '#f5f5f5',
        //'neutral': '#f5f5f5',
        //'base-100': '#f5f5f5',
        //'info': '#f5f5f5',
        //'success': '#f5f5f5',
        //'warning': '#f5f5f5',
        //'error': '#f5f5f5',
      
      }, 
      
      fontFamily: {
        sans: ['NeogramDemiBold', 'sans-serif'],
        sans2: ['NeogramBlackit', 'sans-serif'],
        blackExtended: ['NeogramBlackExtended', 'sans-serif'],
      },
    },
  },
  plugins: [require('daisyui'),],
  daisyui:{
    themes:[""]
  }
}