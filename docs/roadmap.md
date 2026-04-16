# Roadmap — rqm-ising

This document describes the planned phased delivery of `rqm-ising`.

---

## Phase 1 — Local Mock Service ✅

**Goal:** Runnable service with typed API contracts, no external dependencies required.

- FastAPI application with all planned endpoints
- Pydantic request/response schemas for all domains
- Provider abstraction with NVIDIA Ising stub adapter
- In-memory job service
- Local filesystem artifact storage
- Benchmark report generation (mock data)
- pytest test suite for all endpoints
- Docker-ready
- GitHub Actions CI-ready

**Status:** Complete in initial scaffold.

---

## Phase 2 — Provider-Backed NVIDIA Ising Integration

**Goal:** Replace stubs with real calls to the NVIDIA Ising backend.

- Implement live HTTP calls in `NvidiaIsingClient`
- Add authentication handling (API key via environment)
- Handle NVIDIA Ising response parsing and error mapping
- Add async job polling for long-running calibration and benchmark jobs
- Integrate NVIDIA Ising job IDs with the RQM job service
- Add integration tests (requires credentials, run separately from unit tests)
- Document NVIDIA Ising configuration in `.env.example` and README

---

## Phase 3 — RQM Studio Integration

**Goal:** Make `rqm-ising` consumable by `rqm-studio` for production use.

- Finalize API contract versions (`/v1/` prefix already in place)
- Add pagination to job list endpoint
- Add job filtering by status and type
- Add webhook/callback support for job completion events
- Review and harden CORS configuration
- Add OpenAPI schema export for `rqm-studio` SDK generation
- End-to-end integration tests with `rqm-studio`

---

## Phase 4 — Benchmark and Reporting Expansion

**Goal:** Build a complete, data-driven benchmark reporting pipeline.

- Replace mock benchmark reports with real job-backed data
- Store benchmark results in a durable backend (database or object storage)
- Add benchmark history and trend queries
- Add comparative reports across providers
- Export reports as structured JSON and PDF
- Add time-series analysis for calibration drift detection

---

## Phase 5 — Multi-Provider Quantum Operations Layer

**Goal:** Expand beyond NVIDIA Ising to support additional quantum hardware backends.

- Add a second provider implementation (provider TBD)
- Implement provider capability routing (select best provider for a given task)
- Add provider health monitoring and failover
- Document provider onboarding process (see PROJECT_RULES.md)
- Add provider-level rate limiting and cost tracking
- Evaluate standardization against emerging quantum operations APIs

---

## Out of Scope (Permanently)

These concerns belong in other RQM repos and should never be added to `rqm-ising`:

- Quaternionic math primitives → `rqm-core`
- Circuit IR or optimization passes → `rqm-compiler`
- Circuit execution API → `rqm-api`
- Frontend UI components → `rqm-studio`
