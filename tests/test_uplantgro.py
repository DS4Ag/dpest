import dpest
import pytest
from pathlib import Path


def test_uplantgro_success(capsys):
    plantgro_path = Path('tests/DSSAT48/Wheat/PlantGro.OUT').resolve()

    result = dpest.wheat.utils.uplantgro(
        str(plantgro_path),
        '164.0 KG N/HA IRRIG',
        ['LAID', 'CWAD', 'T#AD']
    )

    captured = capsys.readouterr()

    assert result is None
    # Match EXACT output patterns from the function
    assert ("rows added successfully" in captured.out) or \
           ("row added successfully" in captured.out) or \
           ("PlantGro.OUT status: No update required." in captured.out)


def test_invalid_treatment_type(capsys):
    plantgro_path = Path('tests/DSSAT48/Wheat/PlantGro.OUT').resolve()
    result = dpest.wheat.utils.uplantgro(str(plantgro_path), 123, ['LAID'])
    captured = capsys.readouterr()
    assert "ValueError: The 'treatment' must be a non-empty string." in captured.out
    assert result is None


def test_invalid_variables_type(capsys):
    plantgro_path = Path('tests/DSSAT48/Wheat/PlantGro.OUT').resolve()
    result = dpest.wheat.utils.uplantgro(str(plantgro_path), 'Valid Treatment', None)
    captured = capsys.readouterr()
    assert "ValueError: The 'variables' should be a non-empty string or a list of strings." in captured.out
    assert result is None


def test_invalid_nspaces_parameters(capsys):
    plantgro_path = Path('tests/DSSAT48/Wheat/PlantGro.OUT').resolve()

    # Test all numeric parameters in one function
    for param in ['nspaces_year_header', 'nspaces_doy_header', 'nspaces_columns_header']:
        result = dpest.wheat.utils.uplantgro(
            str(plantgro_path),
            'Valid Treatment',
            ['LAID'],
            **{param: 'invalid'}
        )
        captured = capsys.readouterr()
        assert f"{param} must be an integer." in captured.out
        assert result is None


def test_file_not_found(capsys):
    non_existent_path = Path('tests/DSSAT48/Wheat/NonExistentFile.OUT')
    result = dpest.wheat.utils.uplantgro(str(non_existent_path), 'Valid Treatment', ['LAID'])
    captured = capsys.readouterr()
    assert "FileNotFoundError: The file 'NonExistentFile.OUT' does not exist" in captured.out
    assert result is None