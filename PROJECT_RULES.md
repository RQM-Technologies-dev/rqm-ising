# PROJECT_RULES.md — rqm-ising

This document defines the architectural and behavioral rules for contributors and coding agents working in this repository. Follow these rules strictly to maintain the integrity and purpose of `rqm-ising` within the RQM ecosystem.

---

## 1. This Repo Is an Integration/Orchestration Layer

`rqm-ising` is **not** the home of quaternionic compiler logic, circuit IR, or RQM-native math primitives.

Those belong in:
- `rqm-core` — quaternion math and shared foundations
- `rqm-compiler` — circuit IR and optimization passes
- `rqm-api` — circuit optimization and execution API

This repo is the home of:
- NVIDIA Ising integration (and future quantum hardware providers)
- Calibration workflow orchestration
- QEC decoder workflow orchestration
- Experiment and job management
- Benchmark and report generation
- Clean REST APIs for `rqm-studio` to consume

**If a change belongs in `rqm-core` or `rqm-compiler`, do not put it here.**

---

## 2. Keep Provider Boundaries Clean

All provider-specific logic must live inside `rqm_ising/providers/{provider_name}/`.

Shared schemas, services, and workflow code must **not** contain vendor-specific assumptions. The NVIDIA Ising adapter is one implementation of the provider interface—it is not the default or only concept in the system.

Rules:
- Shared schemas in `rqm_ising/schemas/` must be provider-agnostic.
- Workflow orchestration code must not import from `providers/nvidia_ising/` directly—it should go through the provider registry.
- If you find yourself writing `if provider == "nvidia_ising":` in workflow or API code, you are doing it wrong.

---

## 3. Every New Provider Must Implement the Shared Provider Interface

All providers must implement `rqm_ising.providers.base.BaseProvider`.

The base class defines the required interface:
- `provider_id` — unique string identifier
- `display_name` — human-readable name
- `capabilities` — list of `ProviderCapability` values
- `run_calibration_analysis(...)` — provider calibration analysis
- `run_calibration_workflow(...)` — provider calibration workflow
- `run_qec_decoding(...)` — provider QEC decoding
- `run_qec_benchmark(...)` — provider QEC benchmark

Do not bypass this interface for convenience.

---

## 4. Avoid Vendor-Specific Assumptions in Shared Schemas

Schemas in `rqm_ising/schemas/` define the API contract between `rqm-ising` and its consumers (primarily `rqm-studio`).

- Do not add NVIDIA-specific fields to shared schemas.
- Use `provider_config: dict` or `provider_metadata: dict` extension points for vendor-specific data.
- Shared schemas must remain stable across provider changes.

---

## 5. Keep Request/Response Contracts Stable

The API contract (schemas + endpoints) is consumed by `rqm-studio` and potentially by external clients.

- Do not remove or rename fields in existing response schemas without a versioning plan.
- Use the envelope format consistently:
  ```json
  {"status": "success", "data": ..., "meta": {"request_id": "...", "processing_time_ms": ...}}
  ```
- All error responses must use the error envelope format.
- Prefer additive changes over breaking changes.

---

## 6. Preserve Enterprise-Safe Language

In all documentation, comments, and string literals:
- Describe this repo as "the quantum operations integration layer for calibration and QEC workflows in the RQM ecosystem."
- Do not describe it as replacing RQM logic.
- Do not imply NVIDIA Ising is owned by or part of RQM.
- Make it clear this repo integrates external capabilities into the RQM product environment.
- Do not make speculative performance claims unless they are backed by benchmarks run through this system.

---

## 7. Prefer Modularity Over Cleverness

- Keep files focused. Each module should have one clear responsibility.
- Avoid large, multi-purpose utility files.
- Prefer explicit imports over wildcard imports.
- Keep the provider registry and workflow orchestration decoupled.

---

## 8. Persistence and Storage Rules

- The current implementation uses in-memory job storage and local filesystem artifact storage.
- Do not add database dependencies without a design discussion.
- Structure new code so persistence can be upgraded to a database later without rewriting the API layer.
- All artifact writes must go through `ArtifactService`, not direct filesystem calls in routers or workflows.

---

## 9. Testing Requirements

- Every new endpoint must have at least one test in `tests/`.
- Tests must use the FastAPI `TestClient` and must not require live external services.
- Provider adapters must be stubbed in tests.
- Do not add tests that require NVIDIA credentials or live NVIDIA Ising endpoints.

---

## 10. Do Not Break the CI Pipeline

- All changes must pass `pytest` before merging.
- Do not remove or weaken existing tests.
- If a test is failing due to a legitimate bug you introduced, fix the bug—don't delete the test.
