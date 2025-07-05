#!/bin/bash

# Aguardar o PostgreSQL estar pronto
echo "Aguardando PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL está pronto!"

# Iniciar a aplicação
echo "Iniciando aplicação..."
uvicorn main:app --host 0.0.0.0 --port 8000 