import dpest
from pathlib import Path
import pandas as pd

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