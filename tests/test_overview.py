import dpest
from pathlib import Path
import pandas as pd
import pytest

def test_overview(tmp_path):
    """Test generation of instruction file and observations from OVERVIEW.OUT."""
    # Setup paths
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"
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
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"

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

def test_overview_variable_filtering(tmp_path):
    """Test filtering with specific variables"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"

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
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"

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


def test_overview_missing_treatment_argument(tmp_path, capsys):
    """Test missing treatment argument validation"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"

    result = dpest.wheat.overview(
        treatment=None,
        overview_file_path=str(overview_file),
        output_path=str(tmp_path)
    )
    captured = capsys.readouterr()
    assert "ValueError: The 'treatment' argument is required and must be specified by the user." in captured.out
    assert result is None


def test_overview_special_characters_in_treatment(tmp_path, capsys):
    """Test treatment names with special characters"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"

    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA (IRRIGATED)',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path)
    )

    if result is None:
        captured = capsys.readouterr()
        assert "No data found for treatment" in captured.out
    else:
        df, ins_path = result
        assert not df.empty
        assert Path(ins_path).exists()


def test_overview_variables_accepts_string(tmp_path):
    """Test that passing a string for 'variables' is accepted (converted to list internally)."""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"

    # Just call the function with a string for variables; it should not raise an error
    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path),
        variables='Anthesis (DAP)'
    )
    assert result is not None  # The function should run and return a result


@pytest.mark.parametrize("suffix_value, error_msg", [
    (123, "Suffix must be a string"),
    ("bad!", "only contain letters and numbers"),
    ("LONGSUFFIX", "at most 4 characters")
])
def test_overview_invalid_suffix(tmp_path, suffix_value, error_msg, capsys):
    """Test invalid suffix values"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"

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


def test_overview_missing_yaml_file(tmp_path, capsys):
    """Test handling of missing YAML arguments file"""
    # Simulate missing OVERVIEW.OUT file (which triggers the file not found branch)
    non_existent_file = tmp_path / "nonexistent.OUT"
    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(non_existent_file),
        output_path=str(tmp_path)
    )
    captured = capsys.readouterr()
    assert "FileNotFoundError: The file 'nonexistent.OUT' does not exist" in captured.out
    assert result is None


def test_overview_nonexistent_treatment(tmp_path, capsys):
    """Test handling of non-existent treatment"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"

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
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"

    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path),
        variables=[]
    )

    captured = capsys.readouterr()
    assert result is None
    assert "non-empty string or a list of strings" in captured.out


@pytest.mark.parametrize("mrk, smk, expected_error", [
    ('a', '!', "Invalid mrk character"),
    ('!', '!', "Invalid mrk character")  # Both markers being '!' is invalid
])
def test_overview_invalid_markers(tmp_path, mrk, smk, expected_error, capsys):
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"

    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path),
        mrk=mrk,
        smk=smk
    )

    captured = capsys.readouterr()
    assert expected_error in captured.out
    assert result is None


def test_overview_duplicate_markers(tmp_path, capsys):
    """Test validation of identical mrk/smk markers"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"
    # '!' is not allowed as mrk, so this triggers the invalid mrk check before "must be different"
    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path),
        mrk='!',
        smk='!'
    )
    captured = capsys.readouterr()
    assert "Invalid mrk character. It must not be one of A-Z, a-z, 0-9, !, [, ], (, ), :, space, tab, or &." in captured.out
    assert result is None


def test_overview_mrk_smk_same_character(tmp_path, capsys):
    """Test validation of identical valid markers"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"

    # Use valid markers that are identical
    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path),
        mrk='#',
        smk='#'
    )

    captured = capsys.readouterr()
    assert "mrk and smk must be different characters" in captured.out
    assert result is None


def test_overview_different_output_formats(tmp_path):
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"

    # Test only known valid combinations
    valid_markers = [('~', '!'), ('@', '#')]

    for mrk, smk in valid_markers:
        result = dpest.wheat.overview(
            treatment='164.0 KG N/HA IRRIG',
            overview_file_path=str(overview_file),
            output_path=str(tmp_path),
            mrk=mrk,
            smk=smk
        )
        df, ins_path = result
        assert Path(ins_path).exists()


def test_overview_unexpected_error(tmp_path, capsys, monkeypatch):
    """Test handling of unexpected exceptions"""
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"
    # Monkeypatch os.path.isfile to simulate missing YAML file
    import os
    original_isfile = os.path.isfile
    def fake_isfile(path):
        if "arguments.yml" in str(path):
            return False
        return original_isfile(path)
    monkeypatch.setattr(os.path, "isfile", fake_isfile)
    result = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path)
    )
    captured = capsys.readouterr()
    assert "FileNotFoundError: YAML file not found:" in captured.out
    assert result is None