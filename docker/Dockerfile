# Use Python as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# 🛠️ Instala el cliente de PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client

# Instala dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Inicia el contenedor ejecutando el script de arranque
CMD ["sh", "-c", "chmod +x /app/docker/entrypoint.sh && /app/docker/entrypoint.sh"]
