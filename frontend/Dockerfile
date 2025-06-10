
# Etapa de build do frontend (se aplica a projetos React/Vite)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build # Este comando deve gerar os arquivos estáticos na pasta 'dist' (ou similar)

# Etapa para o servidor Nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html 
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf 

EXPOSE 80 
CMD nginx -g "daemon off;"