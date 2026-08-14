"""Execute every project notebook in-place using the installed nbclient engine."""

from __future__ import annotations
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("JUPYTER_CONFIG_DIR", str(ROOT / ".jupyter/config"))
os.environ.setdefault("JUPYTER_DATA_DIR", str(ROOT / ".jupyter/data"))
os.environ.setdefault("JUPYTER_RUNTIME_DIR", str(ROOT / ".jupyter/runtime"))
os.environ.setdefault("IPYTHONDIR", str(ROOT / ".jupyter/ipython"))

import nbformat
from nbclient import NotebookClient


def main() -> None:
    for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
        notebook = nbformat.read(path, as_version=4)
        client = NotebookClient(notebook, timeout=180, kernel_name="python3", resources={"metadata": {"path": str(ROOT)}})
        client.execute()
        nbformat.write(notebook, path)
        executed = sum(cell.get("execution_count") is not None for cell in notebook.cells if cell.cell_type == "code")
        print(f"{path.name}: {executed} code cells executed")


if __name__ == "__main__":
    main()

