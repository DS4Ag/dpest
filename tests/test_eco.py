import dpest
from pathlib import Path

def test_eco(tmp_path):
    """Test generation of ecotype template files."""
    # Setup paths
    repo_root = Path(__file__).parent.parent
    eco_file = repo_root / "tests/DSSAT48_data/Genotype/WHCER048.ECO"
    output_dir = tmp_path / "output"

    # Ensure the input file exists
    assert eco_file.exists(), f"Input file not found: {eco_file}"

    # Create the output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Convert paths to strings
    eco_file = str(eco_file)
    output_dir = str(output_dir)

    # Call the dpest.wheat.ceres.eco function
    result = dpest.wheat.ceres.eco(
        PHEN='P1, P2FR1',
        VERN='VEFF',
        ecotype='CAWH01',
        eco_file_path=eco_file,
        output_path=output_dir
    )

    # 1. Validate result is not None
    assert result is not None, "Function returned None"

    # 2. Validate result is a tuple with length 2
    assert isinstance(result, tuple) and len(result) == 2, "Unexpected return value format"

    # 3. Unpack the result tuple
    params, tpl_path = result

    # 4. Convert tpl_path to a Path and check that the file exists on disk.
    tpl_path = Path(tpl_path)
    assert tpl_path.exists(), f"Template file not created: {tpl_path}"

    # 5. Confirm the first line of the instruction file starts with 'ptf'
    with open(tpl_path, 'r') as file:
        first_line = file.readline().strip().lower()
        assert first_line.startswith('ptf'), f"Instruction file must start with 'ptf', but got: {first_line}"

    # 6. Check that `params` is a dictionary
    assert isinstance(params, dict), "Expected `params` to be a dictionary"

    # 7. Check that the dictionary has the expected nested keys
    expected_keys = {'parameters', 'minima_parameters', 'maxima_parameters', 'parameters_grouped'}
    assert expected_keys.issubset(params), f"Missing expected keys in params: {expected_keys - set(params)}"

