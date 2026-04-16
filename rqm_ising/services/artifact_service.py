"""
Artifact service — writes experiment outputs to local filesystem storage.

The interface is designed so the backing store can be replaced with object
storage (e.g. S3-compatible) without changing callers.
"""

import json
import logging
from pathlib import Path

from rqm_ising.config import get_settings
from rqm_ising.utils.ids import new_artifact_id
from rqm_ising.utils.timestamps import utcnow_iso

logger = logging.getLogger(__name__)


class ArtifactService:
    """Read/write artifacts under a configured base directory."""

    def __init__(self, base_dir: str | None = None) -> None:
        settings = get_settings()
        self._base = Path(base_dir or settings.artifact_dir).resolve()

    def ensure_dir(self, sub_path: str = "") -> Path:
        """Create and return an artifact subdirectory."""
        target = self._base / sub_path if sub_path else self._base
        target.mkdir(parents=True, exist_ok=True)
        return target

    def write_json(self, data: dict, filename: str | None = None, sub_path: str = "") -> Path:
        """
        Serialize *data* to a JSON file and return its absolute path.

        If *filename* is omitted, a unique artifact ID is used as the filename.
        """
        directory = self.ensure_dir(sub_path)
        name = filename or f"{new_artifact_id()}.json"
        file_path = directory / name
        payload = {
            "written_at": utcnow_iso(),
            "data": data,
        }
        file_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
        logger.debug("Artifact written: %s", file_path)
        return file_path

    def read_json(self, file_path: str | Path) -> dict:
        """Read and parse a JSON artifact file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Artifact not found: {path}")
        return json.loads(path.read_text(encoding="utf-8"))


# Module-level singleton
_artifact_service = ArtifactService()


def get_artifact_service() -> ArtifactService:
    return _artifact_service
