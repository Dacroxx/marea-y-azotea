"""Build the approved editorial reference; no catalog mutation or installs."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).resolve().parents[1]/"source/build_editorial.py"),run_name="__main__")
