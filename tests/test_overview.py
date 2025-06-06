import dpest
from pathlib import Path
import pandas as pd
import os
import pytest

def test_overview(tmp_path):
    """Test generation of instruction file and observations from OVERVIEW.OUT."""
    # Setup paths
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"
    output_dir = tmp_path / "output"

    # Ensure the input file exists
    assert overview_file.exists(), f"Input file not found: {overview_filee}"

    # Create the output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Convert paths to strings
    overview_file = str(overview_file)
    output_dir = str(output_dir)

    # Call the dpest.wheat.overview function
    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=overview_file,
        output_path=str(output_dir)
    )

    # 1. Validate result is not None
    assert result is not None, "Function returned None"

    # 2. Validate result is a tuple with length 2
    assert isinstance(result, tuple) and len(result) == 2, "Unexpected return value format"

    # 3. Unpack the result tuple
    df, ins_path = result

    # 4. Check the INS file path and confirm it was created
    ins_path = Path(ins_path)
    assert ins_path.exists(), f"Instruction file not created: {ins_path}"

    # 5. Confirm the first line of the instruction file starts with 'ptf'
    with open(ins_path, 'r') as file:
        first_line = file.readline().strip().lower()
        assert first_line.startswith('pif'), f"Instruction file must start with 'ptf', but got: {first_line}"

    # 6. Confirm that the first element is a pandas DataFrame
    assert isinstance(df, pd.DataFrame), "Expected first return value to be a pandas DataFrame"

    # 7. Check that the DataFrame has the expected columns
    expected_columns = {'variable_name', 'value_measured', 'group'}
    assert expected_columns.issubset(df.columns), f"Missing expected columns in DataFrame: {expected_columns - set(df.columns)}"


def test_overview_with_optional_parameters(tmp_path):
    """Test with all optional parameters specified"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path),
        suffix='TRT1',
        variables=['Anthesis (DAP)', 'Maturity (DAP)'],
        variables_classification={
            'Anthesis (DAP)': 'phenology',
            'Maturity (DAP)': 'phenology'
        },
        overview_ins_first_line="pif #",
        mrk='@',
        smk='#'
    )

    df, ins_path = result
    # Verify suffix in filename
    assert 'TRT1' in ins_path

    # Verify variable filtering
    expected_vars = {'Anthesis_DAP', 'Maturity_DAP'}
    assert expected_vars.issubset(df['variable_name'].values)


def test_overview_nonexistent_treatment(tmp_path):
    """Test with non-existent treatment"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    with pytest.raises(ValueError) as excinfo:
        dpest.wheat.overview(
            treatment='NON_EXISTENT_TREATMENT',
            overview_file_path=str(overview_file),
            output_path=str(tmp_path)
        )
    assert "No data found for treatment" in str(excinfo.value)


def test_overview_output_structure(tmp_path):
    """Detailed output structure validation"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path),
        suffix='TEST'
    )

    df, ins_path = result

    # Verify INS file content
    with open(ins_path, 'r') as f:
        content = f.read()
        # Check for truncated variable names with suffix
        assert any('_TEST!' in line for line in content.split('\n'))