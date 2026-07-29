# rqm-ising

> **Archived July 28, 2026.** This repository preserves a closed NVIDIA Ising
> calibration/QEC integration attempt. The provider client never advanced
> beyond illustrative stubs, and configured live operations remain
> unimplemented. It is not an active RQM Studio service, dependency, release,
> or product roadmap.

The code is retained read-only for historical architecture and schema
reference. Mock outputs are not measurements, provider results, customer
evidence, or proof of a working NVIDIA integration.

---

## Scientific boundary

Complete quaternion and complete conventional complex/SU(2) representations
carry the same information for the supported transformations. Quaternion
coordinates may make ordered rotation structure, residuals, or diagnostics
easier to implement and inspect; they do not create additional measurement
information or establish unique calibration or QEC performance.

---

## Historical role

| Repo | Responsibility |
|------|---------------|
| `rqm-core` | Quaternion math primitives and shared foundations |
| `rqm-compiler` | Circuit IR and optimization passes |
| `rqm-api` | Circuit optimization and execution API |
| `rqm-studio` | Main frontend product shell |
| **`rqm-ising`** | Archived NVIDIA Ising integration attempt |

No active RQM Studio surface should call this service. A future provider
integration must begin from a real provider contract, named consumer,
representative workflow, and independently approved roadmap rather than
reactivating the mock responses.

---

## Features (Day One)

- **Provider registry** — enumerate available quantum operation providers and their capabilities
- **Calibration workflows** — submit calibration tasks and retrieve structured analysis results
- **QEC workflows** — submit syndrome decoding tasks and benchmark decoder approaches
- **Persistent local job management** — in-memory cache backed by local JSON job snapshots for restart-safe development
- **Artifact/report lifecycle** — workflow completions emit structured JSON reports and attach artifact paths to jobs
- **Studio-facing benchmark reporting** — generate comparison-rich report payloads designed for future `rqm-studio` UI views
- **NVIDIA Ising adapter boundary** — clean integration stubs for NVIDIA Ising calibration and decoding

---

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Setup

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install in development mode with dev extras
pip install -e ".[dev]"

# Copy environment template
cp .env.example .env
```

### Running the Server

```bash
uvicorn rqm_ising.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Running Tests

```bash
pytest
```

---

## Docker

```bash
docker build -t rqm-ising .
docker run -p 8000:8000 rqm-ising
```

Versioned multi-architecture images are published to
`ghcr.io/rqm-technologies-dev/rqm-ising` after a reviewed Release Please pull
request is merged. Published images run as an unprivileged user, include
BuildKit provenance and an SBOM, and must pass health and fixable-critical
vulnerability gates.

---

## API Overview

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/version` | API version |
| GET | `/v1/providers` | List providers with status and integration mode |
| GET | `/v1/providers/{provider_name}` | Provider health/detail view |
| POST | `/v1/calibration/analyze` | Analyze calibration experiment metadata |
| POST | `/v1/calibration/run` | Submit a calibration workflow job |
| POST | `/v1/qec/decode` | Decode syndrome data |
| POST | `/v1/qec/benchmark` | Submit a QEC benchmark job |
| GET | `/v1/jobs` | List all jobs |
| GET | `/v1/jobs/{job_id}` | Get a specific job |
| GET | `/v1/benchmarks/report` | Get a structured benchmark report |

Full API documentation: [docs/api.md](docs/api.md)

## Local persistence and artifacts

- Jobs are cached in memory and persisted to disk at `artifacts/jobs/<job_id>/job.json`.
- On startup, the service reloads persisted jobs into memory.
- Calibration and QEC benchmark workflow submissions generate structured artifacts:
  - `artifacts/jobs/<job_id>/calibration_report.json`
  - `artifacts/jobs/<job_id>/benchmark_report.json`
- Job records include `artifact_paths` and `result_summary` fields that point directly to report outputs.

---

## Architecture

See [docs/architecture.md](docs/architecture.md) for system boundaries and design decisions.

## Roadmap

See [docs/roadmap.md](docs/roadmap.md) for the phased delivery plan.

---

## Repository Rules

See [PROJECT_RULES.md](PROJECT_RULES.md) for guidance on contributing to this repo.

---

## License

Apache 2.0. See [LICENSE](LICENSE).
