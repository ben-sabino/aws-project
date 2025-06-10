# Estágio 1: Construção (Build)
# Usa a imagem completa do Node para instalar dependências e construir o projeto
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Estágio 2: Servidor de Produção (Serve)
# Usa uma imagem super leve do Nginx para servir os arquivos estáticos gerados no estágio 1
FROM nginx:stable-alpine
# Copia os arquivos da pasta 'dist' do estágio de build para a pasta padrão do Nginx
COPY --from=build /app/dist /usr/share/nginx/html
# Expõe a porta 80, que é a porta padrão do Nginx
EXPOSE 80
# O comando padrão do Nginx já é iniciar o servidor, então não precisamos de um CMD