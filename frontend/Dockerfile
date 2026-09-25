# Node.js 18 image use karenge
FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 5173

# Vite ko network par expose karne ke liye --host flag zaroori hai
CMD ["npm", "run", "dev", "--", "--host"]