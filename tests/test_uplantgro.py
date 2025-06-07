import dpest.wheat.utils as utils
import pytest
from pathlib import Path

import pytest
from pathlib import Path
import shutil
import dpest.wheat.utils as utils


def test_uplantgro_variable_validation(tmp_path, capsys):
    """Test validation of variables parameter"""
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48_data/Wheat/PlantGro.OUT"
    temp_file = tmp_path / "PlantGro.OUT"
    shutil.copy(plantgro_file, temp_file)

    # Test invalid variable types
    invalid_cases = [
        None,  # None
        123,  # Integer
        [123],  # List of non-strings
        [],  # Empty list
        ''  # Empty string
    ]

    for case in invalid_cases:
        with pytest.raises(ValueError) as excinfo:
            utils.uplantgro(
                plantgro_file_path=str(temp_file),
                treatment='164.0 KG N/HA IRRIG',
                variables=case
            )
        assert "non-empty string or a list of strings" in str(excinfo.value)


def test_uplantgro_header_space_validation(tmp_path, capsys):
    """Test validation of nspaces parameters"""
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48_data/Wheat/PlantGro.OUT"
    temp_file = tmp_path / "PlantGro.OUT"
    shutil.copy(plantgro_file, temp_file)

    # Test invalid space parameters
    invalid_cases = [
        ('invalid', 4, 6),  # Invalid year header
        (5, 'invalid', 6),  # Invalid doy header
        (5, 4, 'invalid')  # Invalid columns header
    ]

    for case in invalid_cases:
        with pytest.raises(ValueError) as excinfo:
            utils.uplantgro(
                plantgro_file_path=str(temp_file),
                treatment='164.0 KG N/HA IRRIG',
                variables=['LAID'],
                nspaces_year_header=case[0],
                nspaces_doy_header=case[1],
                nspaces_columns_header=case[2]
            )
        assert "must be an integer" in str(excinfo.value)


def test_uplantgro_row_addition(tmp_path, capsys):
    """Test successful row addition scenario"""
    repo_root = Path(__file__).parent.parent
    original_file = repo_root / "tests/DSSAT48_data/Wheat/PlantGro.OUT"
    temp_file = tmp_path / "PlantGro.OUT"
    shutil.copy(original_file, temp_file)

    # Get initial line count
    with open(temp_file, 'r') as f:
        initial_lines = len(f.readlines())

    # Run function
    utils.uplantgro(
        plantgro_file_path=str(temp_file),
        treatment='164.0 KG N/HA IRRIG',
        variables=['LAID', 'CWAD', 'T#AD']
    )

    # Get updated line count
    with open(temp_file, 'r') as f:
        new_lines = len(f.readlines())

    # Verify output messages
    captured = capsys.readouterr()
    output = captured.out

    if new_lines > initial_lines:
        assert "row added successfully" in output
    else:
        assert "No update required" in output


# def test_uplantgro_no_update_needed(tmp_path, capsys):
#     """Test scenario where no rows need to be added"""
#     # Create a test file that doesn't need updates
#     test_content = """\
# @YEAR DOY   DAS   LAID   CWAD   T#AD
#  2023 001     1    0.10    5.0     1
#  2023 002     2    0.15    7.5     1
# """
#     temp_file = tmp_path / "PlantGro.OUT"
#     with open(temp_file, 'w') as f:
#         f.write(test_content)
#
#     # Run function
#     utils.uplantgro(
#         plantgro_file_path=str(temp_file),
#         treatment='TestTreatment',
#         variables=['LAID']
#     )
#
#     # Verify output
#     captured = capsys.readouterr()
#     assert "No update required" in captured.out
#
#     # Verify file remains unchanged
#     with open(temp_file, 'r') as f:
#         assert f.read() == test_content

##############################

def test_uplantgro_runs():
    # Verify that the function runs without raising an error
    utils.uplantgro(
        './DSSAT48_data/Wheat/PlantGro.OUT',
        '164.0 KG N/HA IRRIG',
        ['LAID', 'CWAD', 'T#AD']
    )


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