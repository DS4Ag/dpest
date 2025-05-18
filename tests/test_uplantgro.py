ef test_uplantgro(tmp_path, capsys):
    import shutil
    from pathlib import Path
    from dpest.wheat.utils import uplantgro

    # Locate repo root and test data file
    repo_root = Path(__file__).parent.parent
    original_file = repo_root / "tests/DSSAT48_data/Wheat/PlantGro.OUT"

    # Setup isolated temp directory
    test_dir = tmp_path / "dssat_test"
    test_dir.mkdir()
    test_file = test_dir / "PlantGro.OUT"
    shutil.copyfile(original_file, test_file)

    # Read original content
    original = test_file.read_text()

    # Run the function
    uplantgro(
        plantgro_file_path=str(test_file),
        treatment='164.0 KG N/HA IRRIG',
        variables=['LAID', 'CWAD', 'T#AD']
    )

    # Capture stdout and check message
    captured = capsys.readouterr()
    updated = test_file.read_text()

    if "No update required" in captured.out:
        assert original == updated, "File should not be modified when no update is required."
    else:
        assert original != updated, "File should be modified when an update is required."