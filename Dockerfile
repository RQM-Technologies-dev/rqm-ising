FROM python:3.11-slim@sha256:db3ff2e1800a8581e2c48a27c3995339d47bdf046da21c7627accd3d51053a93

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    RQM_ISING_ARTIFACT_DIR=/app/artifacts \
    RQM_ISING_JOBS_DIR=/app/artifacts/jobs

COPY pyproject.toml ./
COPY README.md LICENSE ./
COPY rqm_ising/ ./rqm_ising/

RUN pip install --no-cache-dir . \
    && python -c "from rqm_ising.main import app; assert app.title == 'RQM Ising API'" \
    && useradd --create-home --uid 10001 --shell /usr/sbin/nologin appuser \
    && mkdir -p /app/artifacts/jobs \
    && chown -R appuser:appuser /app/artifacts

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c \
        "import urllib.request, sys; \
         urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4); \
         sys.exit(0)" \
    || exit 1

CMD ["uvicorn", "rqm_ising.main:app", "--host", "0.0.0.0", "--port", "8000"]
