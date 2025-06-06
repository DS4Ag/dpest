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
    assert 'TRT1' in ins_path
    assert {'Anthesis_DAP_TRT1', 'Maturity_DAP_TRT1'}.issubset(set(df['variable_name'].values))


@pytest.mark.parametrize("suffix_value, error_msg", [
    (123, "Suffix must be a string"),
    ("bad!", "only contain letters and numbers"),
    ("LONGSUFFIX", "at most 4 characters")
])
def test_overview_invalid_suffix(tmp_path, suffix_value, error_msg, capsys):
    """Test invalid suffix values"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path),
        suffix=suffix_value
    )
    captured = capsys.readouterr()
    assert error_msg in captured.out
    assert result is None


def test_overview_file_not_found(tmp_path, capsys):
    """Test non-existent input file handling"""
    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path="nonexistent/file.out",
        output_path=str(tmp_path)
    )
    captured = capsys.readouterr()
    assert "does not exist" in captured.out
    assert result is None


@pytest.mark.parametrize("mrk, smk, error_msg", [
    ('a', '!', "Primary marker validation failed"),
    ('!', '!', "Primary and secondary markers cannot match")
])
def test_overview_invalid_markers(tmp_path, mrk, smk, error_msg, capsys):
    """Test invalid marker configurations"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path),
        mrk=mrk,
        smk=smk
    )
    captured = capsys.readouterr()
    assert error_msg in captured.out
    assert result is None


def test_overview_nonexistent_treatment(tmp_path, capsys):
    """Test handling of non-existent treatment"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    result = dpest.wheat.overview(
        treatment='NON_EXISTENT_TREATMENT',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path)
    )
    captured = capsys.readouterr()
    assert "No data found for treatment" in captured.out
    assert result is None


def test_overview_empty_variables(tmp_path, capsys):
    """Test empty variables list handling"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"

    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path),
        variables=[]
    )
    captured = capsys.readouterr()
    assert "At least one variable must be specified" in captured.out
    assert result is None


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
    # Check for base variable names in formatted output
    assert any('Anthesis_DAP' in name for name in df['variable_name'].values)
    assert any('Productwtkgdmha' in name for name in df['variable_name'].values)


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
    assert {'variable_name', 'value_measured', 'group'}.issubset(df.columns)
    assert len(df) == len(custom_vars)

    with open(ins_path, 'r') as f:
        content = f.read()
        assert content.startswith('pif # @')
        assert '@Anthesis (DAP)@ %Anthesis_DAP_TEST%' in content
        assert '@Maturity (DAP)@ %Maturity_DAP_TEST%' in content


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