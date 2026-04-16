# API Reference — rqm-ising

All endpoints return a consistent JSON envelope:

**Success:**
```json
{
  "status": "success",
  "data": { ... },
  "meta": {
    "request_id": "req_abc123",
    "processing_time_ms": 12.3
  }
}
```

**Error:**
```json
{
  "status": "error",
  "error": {
    "code": "provider_not_found",
    "message": "Provider 'unknown' is not registered."
  },
  "meta": {
    "request_id": "req_abc123",
    "processing_time_ms": 1.1
  }
}
```

---

## Meta Endpoints

### GET /health

Health check. Returns `{"healthy": true}` in the `data` field.

### GET /version

Returns the API version string in the standard success envelope.

```json
{
  "status": "success",
  "data": {"version": "0.1.0"},
  "meta": {
    "request_id": "req_abc123",
    "processing_time_ms": 0.8
  }
}
```

---

## Providers

### GET /v1/providers

List all registered providers and their capabilities.

**Response `data`:**
```json
{
  "providers": [
    {
      "name": "nvidia_ising",
      "display_name": "NVIDIA Ising",
      "capabilities": ["calibration_analysis", "calibration_workflows", "qec_decoding", "qec_benchmarking"],
      "status": "available",
      "integration_mode": "mock",
      "summary": "NVIDIA Ising running in local mock mode; external calls are stubbed."
    }
  ],
  "total": 1
}
```

### GET /v1/providers/{provider_name}

Returns provider detail and integration health metadata.

**Response `data`:**
```json
{
  "name": "nvidia_ising",
  "display_name": "NVIDIA Ising",
  "version": "0.1.0-stub",
  "capabilities": ["calibration_analysis", "calibration_workflows", "qec_decoding", "qec_benchmarking"],
  "status": "available",
  "availability": true,
  "credentials_configured": false,
  "externally_connected": false,
  "mock_only": true,
  "integration_mode": "mock",
  "summary": "NVIDIA Ising running in local mock mode; external calls are stubbed.",
  "description": "Integration adapter for NVIDIA Ising quantum operations."
}
```

---

## Calibration

### POST /v1/calibration/analyze

Analyze calibration experiment metadata and return a structured result.

**Request body:**
```json
{
  "experiment_id": "exp-001",
  "qubit_count": 4,
  "coupling_map": [[0,1],[1,2],[2,3]],
  "gate_set": ["cx", "h", "rz"],
  "noise_metadata": {},
  "provider": "nvidia_ising"
}
```

**Response `data`:**
```json
{
  "experiment_id": "exp-001",
  "provider": "nvidia_ising",
  "qubit_count": 4,
  "recommended_gate_fidelities": {"cx": 0.997, "h": 0.997, "rz": 0.997},
  "t1_estimates_us": {"0": 85.0, "1": 87.5, "2": 90.0, "3": 92.5},
  "t2_estimates_us": {"0": 60.0, "1": 61.8, "2": 63.6, "3": 65.4},
  "noise_model_summary": "...",
  "analysis_warnings": ["Running in stub mode — results are illustrative, not measured."]
}
```

### POST /v1/calibration/run

Submit a calibration workflow job. Returns a job handle.

**Request body:**
```json
{
  "experiment_id": "exp-001",
  "qubit_count": 4,
  "coupling_map": [[0,1]],
  "gate_set": ["cx"],
  "workflow_params": {},
  "provider": "nvidia_ising"
}
```

**Response `data`:**
```json
{
  "job_id": "job_abcdef01234567",
  "provider": "nvidia_ising",
  "experiment_id": "exp-001",
  "status": "completed",
  "artifact_paths": ["/workspace/artifacts/jobs/job_abcdef01234567/calibration_report.json"],
  "result_summary": {
    "report_artifact": "/workspace/artifacts/jobs/job_abcdef01234567/calibration_report.json",
    "report_type": "calibration_report",
    "summary": "Calibration workflow completed with structured report artifact output."
  }
}
```

---

## QEC

### POST /v1/qec/decode

Decode syndrome data and return a structured summary.

**Request body:**
```json
{
  "run_id": "run-001",
  "code_type": "surface_code",
  "distance": 5,
  "syndrome_data": [[0,1,0,1],[1,0,1,0]],
  "decoder": "mwpm",
  "provider": "nvidia_ising"
}
```

