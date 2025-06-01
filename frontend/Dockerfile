FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

# Instalar todas as dependências necessárias
RUN npm install && \
    npm install @mui/material @emotion/react @emotion/styled axios @types/axios && \
    npm install -g serve

COPY . .

# Build the app
RUN npm run build

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"] 