"""
Local filesystem storage implementation.

Provides low-level read/write primitives used by ArtifactService.
Keeping this separate from ArtifactService makes it easy to swap the
storage backend (e.g., to S3) without touching service logic.
"""

import json
from pathlib import Path


def ensure_directory(path: str | Path) -> Path:
    """Create *path* (and parents) if it does not exist. Return the Path object."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_json_file(path: str | Path, data: dict) -> Path:
    """Serialize *data* as pretty-printed JSON and write to *path*."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    return p


def read_json_file(path: str | Path) -> dict:
    """Read and parse a JSON file at *path*."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def list_files(directory: str | Path, pattern: str = "*") -> list[Path]:
    """Return a sorted list of files matching *pattern* under *directory*."""
    d = Path(directory)
    if not d.exists():
        return []
    return sorted(d.glob(pattern))
