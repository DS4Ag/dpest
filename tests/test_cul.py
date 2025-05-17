import dpest
from pathlib import Path
import pytest


def test_cul_template_generation(tmp_path):
    """Test generation of cultivar template files."""
    # Setup paths
    repo_root = Path(__file__).parent.parent
    input_file = repo_root / "tests/DSSAT48_data/Genotype/WHCER048.CUL"
    output_dir = tmp_path / "output"

    # Ensure the input file exists
    assert input_file.exists(), f"Input file not found: {input_file}"

    # Create the output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Call the dpest.wheat.ceres.cul function and check return
    result = dpest.wheat.ceres.cul(
        P='P1D, P5',
        G='G1, G2, G3',
        PHINT='PHINT',
        cultivar='MANITOU',
        cul_file_path=input_file,
        output_path=output_dir
    )

    assert result is not None, "Function returned None"
    assert isinstance(result, tuple) and len(result) == 2, "Unexpected return value format"

    params, tpl_path = result

    # Validate the output template file
    assert tpl_path.exists(), f"Template file not created: {tpl_path}"
    # Optional: check contents or filename
    # assert tpl_path.name == "WHCER048_CUL.TPL"
