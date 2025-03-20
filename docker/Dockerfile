# Use Python as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set execution permissions for entrypoint.sh
RUN chmod +x /app/docker/entrypoint.sh

# Start the container using entrypoint.sh
CMD ["/app/docker/entrypoint.sh"]
