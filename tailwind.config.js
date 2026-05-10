/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./akun/templates/**/*.html",
    "./petani/templates/**/*.html",
    "./donatur/templates/**/*.html",
    "./dashboard/templates/**/*.html",
    "./edukasi/templates/**/*.html",

    "./static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        jejak: {
          primary: "#1D4D3A",   
          secondary: "#4D7C3E", 
          accent: "#D4A017",    
          bg: "#F7F9F2",        
          text: "#0F172A",      
        },
      },

      fontFamily: {
        heading: ["Plus Jakarta Sans", "sans-serif"],
        body: ["Inter", "sans-serif"],
      },

      boxShadow: {
        glow: "0 10px 40px rgba(29,77,58,0.18)",
        glass: "0 8px 32px rgba(15,23,42,0.08)",
        premium: "0 20px 80px rgba(29,77,58,0.15)",
      },

      backdropBlur: {
        xs: "2px",
      },


      borderRadius: {
        card: "2rem",
      },

      animation: {
        shimmer: "shimmer 2s linear infinite",
      },

      keyframes: {
        shimmer: {
          "100%": {
            transform: "translateX(200%)",
          },
        },
      },
    },
  },

  plugins: [],
}