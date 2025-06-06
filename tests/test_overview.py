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

    # Custom variables and classification
    test_vars = ['Anthesis (DAP)', 'Maturity (DAP)']
    test_classification = {'Anthesis (DAP)': 'phenology', 'Maturity (DAP)': 'phenology'}

    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path),
        suffix='TRT1',
        variables=test_vars,
        variables_classification=test_classification,
        overview_ins_first_line="pif #",
        mrk='@',
        smk='#'
    )

    df, ins_path = result
    # Verify custom parameters
    assert 'TRT1' in ins_path
    assert set(df['variable']) == set(test_vars)
    assert df['group'].unique().tolist() == ['phenology']


def test_overview_missing_required_arguments():
    """Test missing required arguments"""
    with pytest.raises(ValueError) as excinfo:
        dpest.wheat.overview(treatment=None, overview_file_path="dummy/path")
    assert "The 'treatment' argument is required" in str(excinfo.value)


def test_overview_invalid_suffix(tmp_path):
    """Test invalid suffix values"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    # Test non-string suffix
    with pytest.raises(ValueError) as excinfo:
        dpest.wheat.overview(
            treatment='TREATMENT',
            overview_file_path=str(overview_file),
            suffix=123
        )
    assert "Suffix must be a string" in str(excinfo.value)

    # Test invalid characters
    with pytest.raises(ValueError) as excinfo:
        dpest.wheat.overview(
            treatment='TREATMENT',
            overview_file_path=str(overview_file),
            suffix="bad$"
        )
    assert "only contain letters and numbers" in str(excinfo.value)

    # Test too long suffix
    with pytest.raises(ValueError) as excinfo:
        dpest.wheat.overview(
            treatment='TREATMENT',
            overview_file_path=str(overview_file),
            suffix="LONGSUFFIX"
        )
    assert "at most 4 characters" in str(excinfo.value)


def test_overview_file_not_found(tmp_path):
    """Test with non-existent input file"""
    with pytest.raises(FileNotFoundError):
        dpest.wheat.overview(
            treatment='TREATMENT',
            overview_file_path="nonexistent/file.out",
            output_path=str(tmp_path)
        )


def test_overview_variable_filtering(tmp_path):
    """Test filtering with specific variables"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    test_vars = ['Anthesis (DAP)', 'Product wt (kg dm/ha;no loss)']

    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path),
        variables=test_vars
    )

    df, _ = result
    assert set(df['variable']) == set(test_vars)


def test_overview_marker_validation(tmp_path):
    """Test invalid marker delimiters"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    # Test invalid mrk
    with pytest.raises(ValueError):
        dpest.wheat.overview(
            treatment='TREATMENT',
            overview_file_path=str(overview_file),
            mrk='a'  # Invalid character
        )

    # Test matching mrk/smk
    with pytest.raises(ValueError):
        dpest.wheat.overview(
            treatment='TREATMENT',
            overview_file_path=str(overview_file),
            mrk='!',
            smk='!'
        )


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

    # Verify DataFrame structure
    required_columns = {'variable_name', 'value_measured', 'group'}
    assert required_columns.issubset(df.columns)
    assert not df.empty

    # Verify INS file content
    with open(ins_path, 'r') as f:
        content = f.read()
        assert content.startswith('pif ~')
        assert '~164.0 KG N/HA IRRIG~' in content
        assert '!variable_name_TEST!' in content


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