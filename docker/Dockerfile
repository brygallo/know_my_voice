# Use Python as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Instala PostgreSQL Client (para usar psql)
RUN apt-get update && apt-get install -y postgresql-client

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Start the container using entrypoint.sh
CMD ["sh", "-c", "chmod +x /app/docker/entrypoint.sh && /app/docker/entrypoint.sh"]
