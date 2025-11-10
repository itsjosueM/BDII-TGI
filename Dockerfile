# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema mínimas para psycopg2
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-u", "app.py"]
