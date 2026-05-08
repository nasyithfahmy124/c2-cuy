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
          bg: "#F6F8F4",
          text: "#0F172A",
        },
      },

      boxShadow: {
        glass: "0 10px 40px rgba(15,23,42,0.08)",
        soft: "0 8px 30px rgba(0,0,0,0.06)",
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