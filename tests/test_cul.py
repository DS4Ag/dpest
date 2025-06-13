import dpest
from pathlib import Path

def test_cul(tmp_path):
    """Test generation of cultivar template files."""
    # Setup paths
    repo_root = Path(__file__).parent.parent
    cul_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.CUL"
    output_dir = tmp_path / "output"

    # Ensure the input file exists
    assert cul_file.exists(), f"Input file not found: {input_file}"

    # Create the output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Convert paths to strings
    cul_file = str(cul_file)
    output_dir = str(output_dir)

    # Call the dpest.wheat.ceres.cul function
    result = dpest.wheat.ceres.cul(
        P = 'P1D, P5',
        G = 'G1, G2, G3',
        PHINT = 'PHINT',
        cultivar = 'MANITOU',
        cul_file_path = cul_file,
        output_path = str(output_dir)
    )

    # 1. Validate result is not None
    assert result is not None, "Function returned None"

    # 2. Validate result is a tuple with length 2
    assert isinstance(result, tuple) and len(result) == 2, "Unexpected return value format"

    # 3. Unpack the result tuple
    params, tpl_path = result

    # 4. Convert tpl_path to a Path and check that the file exists on disk.
    tpl_path = Path(tpl_path)  # Convert str to Path for file checking
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


def test_cul_missing_arguments_file(capsys, tmp_path):
    """Test printed error when arguments.yml is missing."""
    # Temporarily rename arguments.yml if it exists
    repo_root = Path(__file__).parent.parent
    cul_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.CUL"
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    module_dir = Path(dpest.wheat.ceres.__file__).parent
    yml_path = module_dir / "arguments.yml"
    yml_backup = module_dir / "arguments.yml.bak"
    if yml_path.exists():
        yml_path.rename(yml_backup)
    try:
        result = dpest.wheat.ceres.cul(
            P='P1D, P5',
            G='G1, G2, G3',
            PHINT='PHINT',
            cultivar='MANITOU',
            cul_file_path=str(cul_file),
            output_path=str(output_dir)
        )
        captured = capsys.readouterr()
        assert "FileNotFoundError: YAML file not found:" in captured.out
        assert result is None
    finally:
        # Restore the yaml file if it was renamed
        if yml_backup.exists():
            yml_backup.rename(yml_path)

def test_cul_missing_cultivar(capsys, tmp_path):
    """Test printed error when cultivar is not provided."""
    repo_root = Path(__file__).parent.parent
    cul_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.CUL"
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    result = dpest.wheat.ceres.cul(
        P='P1D, P5',
        G='G1, G2, G3',
        PHINT='PHINT',
        cul_file_path=str(cul_file),
        output_path=str(output_dir)
        # cultivar is omitted!
    )
    captured = capsys.readouterr()
    assert "ValueError: The 'cultivar' argument is required and must be specified by the user." in captured.out
    assert result is None

def test_cul_invalid_cultivar(capsys, tmp_path):
    """Test printed error when cultivar does not exist in file."""
    repo_root = Path(__file__).parent.parent
    cul_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.CUL"
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    result = dpest.wheat.ceres.cul(
        P='P1D, P5',
        G='G1, G2, G3',
        PHINT='PHINT',
        cultivar='INVALID',
        cul_file_path=str(cul_file),
        output_path=str(output_dir)
    )
    captured = capsys.readouterr()
    assert "ValueError: The cultivar INVALID wasn't founded on file" in captured.out
    assert result is None

def test_cul_invalid_parameters(capsys, tmp_path):
    """Test printed error when parameter does not exist in header."""
    repo_root = Path(__file__).parent.parent
    cul_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.CUL"
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    result = dpest.wheat.ceres.cul(
        P='INVALID_PARAM',
        G='G1, G2, G3',
        PHINT='PHINT',
        cultivar='MANITOU',
        cul_file_path=str(cul_file),
        output_path=str(output_dir)
    )
    captured = capsys.readouterr()
    assert "ValueError: Parameter 'INVALID_PARAM' does not exist in the header line of" in captured.out
    assert result is None

def test_cul_default_new_template_file_extension(capsys, tmp_path):
    """Test that default new_template_file_extension is used when not provided."""
    repo_root = Path(__file__).parent.parent
    cul_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.CUL"
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Don't provide new_template_file_extension
    result = dpest.wheat.ceres.cul(
        P='P1D, P5',
        G='G1, G2, G3',
        PHINT='PHINT',
        cultivar='MANITOU',
        cul_file_path=str(cul_file),
        output_path=str(output_dir)
    )
    assert result is not None

def test_cul_default_header_start(capsys, tmp_path):
    """Test that default header_start is used when not provided."""
    repo_root = Path(__file__).parent.parent
    cul_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.CUL"
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Don't provide header_start
    result = dpest.wheat.ceres.cul(
        P='P1D, P5',
        G='G1, G2, G3',
        PHINT='PHINT',
        cultivar='MANITOU',
        cul_file_path=str(cul_file),
        output_path=str(output_dir),
        new_template_file_extension='.tpl'  # Provide something else to not hit previous test
    )
    assert result is not None

def test_cul_empty_parameters_grouped(tmp_path):
    """Test that empty parameters_grouped triggers YAML defaults."""
    repo_root = Path(__file__).parent.parent
    cul_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.CUL"
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Call WITHOUT any parameter group arguments (P=..., G=..., etc.)
    result = dpest.wheat.ceres.cul(
        cultivar='MANITOU',
        cul_file_path=str(cul_file),
        output_path=str(output_dir),
        new_template_file_extension='.tpl'
    )

    # Verify function completes successfully
    assert result is not None