def test_uplantgro(tmp_path):
    import shutil
    from dpest.wheat.utils import uplantgro

    # Setup test environment
    test_dir = tmp_path / "dssat_test"
    test_dir.mkdir()
    original_file = Path('./tests/data/PlantGro_sample.OUT')
    test_file = test_dir / "PlantGro.OUT"
    shutil.copyfile(original_file, test_file)

    # Read original content
    original = test_file.read_text()

    # Run function and capture result message
    result = uplantgro(
        plantgro_file=str(test_file),
        trno='164.0 KG N/HA IRRIG',
        variables=['LAID', 'CWAD', 'T#AD']
    )

    # Read updated content
    updated = test_file.read_text()

    # Assert based on result message
    if "No update required" in result:
        assert original == updated, "File should not be modified when no update is required."
    else:
        assert original != updated, "File should be modified when an update is required."