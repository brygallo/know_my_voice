# Usa Python como base
FROM python:3.10

# Configuración del entorno
ENV PYTHONUNBUFFERED=1

# Define el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos e instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación
COPY . .

# Ejecutar `collectstatic` antes de iniciar Gunicorn
RUN python manage.py collectstatic --noinput

# Permisos de ejecución para el entrypoint
RUN chmod +x /app/docker/entrypoint.sh

# Ejecuta el script de inicio
CMD ["/app/docker/entrypoint.sh"]
