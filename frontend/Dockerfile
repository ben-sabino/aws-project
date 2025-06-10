
# Etapa de build do frontend (se aplica a projetos React/Vite)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build # Este comando deve gerar os arquivos estáticos na pasta 'dist' (ou similar)

# Etapa para o servidor Nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html # Copia os arquivos compilados para o Nginx
COPY ./frontend/nginx/nginx.conf /etc/nginx/conf.d/default.conf # <--- ADICIONE/MODIFIQUE ESTA LINHA

EXPOSE 80 
CMD ["nginx", "-g", "daemon off;"] # Inicia o Nginx