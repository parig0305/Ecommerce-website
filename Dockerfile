# Base image
FROM python:3.11-slim

# Set environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static (run at build-time)
RUN python manage.py collectstatic --noinput || true

# Expose
EXPOSE 8000

# Run (default) - use gunicorn
CMD ["gunicorn", "ecommerce.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
