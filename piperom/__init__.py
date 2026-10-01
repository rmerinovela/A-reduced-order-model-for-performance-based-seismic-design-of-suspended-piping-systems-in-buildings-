"""Reduced-order model for performance-based seismic design of suspended piping systems.

Units throughout: N, mm, s (mass in tonnes = N*s^2/mm).
"""

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_DIR = PACKAGE_DIR.parent
INPUTS_DIR = REPO_DIR / "inputs"            # the engine reads data only from inputs/ (and motions/)
DEFAULTS_DIR = INPUTS_DIR / "defaults"
TRAPEZES_DIR = INPUTS_DIR / "trapezes"

__version__ = "0.1.0"
