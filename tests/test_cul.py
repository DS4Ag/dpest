import dpest
from pathlib import Path
import pytest


def test_cul_template_generation(tmp_path):
    """Test generation of cultivar template files"""
    # Setup tests environment
    test_data_dir = Path(__file__).parent / "test_data"
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

    # Verify parameter extraction
    expected_params = {
        'parameters': {
            'P1D': '13.12',
            'P5': '331.4',
            'G1': '12.11',
            'G2': '63.48',
            'G3': '2.214',
            'PHI': '86.00'
        },
        'minima_parameters': {
            'P1D': '0',
            'P5': '100',
            'G1': '10',
            'G2': '10',
            'G3': '0.5',
            'PHI': '30'
        },
        'maxima_parameters': {
            'P1D': '200',
            'P5': '999',
            'G1': '50',
            'G2': '80',
            'G3': '8.0',
            'PHI': '150'
        },
        'parameters_grouped': {
            'P': 'P1D, P5',
            'G': 'G1, G2, G3',
            'PHINT': 'PHI'
        }
    }

    assert params == expected_params
    assert "ptf $" in tpl_path.read_text()  # Verify template format