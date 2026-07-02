FROM python:3.13-slim

WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry package manager
RUN pip install --upgrade pip setuptools wheel poetry

# Copy dependency files
COPY pyproject.toml poetry.lock* ./


# Configure Poetry to avoid creating virtual environments and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy application source code
COPY api/ /app/api/
COPY application/ /app/application/
COPY domain/ /app/domain/
COPY infrastructure/ /app/infrastructure/
COPY config/ /app/config/

COPY .env.dev /app/.env.dev

# Create a non-root user
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup \
    && chown -R appuser:appgroup /app

USER appuser

# Expose port 8080 for the application
EXPOSE 8080

# Start the app with Gunicorn using Uvicorn workers
CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", \
    "-b", "0.0.0.0:8080", "--timeout", "300", "api.main:app"]