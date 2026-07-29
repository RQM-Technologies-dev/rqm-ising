"""rqm-ising — quantum operations integration layer for calibration and QEC workflows."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("rqm-ising")
except PackageNotFoundError:  # pragma: no cover - source tree without installation
    __version__ = "0.0.0+unknown"