**Response `data`:**
```json
{
  "run_id": "run-001",
  "provider": "nvidia_ising",
  "code_type": "surface_code",
  "distance": 5,
  "decoder": "mwpm",
  "logical_error_rate": 0.0012,
  "correction_count": 0,
  "rounds_processed": 2,
  "decode_time_ms": 4.2,
  "warnings": ["Running in stub mode — results are illustrative, not measured."]
}
```

### POST /v1/qec/benchmark

Submit a QEC benchmark job comparing decoder approaches.

**Request body:**
```json
{
  "benchmark_id": "bench-001",
  "code_type": "surface_code",
  "distance": 5,
  "decoders": ["mwpm", "union_find"],
  "rounds": 1000,
  "provider": "nvidia_ising"
}
```

**Response `data`:**
```json
{
  "job_id": "job_abcdef01234567",
  "provider": "nvidia_ising",
  "benchmark_id": "bench-001",
  "status": "completed",
  "artifact_paths": ["/workspace/artifacts/jobs/job_abcdef01234567/benchmark_report.json"],
  "result_summary": {
    "message": "QEC benchmark completed with Studio-ready benchmark artifact.",
    "benchmark_report_path": "/workspace/artifacts/jobs/job_abcdef01234567/benchmark_report.json",
    "provider_status": "mock_mode",
    "benchmark_id": "bench-001"
  }
}
```

---

## Jobs

### GET /v1/jobs

List all jobs (in-memory cache backed by persisted filesystem records).

**Response `data`:**
```json
{
  "jobs": [...],
  "total": 3
}
```

### GET /v1/jobs/{job_id}

Get a specific job by ID.

**Response `data`:** (Job object)
```json
{
  "job_id": "job_abcdef01234567",
  "type": "calibration_workflow",
  "status": "completed",
  "provider": "nvidia_ising",
  "input_summary": {"experiment_id": "exp-001", "qubit_count": 4},
  "artifact_paths": ["/workspace/artifacts/jobs/job_abcdef01234567/calibration_report.json"],
  "result_summary": {
    "report_artifact": "/workspace/artifacts/jobs/job_abcdef01234567/calibration_report.json",
    "report_type": "calibration_report",
    "summary": "Calibration workflow completed with structured report artifact output."
  },
  "created_at": "2024-01-01T00:00:00+00:00",
  "updated_at": "2024-01-01T00:00:00+00:00"
}
```

**404 Error** if job not found.

---

## Benchmarks

### GET /v1/benchmarks/report

Return a structured benchmark report.

**Query parameters:**
- `code_type` (default: `surface_code`)
- `distance` (default: `5`)
- `provider` (default: `nvidia_ising`)

**Response `data`:**
```json
{
  "report_id": "report_abcd1234",
  "benchmark_type": "qec_surface_code_d5",
  "provider": "nvidia_ising",
  "created_at": "2026-04-16T00:00:00+00:00",
  "summary": {
    "headline": "QEC benchmark for surface_code d=5",
    "key_findings": ["Candidate decoder reduces latency in mock benchmark path."]
  },
  "comparisons": [
    {
      "decoder_baseline": "mwpm",
      "decoder_candidate": "union_find",
      "logical_error_rate": 0.0018,
      "syndrome_density_reduction": 0.17,
      "estimated_latency_ms": 1.8,
      "confidence": 0.74,
      "notes": "Mock comparison values for Studio integration prototyping."
    }
  ],
  "metrics": [
    {
      "name": "estimated_latency_ms",
      "value": 1.8,
      "unit": "ms",
      "direction": "lower_is_better",
      "notes": "Estimated candidate decode latency."
    }
  ],
  "artifact_paths": ["/workspace/artifacts/benchmarks/report_abcd1234.json"],
  "artifacts": [
    {
      "path": "/workspace/artifacts/benchmarks/report_abcd1234.json",
      "kind": "benchmark_report",
      "format": "json",
      "label": "QEC benchmark report"
    }
  ],
  "recommended_next_step": "Run provider-backed benchmark with production syndrome traces and validate candidate decoder confidence interval.",
  "notes": [
    "Mock report generated for local development.",
    "Replace values with provider-derived benchmark telemetry when available."
  ]
}
```
