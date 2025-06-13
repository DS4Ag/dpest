import pytest
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

    # Configure executor
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")

    # Run notebook
    ep.preprocess(nb, {"metadata": {"path": os.path.dirname(NOTEBOOK_PATH)}})