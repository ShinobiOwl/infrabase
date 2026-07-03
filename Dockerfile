FROM python:3.11-slim

# System dependencies for mysqlclient
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential pkg-config && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files for WhiteNoise to serve
RUN python manage.py collectstatic --noinput

EXPOSE 5000

# Gunicorn production server (Port 5000 for Caddy)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "infrabase_project.wsgi:application"]