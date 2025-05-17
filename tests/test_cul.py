import dpest
from pathlib import Path
import pytest


def test_cul_template_generation(tmp_path):
    """Test generation of cultivar template files"""
    # Correct path setup
    repo_root = Path(__file__).parent.parent  # Move up to root directory
    input_file = repo_root / "tests/DSSAT48_data/Genotype/WHCER048.CUL"
    output_dir = tmp_path / "output"

    # Verify the input file exists
    assert input_file.exists(), f"Input file not found: {input_file}"

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Call the function
    params, tpl_path = dpest.wheat.ceres.cul(
        P='P1D, P5',
        G='G1, G2, G3',
        PHINT='PHINT',
        cultivar='MANITOU',
        cul_file_path=str(input_file),
        output_dir=str(output_dir)
    )

    # Verify outputs
    assert tpl_path.exists()
    # assert tpl_path.name == "WHCER048_CUL.TPL"
