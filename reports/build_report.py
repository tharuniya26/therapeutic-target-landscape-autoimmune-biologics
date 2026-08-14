"""Compile the professional Times New Roman LaTeX report with XeLaTeX."""
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
SOURCE = REPORTS / "autoimmune_biologics_target_landscape.tex"
OUTPUT = REPORTS / "autoimmune_biologics_target_landscape.pdf"

def build() -> None:
    engine = shutil.which("xelatex")
    if engine is None:
        raise RuntimeError("XeLaTeX is required to compile the Times New Roman report.")
    command = [engine, "-interaction=nonstopmode", "-halt-on-error", f"-output-directory={REPORTS}", str(SOURCE)]
    for _ in range(2):
        subprocess.run(command, cwd=ROOT, check=True)
    if not OUTPUT.exists() or OUTPUT.stat().st_size == 0:
        raise RuntimeError("XeLaTeX completed without producing a valid PDF.")

if __name__ == "__main__":
    build()
    print(OUTPUT)

