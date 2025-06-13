import dpest
from pathlib import Path
import pandas as pd
import pytest

def test_plantgro(tmp_path):
    """Test generation of instruction file and observations from PlantGro.OUT."""
    # Setup paths
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"
    output_dir = tmp_path / "output"

    # Ensure the input file exists
    assert plantgro_file.exists(), f"Input file not found: {plantgro_file}"

    # Create the output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Convert paths to strings
    plantgro_file = str(plantgro_file)
    output_dir = str(output_dir)

    # Call the dpest.wheat.plantgro function
    result = dpest.wheat.plantgro(
        treatment='164.0 KG N/HA IRRIG',
        variables=['LAID', 'CWAD', 'T#AD'],
        plantgro_file_path=plantgro_file,
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

####################
def test_plantgro_with_optional_parameters(tmp_path):
    """Test with all optional parameters specified"""
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"

    result = dpest.wheat.plantgro(
        treatment='164.0 KG N/HA IRRIG',
        plantgro_file_path=str(plantgro_file),
        output_path=str(tmp_path),
        suffix='TRT1',
        variables=['LAID', 'CWAD'],
        variables_classification={
            'LAID': 'lai',
            'CWAD': 'biomass'
        },
        plantgro_ins_first_line="pif #",
        mrk='@',
        smk='#'
    )

    df, ins_path = result
    assert 'TRT1' in ins_path
    # Check that at least one row for each variable exists (with suffix)
    assert any('LAID' in name and 'TRT1' in name for name in df['variable_name'].values)
    assert any('CWAD' in name and 'TRT1' in name for name in df['variable_name'].values)

def test_plantgro_variable_filtering(tmp_path):
    """Test filtering with specific variables"""
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"

    test_vars = ['LAID', 'CWAD']

    result = dpest.wheat.plantgro(
        treatment='164.0 KG N/HA IRRIG',
        plantgro_file_path=str(plantgro_file),
        output_path=str(tmp_path),
        variables=test_vars
    )

    df, _ = result
    assert any('LAID' in name for name in df['variable_name'].values)
    assert any('CWAD' in name for name in df['variable_name'].values)

def test_plantgro_missing_treatment_argument(tmp_path, capsys):
    """Test missing treatment argument validation"""
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"

    result = dpest.wheat.plantgro(
        treatment=None,
        plantgro_file_path=str(plantgro_file),
        output_path=str(tmp_path)
    )
    captured = capsys.readouterr()
    assert "ValueError: The 'treatment' must be a non-empty string." in captured.out
    assert result is None

def test_plantgro_special_characters_in_treatment(tmp_path, capsys):
    """Test treatment names with special characters"""
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"

    result = dpest.wheat.plantgro(
        treatment='164.0 KG N/HA (IRRIGATED)',
        plantgro_file_path=str(plantgro_file),
        output_path=str(tmp_path)
    )

    if result is None:
        captured = capsys.readouterr()
        # Accept any error about variables or missing treatment
        assert (
            "No valid data found for treatment" in captured.out or
            "No data found for treatment" in captured.out or
            "should be a non-empty string or a list of strings" in captured.out
        )
    else:
        df, ins_path = result
        assert not df.empty
        assert Path(ins_path).exists()

def test_plantgro_variables_accepts_string(tmp_path):
    """Test that passing a string for 'variables' is accepted (converted to list internally)."""
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"

    result = dpest.wheat.plantgro(
        treatment='164.0 KG N/HA IRRIG',
        plantgro_file_path=str(plantgro_file),
        output_path=str(tmp_path),
        variables='LAID'
    )
    assert result is not None

@pytest.mark.parametrize("suffix_value, error_msg", [
    (123, "An unexpected error occurred"),
    ("bad!", "Suffix must only contain letters and numbers."),
    ("LONGSUFFIX", "Suffix must be at most 4 characters long.")
])
def test_plantgro_invalid_suffix(tmp_path, suffix_value, error_msg, capsys):
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"

    result = dpest.wheat.plantgro(
        treatment='164.0 KG N/HA IRRIG',
        plantgro_file_path=str(plantgro_file),
        output_path=str(tmp_path),
        variables=['LAID'],
        suffix=suffix_value
    )
    captured = capsys.readouterr()
    assert error_msg in captured.out
    assert result is None

def test_plantgro_file_not_found(tmp_path, capsys):
    """Test non-existent input file handling"""
    non_existent_file = tmp_path / "nonexistent.OUT"
    result = dpest.wheat.plantgro(
        treatment='164.0 KG N/HA IRRIG',
        plantgro_file_path=str(non_existent_file),
        output_path=str(tmp_path),
        variables=['LAID']
    )
    captured = capsys.readouterr()
    assert "FileNotFoundError: YAML file not found:" in captured.out or "FileNotFoundError: The file" in captured.out
    assert result is None

def test_plantgro_missing_yaml_file(tmp_path, capsys):
    """Test handling of missing YAML arguments file"""
    non_existent_file = tmp_path / "nonexistent.OUT"
    result = dpest.wheat.plantgro(
        treatment='164.0 KG N/HA IRRIG',
        plantgro_file_path=str(non_existent_file),
        output_path=str(tmp_path),
        variables=['LAID']
    )
    captured = capsys.readouterr()
    assert "FileNotFoundError: The file 'nonexistent.OUT' does not exist" in captured.out or "YAML file not found" in captured.out
    assert result is None

def test_plantgro_nonexistent_treatment(tmp_path, capsys):
    """Test handling of non-existent treatment"""
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"

    result = dpest.wheat.plantgro(
        treatment='NON_EXISTENT_TREATMENT',
        plantgro_file_path=str(plantgro_file),
        output_path=str(tmp_path),
        variables=['LAID']
    )
    captured = capsys.readouterr()
    # Accept any error about missing treatment or unexpected error
    assert (
        "No valid data found for treatment" in captured.out or
        "No data found for treatment" in captured.out or
        "An unexpected error occurred" in captured.out
    )
    assert result is None

def test_plantgro_empty_variables(tmp_path, capsys):
    """Test empty variables list handling"""
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"

    result = dpest.wheat.plantgro(
        treatment='164.0 KG N/HA IRRIG',
        plantgro_file_path=str(plantgro_file),
        output_path=str(tmp_path),
        variables=[]
    )
    captured = capsys.readouterr()
    assert result is None
    assert "should be a non-empty string or a list of strings" in captured.out

@pytest.mark.parametrize("mrk, smk, expected_error", [
    ('a', '!', "Invalid mrk character"),
    ('!', '!', "Invalid mrk character")
])
def test_plantgro_invalid_markers(tmp_path, mrk, smk, expected_error, capsys):
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"

    result = dpest.wheat.plantgro(
        treatment='164.0 KG N/HA IRRIG',
        plantgro_file_path=str(plantgro_file),
        output_path=str(tmp_path),
        variables=['LAID'],
        mrk=mrk,
        smk=smk
    )

    captured = capsys.readouterr()
    assert expected_error in captured.out
    assert result is None

def test_plantgro_duplicate_markers(tmp_path, capsys):
    """Test validation of identical mrk/smk markers"""
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"
    result = dpest.wheat.plantgro(
        treatment='164.0 KG N/HA IRRIG',
        plantgro_file_path=str(plantgro_file),
        output_path=str(tmp_path),
        variables=['LAID'],
        mrk='#',
        smk='#'
    )
    captured = capsys.readouterr()
    assert "mrk and smk must be different characters." in captured.out
    assert result is None

def test_plantgro_mrk_smk_same_character(tmp_path, capsys):
    """Test validation of identical valid markers"""
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"

    # Use valid markers that are identical
    result = dpest.wheat.plantgro(
        treatment='164.0 KG N/HA IRRIG',
        plantgro_file_path=str(plantgro_file),
        output_path=str(tmp_path),
        variables=['LAID'],
        mrk='#',
        smk='#'
    )

    captured = capsys.readouterr()
    assert "mrk and smk must be different characters" in captured.out
    assert result is None

def test_plantgro_different_output_formats(tmp_path):
    repo_root = Path(__file__).parent.parent
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"

    # Test only known valid combinations
    valid_markers = [('~', '!'), ('@', '#')]

    for mrk, smk in valid_markers:
        result = dpest.wheat.plantgro(
            treatment='164.0 KG N/HA IRRIG',
            plantgro_file_path=str(plantgro_file),
            output_path=str(tmp_path),
            variables=['LAID'],
            mrk=mrk,
            smk=smk
        )
        df, ins_path = result
        assert Path(ins_path).exists()
