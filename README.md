# rqm-ising

**The quantum operations integration layer for calibration and QEC workflows in the RQM ecosystem.**

`rqm-ising` connects external quantum hardware capabilities—initially NVIDIA Ising—into the broader RQM stack. It does not contain RQM's native compiler or quaternion math logic. Instead, it orchestrates calibration workflows, QEC decoder workflows, experiment/job management, and benchmark reporting through clean, typed REST APIs.

---

## Role in the RQM Ecosystem

| Repo | Responsibility |
|------|---------------|
| `rqm-core` | Quaternion math primitives and shared foundations |
| `rqm-compiler` | Circuit IR and optimization passes |
| `rqm-api` | Circuit optimization and execution API |
| `rqm-studio` | Main frontend product shell |
| **`rqm-ising`** | Quantum operations integration layer for calibration + QEC workflows |

`rqm-ising` treats NVIDIA Ising as one external provider among potentially many. Its provider abstraction is designed to accommodate future hardware backends beyond NVIDIA.

---

## Features (Day One)

- **Provider registry** — enumerate available quantum operation providers and their capabilities
- **Calibration workflows** — submit calibration tasks and retrieve structured analysis results
- **QEC workflows** — submit syndrome decoding tasks and benchmark decoder approaches
- **Job management** — track async workflow jobs with status, artifacts, and result summaries
- **Benchmark reporting** — generate structured reports comparing decoder or calibration approaches
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

---

## API Overview

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/version` | API version |
| GET | `/v1/providers` | List providers and capabilities |
| POST | `/v1/calibration/analyze` | Analyze calibration experiment metadata |
| POST | `/v1/calibration/run` | Submit a calibration workflow job |
| POST | `/v1/qec/decode` | Decode syndrome data |
| POST | `/v1/qec/benchmark` | Submit a QEC benchmark job |
| GET | `/v1/jobs` | List all jobs |
| GET | `/v1/jobs/{job_id}` | Get a specific job |
| GET | `/v1/benchmarks/report` | Get a structured benchmark report |

Full API documentation: [docs/api.md](docs/api.md)

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
