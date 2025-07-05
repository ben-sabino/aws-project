FROM python:3.9-slim

WORKDIR /app

# Instalar netcat para verificar conectividade
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Tornar o script executável
RUN chmod +x start.sh

CMD ["./start.sh"] 