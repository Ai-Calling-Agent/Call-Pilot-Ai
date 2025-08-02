# How to start frontend

1. install tailwind

A. npm install tailwindcss @tailwindcss/postcss postcss
B. create postcss.config.mjs on root
B.1 const config = {
plugins: {
"@tailwindcss/postcss": {},
},
};
export default config;

## 2.add this @import "tailwindcss"; on top of globals.css

## 3. Restart npm run dev
