FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  POETRY_VERSION=1.7.1 \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update && apt-get install -y \
  postgresql-client \
  libpq-dev \
  gcc \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
  gunicorn \
  psycopg2-binary \
  python-decouple

COPY . .

RUN adduser --disabled-password --gecos '' django_user && \
  chown -R django_user:django_user /app
USER django_user

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health/ || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "task_manager.wsgi:application"]