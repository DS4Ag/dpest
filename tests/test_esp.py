import dpest
from pathlib import Path


def test_spe(tmp_path):
    """Test generation of species template files."""
    # Setup paths
    repo_root = Path(__file__).parent.parent
    spe_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.SPE"
    output_dir = tmp_path / "output"

    # Ensure the input file exists
    assert spe_file.exists(), f"Input file not found: {spe_file}"

    # Create the output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Call the dpest.spe function (tuple syntax example)
    result = dpest.spe(
        species_file_path=str(spe_file),
        output_path=str(output_dir),
        PGERM=(15, 1, 0.0, 20.0, "Phase_dur"),
        P0=(15, 3, -5.0, 5.0, "Phase_dur"),
        Fac=(19, 1, 0.0, 2.0, "Phase_dur"),
        h=(19, 2, 10.0, 30.0, "Phase_dur"),
        GrStg=(19, 3, 0.0, 4.0, "Phase_dur"),
        LWLOS=(30, 3, 0.0, 6.0, "Phase_dur"),
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

    # 5. Confirm the first line of the template file starts with 'ptf'
    with tpl_path.open("r") as f:
        first_line = f.readline().strip().lower()
        assert first_line.startswith("ptf"), f"Template file must start with 'ptf', but got: {first_line}"

    # 6. Check that `params` is a dictionary
    assert isinstance(params, dict), "Expected `params` to be a dictionary"

    # 7. Check that the dictionary has the expected nested keys
    expected_keys = {"parameters", "minima_parameters", "maxima_parameters", "parameters_grouped"}
    assert expected_keys.issubset(params), f"Missing expected keys in params: {expected_keys - set(params)}"


def test_spe_dict_syntax(tmp_path):
    """Test spe using the dictionary syntax for parameter specification."""
    repo_root = Path(__file__).parent.parent
    spe_file = repo_root / "tests/DSSAT48/Genotype/SBGRO048.SPE"
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # If the soybean species file is not present in tests, skip this test gracefully
    if not spe_file.exists():
        # pytest-style skip without importing pytest at top-level if you prefer:
        import pytest

        pytest.skip(f"Soybean species test file not found: {spe_file}")

    result = dpest.spe(
        species_file_path=str(spe_file),
        output_path=str(output_dir),
        PARMAX={
            "line": 5,
            "column": 1,
            "min": 20.0,
            "max": 60.0,
            "group": "PHOTOSYN",
        },
        PHTMAX={
            "line": 5,
            "column": 2,
            "min": 40.0,
            "max": 80.0,
            "group": "PHOTOSYN",
        },
        XLMAXT_2={
            "line": 11,
            "column": 2,
            "min": 0.0,
            "max": 20.0,
            "group": "TEMP_RESP",
        },
        XPGSLW_3={
            "line": 18,
            "column": 3,
            "min": 0.0,
            "max": 0.01,
            "group": "SLW_SHAPE",
        },
        RTDEPI={
            "line": 40,
            "column": 1,
            "min": 10.0,
            "max": 40.0,
            "group": "ROOTS",
        },
    )

    assert result is not None
    params, tpl_path = result
    tpl_path = Path(tpl_path)
    assert tpl_path.exists(), f"Template file not created: {tpl_path}"
    assert isinstance(params, dict)
    expected_keys = {"parameters", "minima_parameters", "maxima_parameters", "parameters_grouped"}
    assert expected_keys.issubset(params)


def test_spe_missing_arguments_file(capsys, tmp_path):
    """Test printed error when arguments.yml is missing."""
    repo_root = Path(__file__).parent.parent
    spe_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.SPE"
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Locate the module directory where arguments.yml should reside
    # Adjust this path if your spe function lives in a submodule
    import dpest as _dpest

    module_dir = Path(_dpest.__file__).parent  # or Path(_dpest.wheat.ceres.__file__).parent for wheat-only layout
    yml_path = module_dir / "arguments.yml"
    yml_backup = module_dir / "arguments.yml.bak"

    if yml_path.exists():
        yml_path.rename(yml_backup)

    try:
        result = dpest.spe(
            species_file_path=str(spe_file),
            output_path=str(output_dir),
            PGERM=(15, 1, 0.0, 20.0, "Phase_dur"),
        )
        captured = capsys.readouterr()
        assert "FileNotFoundError: YAML file not found:" in captured.out
        assert result is None
    finally:
        if yml_backup.exists():
            yml_backup.rename(yml_path)


def test_spe_missing_species_file_path(capsys, tmp_path):
    """Test printed error when species_file_path is not provided."""
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    result = dpest.spe(
        output_path=str(output_dir),
        PGERM=(15, 1, 0.0, 20.0, "Phase_dur"),
    )
    captured = capsys.readouterr()
    assert "ValueError: The 'species_file_path' argument is required and must be specified by the user." in captured.out
    assert result is None


def test_spe_invalid_line_column(capsys, tmp_path):
    """Test printed error when line/column indices are out of range or non-integer."""
    repo_root = Path(__file__).parent.parent
    spe_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.SPE"
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Use an obviously invalid line index
    result = dpest.spe(
        species_file_path=str(spe_file),
        output_path=str(output_dir),
        PGERM=(10_000, 1, 0.0, 20.0, "Phase_dur"),
    )
    captured = capsys.readouterr()
    assert "ValueError: Line index" in captured.out or "out of range" in captured.out
    assert result is None


def test_spe_default_marker_and_extension(tmp_path):
    """Test that defaults for mrk, tpl_first_line and new_template_file_extension are applied."""
    repo_root = Path(__file__).parent.parent
    spe_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.SPE"
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Do not provide mrk, tpl_first_line, or new_template_file_extension
    result = dpest.spe(
        species_file_path=str(spe_file),
        output_path=str(output_dir),
        PGERM=(15, 1, 0.0, 20.0, "Phase_dur"),
    )
    assert result is not None
    _, tpl_path = result
    tpl_path = Path(tpl_path)
    assert tpl_path.exists()
    assert tpl_path.suffix.lower() in {".tpl", ".TPL".lower()}
