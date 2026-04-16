"""
NVIDIA Ising calibration adapter.

Translates between rqm-ising's provider-agnostic calibration schemas and the
NVIDIA Ising client interface. This is the only place in the codebase where
NVIDIA-specific calibration field mappings should live.
"""

import logging

from rqm_ising.providers.nvidia_ising.client import NvidiaIsingClient
from rqm_ising.schemas.calibration import (
    CalibrationAnalysisResult,
    CalibrationAnalyzeRequest,
    CalibrationRunRequest,
    CalibrationRunResponse,
)
from rqm_ising.utils.ids import new_job_id

logger = logging.getLogger(__name__)


class NvidiaCalibrationAdapter:
    """Adapts RQM calibration schemas to/from the NVIDIA Ising client."""

    def __init__(self, client: NvidiaIsingClient) -> None:
        self._client = client

    def analyze(self, request: CalibrationAnalyzeRequest) -> CalibrationAnalysisResult:
        """
        Run a calibration analysis via NVIDIA Ising and return a structured result.

        In stub mode, returns realistic-looking mock data without calling any
        external service.
        """
        payload = {
            "experiment_id": request.experiment_id,
            "qubit_count": request.qubit_count,
            "coupling_map": request.coupling_map,
            "gate_set": request.gate_set,
            "noise_metadata": request.noise_metadata,
        }
        raw = self._client.submit_calibration_analysis(payload)
        logger.debug("nvidia calibration analysis raw response: %s", raw)

        # Translate stub/live response into the shared RQM schema
        gate_fidelities = {g: 0.997 for g in (request.gate_set or ["cx", "h", "rz"])}
        t1 = {str(q): 85.0 + q * 2.5 for q in range(request.qubit_count)}
        t2 = {str(q): 60.0 + q * 1.8 for q in range(request.qubit_count)}

        return CalibrationAnalysisResult(
            experiment_id=request.experiment_id,
            provider="nvidia_ising",
            qubit_count=request.qubit_count,
            recommended_gate_fidelities=gate_fidelities,
            t1_estimates_us=t1,
            t2_estimates_us=t2,
            noise_model_summary=(
                f"Stub noise model for {request.qubit_count}-qubit device. "
                "Replace with NVIDIA Ising live analysis in Phase 2."
            ),
            analysis_warnings=(
                ["Running in stub mode — results are illustrative, not measured."]
                if not self._client.is_live
                else []
            ),
        )

    def run_workflow(self, request: CalibrationRunRequest) -> CalibrationRunResponse:
        """Submit a calibration workflow job via NVIDIA Ising."""
        payload = {
            "experiment_id": request.experiment_id,
            "qubit_count": request.qubit_count,
            "coupling_map": request.coupling_map,
            "gate_set": request.gate_set,
            "workflow_params": request.workflow_params,
        }
        raw = self._client.submit_calibration_workflow(payload)
        logger.debug("nvidia calibration workflow raw response: %s", raw)

        return CalibrationRunResponse(
            job_id=new_job_id(),
            provider="nvidia_ising",
            experiment_id=request.experiment_id,
            status="pending",
        )
