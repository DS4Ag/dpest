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

    # Verify variable filtering (with suffix)
    expected_vars = {'Anthesis_DAP_TRT1', 'Maturity_DAP_TRT1'}
    assert expected_vars.issubset(df['variable_name'].values)


def test_overview_nonexistent_treatment(tmp_path, capsys):
    """Test with non-existent treatment"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    # Run the function
    dpest.wheat.overview(
        treatment='NON_EXISTENT_TREATMENT',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path)
    )

    # Capture printed output
    captured = capsys.readouterr()
    assert "No data found for treatment" in captured.out


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


def test_overview_missing_required_arguments():
    """Test missing required 'treatment' argument"""
    with pytest.raises(ValueError) as excinfo:
        dpest.wheat.overview(
            treatment=None,
            overview_file_path="dummy/path"
        )
    assert "The 'treatment' argument is required" in str(excinfo.value)


@pytest.mark.parametrize("invalid_suffix, error_msg", [
    (123, "Suffix must be a string"),
    ("bad!", "only contain letters and numbers"),
    ("LONGSUFFIX", "at most 4 characters")
])
def test_overview_invalid_suffix(tmp_path, invalid_suffix, error_msg):
    """Test invalid suffix values"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    with pytest.raises(ValueError) as excinfo:
        dpest.wheat.overview(
            treatment='164.0 KG N/HA IRRIG',
            overview_file_path=str(overview_file),
            output_path=str(tmp_path),
            suffix=invalid_suffix
        )
    assert error_msg in str(excinfo.value)


def test_overview_file_not_found(tmp_path):
    """Test non-existent input file handling"""
    with pytest.raises(FileNotFoundError):
        dpest.wheat.overview(
            treatment='164.0 KG N/HA IRRIG',
            overview_file_path="nonexistent/file.out",
            output_path=str(tmp_path)
        )


@pytest.mark.parametrize("mrk, smk, error_msg", [
    ('a', '!', "Primary marker validation failed"),
    ('!', '!', "Primary and secondary markers cannot match")
])
def test_overview_invalid_markers(tmp_path, mrk, smk, error_msg):
    """Test invalid marker configurations"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    with pytest.raises(ValueError) as excinfo:
        dpest.wheat.overview(
            treatment='164.0 KG N/HA IRRIG',
            overview_file_path=str(overview_file),
            output_path=str(tmp_path),
            mrk=mrk,
            smk=smk
        )
    assert error_msg in str(excinfo.value)


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
    expected_vars = {v.replace(' ', '')[:20] for v in test_vars}
    assert all(var in df['variable_name'].values for var in expected_vars)


def test_overview_nonexistent_treatment(tmp_path):
    """Test handling of non-existent treatment"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    with pytest.raises(ValueError) as excinfo:
        dpest.wheat.overview(
            treatment='NON_EXISTENT_TREATMENT',
            overview_file_path=str(overview_file),
            output_path=str(tmp_path)
        )
    assert "No data found for treatment" in str(excinfo.value)


def test_overview_full_parameters(tmp_path):
    """Test all optional parameters together"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    custom_vars = ['Anthesis (DAP)', 'Maturity (DAP)']
    custom_classification = {'Anthesis (DAP)': 'phenology', 'Maturity (DAP)': 'phenology'}

    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path),
        suffix='TEST',
        variables=custom_vars,
        variables_classification=custom_classification,
        overview_ins_first_line="pif #",
        mrk='@',
        smk='%'
    )

    df, ins_path = result

    # Verify DataFrame structure
    assert {'variable_name', 'value_measured', 'group'}.issubset(df.columns)
    assert len(df) == len(custom_vars)

    # Verify INS file content
    with open(ins_path, 'r') as f:
        content = f.read()
        assert content.startswith('pif #')
        assert all(f"!{v.replace(' ', '_')[:20]}_TEST!" in content for v in custom_vars)


def test_overview_empty_variables(tmp_path):
    """Test empty variables list handling"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    with pytest.raises(ValueError) as excinfo:
        dpest.wheat.overview(
            treatment='164.0 KG N/HA IRRIG',
            overview_file_path=str(overview_file),
            output_path=str(tmp_path),
            variables=[]
        )
    assert "At least one variable must be specified" in str(excinfo.value)


def test_overview_special_characters_in_treatment(tmp_path):
    """Test treatment names with special characters"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA (IRRIGATED)',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path)
    )

    df, ins_path = result
    assert not df.empty
    assert Path(ins_path).exists()


def test_overview_different_output_formats(tmp_path):
    """Test various output configurations"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    # Test with different marker combinations
    for mrk, smk in [('$', '&'), ('*', '?')]:
        result = dpest.wheat.overview(
            treatment='164.0 KG N/HA IRRIG',
            overview_file_path=str(overview_file),
            output_path=str(tmp_path),
            mrk=mrk,
            smk=smk
        )
        df, ins_path = result
        with open(ins_path, 'r') as f:
            content = f.read()
            assert f"pif {mrk}" in content