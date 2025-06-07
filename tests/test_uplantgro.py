import dpest.wheat.utils as utils
import pytest
from pathlib import Path

def test_uplantgro_runs():
    # Just verify that the function runs without raising an error
    utils.uplantgro(
        './DSSAT48_data/Wheat/PlantGro.OUT',
        '164.0 KG N/HA IRRIG',
        ['LAID', 'CWAD', 'T#AD']
    )

#############

@pytest.mark.parametrize("treatment_input,expected_error", [
    (None, "The 'treatment' must be a non-empty string"),
    ("", "The 'treatment' must be a non-empty string"),
    (123, "The 'treatment' must be a non-empty string"),
    (["list_instead_of_str"], "The 'treatment' must be a non-empty string")
])
def test_uplantgro_treatment_validation(treatment_input, expected_error, capsys):
    """Test validation of treatment parameter in uplantgro()"""
    # Setup valid file path
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48_data/Wheat/PlantGro.OUT"

    # Ensure test file exists
    assert plantgro_file.exists(), f"Required test file missing: {plantgro_file}"

    # Call function with parameter under test
    utils.uplantgro(
        plantgro_file_path=str(plantgro_file),
        treatment=treatment_input,
        variables=['LAID']  # Valid variables to avoid unrelated errors
    )

    # Verify error handling
    captured = capsys.readouterr()
    assert expected_error in captured.out