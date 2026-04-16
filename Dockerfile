FROM python:3.11-slim

WORKDIR /app

# Install dependencies before copying source for better layer caching
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e "."

# Copy application source
COPY rqm_ising/ ./rqm_ising/

# Create artifact storage directory
RUN mkdir -p /app/artifacts

# Non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "rqm_ising.main:app", "--host", "0.0.0.0", "--port", "8000"]
