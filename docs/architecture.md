# Architecture — rqm-ising

## Overview

`rqm-ising` is the quantum operations integration layer for calibration and QEC workflows in the RQM ecosystem. It exists as a dedicated service — separate from `rqm-core`, `rqm-compiler`, `rqm-api`, and `rqm-studio` — for deliberate architectural reasons.

---

## Why rqm-ising Exists Separately

### 1. Separation of RQM-native logic from external provider capabilities

`rqm-core` and `rqm-compiler` contain RQM's quaternionic math primitives and circuit IR. These are stable, internally-owned abstractions. `rqm-ising`, by contrast, integrates capabilities from external quantum hardware providers — initially NVIDIA Ising. Mixing vendor-specific integration logic into `rqm-core` would couple RQM's mathematical identity to the API surface of a third-party vendor, creating fragility and making future provider expansion harder.

### 2. Provider abstraction boundary

`rqm-ising` defines a provider interface (`BaseProvider`) that all hardware backends must implement. NVIDIA Ising is one implementation. Future providers (e.g., different hardware backends or decoder services) register in the same provider registry and implement the same interface. This keeps provider-specific details isolated inside `providers/{provider_name}/`.

### 3. Workflow orchestration

Calibration and QEC workflows involve multi-step coordination: submitting jobs, tracking status, storing artifacts, and generating reports. This workflow orchestration is not appropriate in `rqm-api` (which focuses on circuit optimization and execution) or `rqm-compiler` (which focuses on circuit IR). `rqm-ising` provides a dedicated orchestration layer for these operations.

### 4. Clean APIs for rqm-studio

`rqm-studio` consumes REST endpoints from `rqm-ising` to display calibration status, QEC results, and benchmark reports. Keeping this service boundary clean — with stable, typed response envelopes — ensures `rqm-studio` can evolve independently of the underlying provider implementations.

---

## System Boundaries

```
rqm-studio (frontend)
    │
    │  REST (JSON envelope)
    ▼
rqm-ising (this service)
    │
    ├── rqm-api         (circuit execution — separate concern)
    ├── rqm-compiler    (circuit IR — separate concern)
    ├── rqm-core        (math primitives — separate concern)
    │
    └── External providers
            ├── NVIDIA Ising (calibration + QEC decoding)
            └── [future providers]
```

---

## Internal Structure

```
rqm_ising/
  main.py          — FastAPI application and middleware
  config.py        — Environment-based configuration
  logging.py       — Structured logging setup

  api/             — FastAPI routers (one file per domain)
  schemas/         — Pydantic request/response models
  services/        — Business logic and persistence
  providers/       — Provider registry and adapter implementations
  workflows/       — Orchestration logic coordinating services and providers
  storage/         — Local filesystem artifact storage primitives
  utils/           — ID generation, timestamps
```

### Data Flow (example: calibration analyze)

```
POST /v1/calibration/analyze
    → calibration router
    → calibration_workflow.analyze_calibration()
    → provider registry: get_or_raise("nvidia_ising")
    → NvidiaIsingProvider.run_calibration_analysis()
    → NvidiaCalibrationAdapter.analyze()
    → NvidiaIsingClient.submit_calibration_analysis()  ← integration boundary
    ← CalibrationAnalysisResult
    ← JSON success envelope
```

---

## Persistence and Artifact Lifecycle

Current local persistence uses filesystem-backed services:

- **Job storage** (`JobService` + `JobStorage`):
  - In-memory cache for fast reads
  - Durable snapshots to `artifacts/jobs/{job_id}/job.json`
  - Startup reload via FastAPI lifespan to recover persisted jobs after restart
- **Artifact storage** (`ArtifactService`):
  - JSON report outputs written under `./artifacts/`
  - Calibration workflow writes `calibration_report.json` per job
  - QEC benchmark workflow writes `benchmark_report.json` per job
  - Benchmark report endpoint writes report artifacts under `artifacts/benchmarks/`

Job records include `artifact_paths` and `result_summary` so Studio can directly locate
first-class outputs.

---

## Security Considerations

- NVIDIA Ising credentials (`NVIDIA_ISING_API_KEY`) are loaded from environment and never logged.
- The service runs as a non-root user in Docker.
- No credentials are stored in code or committed to version control.
- CORS origins are explicitly configured, not open by default.

---

## Provider Contract

Every provider must implement `rqm_ising.providers.base.BaseProvider`:

```python
class BaseProvider(ABC):
    provider_id: str
    display_name: str
    version: str
    capabilities: list[ProviderCapability]
    credentials_configured: bool
    externally_connected: bool
    mock_only: bool
    status: ProviderStatus
    integration_mode: ProviderIntegrationMode
    summary: str

    def run_calibration_analysis(request) -> CalibrationAnalysisResult: ...
    def run_calibration_workflow(request) -> CalibrationRunResponse: ...
    def run_qec_decoding(request) -> QECDecodeSummary: ...
    def run_qec_benchmark(request) -> QECBenchmarkRunResponse: ...
```

Provider API shape:
- `GET /v1/providers` returns Studio-ready summary fields (`name`, `display_name`,
  `capabilities`, `status`, `integration_mode`, `summary`)
- `GET /v1/providers/{provider_name}` returns provider detail status/health fields.

See `PROJECT_RULES.md` for full provider implementation requirements.
