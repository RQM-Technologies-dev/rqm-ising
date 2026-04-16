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

Returns the API version string.

```json
{"version": "0.1.0"}
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
      "provider_id": "nvidia_ising",
      "display_name": "NVIDIA Ising",
      "version": "0.1.0-stub",
      "capabilities": ["calibration_analysis", "calibration_workflows", "qec_decoding", "qec_benchmarking"],
      "description": "...",
      "is_available": true
    }
  ],
  "total": 1
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
  "status": "pending"
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
  "status": "pending"
}
```

---

## Jobs

### GET /v1/jobs

List all jobs.

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
  "status": "pending",
  "provider": "nvidia_ising",
  "input_summary": {"experiment_id": "exp-001", "qubit_count": 4},
  "artifact_paths": [],
  "result_summary": null,
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
  "code_type": "surface_code",
  "distance": 5,
  "provider": "nvidia_ising",
  "entries": [
    {"decoder": "mwpm", "logical_error_rate": 0.0012, "avg_decode_time_ms": 4.2, "rounds_tested": 1000},
    {"decoder": "union_find", "logical_error_rate": 0.0018, "avg_decode_time_ms": 1.8, "rounds_tested": 1000}
  ],
  "summary": "...",
  "artifact_path": "./artifacts/benchmarks/report_abcd1234.json"
}
```
