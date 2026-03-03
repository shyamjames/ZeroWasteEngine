# Base Image
FROM python:3.11-slim-bookworm

# Environment variables to optimize Python for Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings.prod

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies via pip
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the actual project
COPY . /app/

# Create a non-root user to run the server for security
RUN adduser --disabled-password --no-create-home myuser \
    && chown -R myuser:myuser /app
USER myuser

# Expose Django port
EXPOSE 8000

# Run gunicorn (this can be overridden by docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
