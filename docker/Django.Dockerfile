FROM python:3.10-slim
WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev build-essential pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput || true

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "infrabase_project.wsgi:application"]