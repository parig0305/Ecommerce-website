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

# Run (default) - automate migrations, create superuser if missing, then start gunicorn
CMD ["/bin/sh", "-c", "python manage.py migrate && python manage.py shell -c \"from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@email.com', 'Admin@123!!')\" && gunicorn ecommerce.wsgi:application --bind 0.0.0.0:$PORT --workers 3"]
