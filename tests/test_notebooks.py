import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

NOTEBOOK_PATH = os.path.join(
    os.path.dirname(__file__), "..", "examples", "wheat", "ceres", "usage_example.ipynb"
)

def test_notebook_execution():
    # Load notebook
    with open(NOTEBOOK_PATH, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # Skip cells tagged with "skip-in-ci" if running in CI
    if os.environ.get("CI") == "true":
        skipped_cells = []
        for cell in nb.cells:
            if "skip-in-ci" in cell.metadata.get("tags", []):
                skipped_cells.append(cell)
        nb.cells = [cell for cell in nb.cells if cell not in skipped_cells]

    # Configure executor
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")

    # Run notebook
    ep.preprocess(nb, {"metadata": {"path": os.path.dirname(NOTEBOOK_PATH)}})