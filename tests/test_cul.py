import dpest
from pathlib import Path
import pytest


def test_cul_template_generation(tmp_path):
    """Test generation of cultivar template files"""
    # Setup tests environment
    test_data_dir = Path(__file__).parent
    input_file = test_data_dir / "DSSAT48_data/Genotype/WHCER048.CUL"
    output_dir = tmp_path / "output"

    # Create tests output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Call the function under tests
    params, tpl_path = dpest.wheat.ceres.cul(
        P='P1D, P5',
        G='G1, G2, G3',
        PHINT='PHINT',
        cultivar='MANITOU',
        cul_file_path=str(input_file),
        output_dir=str(output_dir)
    )

    # Verify file creation
    assert tpl_path.exists()
    assert tpl_path.name == "WHCER048_CUL.TPL"
