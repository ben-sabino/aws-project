
# Etapa de build do frontend (se aplica a projetos React/Vite)
FROM node:20-slim AS builder
WORKDIR /app

# Install Python for native dependency building (required for some npm packages)
RUN apt-get update && apt-get install -y python3 make g++ && rm -rf /var/lib/apt/lists/*

COPY package*.json ./

# Clear npm cache and install dependencies with platform-specific Rollup
RUN npm cache clean --force
RUN npm install --legacy-peer-deps
RUN npm install @rollup/rollup-linux-x64-gnu --save-dev --legacy-peer-deps

COPY . .
RUN npm run build

# Etapa para o servidor Nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html 
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf 

EXPOSE 80 
CMD nginx -g "daemon off;"