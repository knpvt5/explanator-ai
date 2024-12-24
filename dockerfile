# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment in /opt/venv
RUN python -m venv /opt/venv

# Install dependencies
COPY requirements.txt .
RUN . /opt/venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Collect static files
RUN . /opt/venv/bin/activate && python manage.py collectstatic --no-input

# Expose the port the app runs on
EXPOSE 8000

# Make entrypoint executable
RUN chmod +x /usr/src/app/entrypoint.sh

# Set the entrypoint script
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]