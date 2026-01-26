# tests/test_spe.py

from pathlib import Path
import dpest


def test_spe_tuple_syntax_whcer(tmp_path):
    """Successful template generation using tuple syntax (WHCER048.SPE example)."""
    repo_root = Path(__file__).parent.parent
    spe_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.SPE"
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    assert spe_file.exists(), f"Input file not found: {spe_file}"

    # Example 1 from the spe docstring
    species_parameters, species_tpl_path = dpest.spe(
        species_file_path=str(spe_file),
        PGERM=(15, 1, 0.0, 20.0, "Phase_dur"),
        P0=(15, 3, -5.0, 5.0, "Phase_dur"),
        Fac=(19, 1, 0.0, 2.0, "Phase_dur"),
        h=(19, 2, 10.0, 30.0, "Phase_dur"),
        GrStg=(19, 3, 0.0, 4.0, "Phase_dur"),
        LWLOS=(30, 3, 0.0, 6.0, "Phase_dur"),
        output_path=str(output_dir),
    )

    # Check return structure
    assert isinstance(species_parameters, dict)
    expected_keys = {
        "parameters",
        "minima_parameters",
        "maxima_parameters",
        "parameters_grouped",
    }
    assert expected_keys.issubset(
        species_parameters
    ), f"Missing expected keys: {expected_keys - set(species_parameters)}"

    # Check template file
    tpl_path = Path(species_tpl_path)
    assert tpl_path.exists(), f"Template file not created: {tpl_path}"
    with tpl_path.open("r") as f:
        first_line = f.readline().strip().lower()
    assert first_line.startswith(
        "ptf"
    ), f"Template file must start with 'ptf', got: {first_line}"


def test_spe_dict_syntax_sbgro(tmp_path):
    """Successful template generation using dict syntax (SBGRO048.SPE example)."""
    repo_root = Path(__file__).parent.parent
    spe_file = repo_root / "tests/DSSAT48/Genotype/SBGRO048.SPE"
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    assert spe_file.exists(), f"Input file not found: {spe_file}"

    # Example 2 from the spe docstring
    species_parameters, species_tpl_path = dpest.spe(
        species_file_path=str(spe_file),
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
        output_path=str(output_dir),
    )

    # Check return structure
    assert isinstance(species_parameters, dict)
    expected_keys = {
        "parameters",
        "minima_parameters",
        "maxima_parameters",
        "parameters_grouped",
    }
    assert expected_keys.issubset(
        species_parameters
    ), f"Missing expected keys: {expected_keys - set(species_parameters)}"

    # Check template file
    tpl_path = Path(species_tpl_path)
    assert tpl_path.exists(), f"Template file not created: {tpl_path}"
    with tpl_path.open("r") as f:
        first_line = f.readline().strip().lower()
    assert first_line.startswith(
        "ptf"
    ), f"Template file must start with 'ptf', got: {first_line}"


def test_spe_missing_species_file_path(capsys, tmp_path):
    """Missing species_file_path should print a ValueError and return None."""
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    result = dpest.spe(
        # species_file_path omitted on purpose
        output_path=str(output_dir),
        PGERM=(15, 1, 0.0, 20.0, "Phase_dur"),
    )

    captured = capsys.readouterr()
    assert (
        "ValueError: The 'species_file_path' argument is required and must be specified by the user."
        in captured.out
    )
    assert result is None
