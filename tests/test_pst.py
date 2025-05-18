import dpest
from pathlib import Path

def test_pst(tmp_path):
    """Test creation of a PEST control file (.PST) with all required inputs."""

    # Define test file paths
    repo_root = Path(__file__).parent.parent
    cul_file = repo_root / "tests/DSSAT48_data/Genotype/WHCER048.CUL"
    eco_file = repo_root / "tests/DSSAT48_data/Genotype/WHCER048.ECO"
    overview_file = repo_root / "tests/DSSAT48_data/Wheat/OVERVIEW.OUT"
    plantgro_file = repo_root / "tests/DSSAT48_data/Wheat/PlantGro.OUT"

    # Ensure all required files exist
    assert cul_file.exists(), f"Missing: {cul_file}"
    assert eco_file.exists(), f"Missing: {eco_file}"
    assert overview_file.exists(), f"Missing: {overview_file}"
    assert plantgro_file.exists(), f"Missing: {plantgro_file}"

    # Create the output directory
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Convert paths to strings
    cul_file = str(cul_file)
    eco_file = str(eco_file)
    overview_file = str(overview_file)
    plantgro_file = str(plantgro_file)
    output_dir_str = str(output_dir)

    # Step 1: Generate parameter dicts using cul/eco functions
    cultivar_parameters, cul_tpl_path = dpest.wheat.ceres.cul(
        P='P1D, P5',
        G='G1, G2, G3',
        PHINT='PHINT',
        cultivar='MANITOU',
        cul_file_path=cul_file,
        output_path=output_dir_str
    )

    ecotype_parameters, eco_tpl_path = dpest.wheat.ceres.eco(
        PHEN='P1, P2FR1',
        VERN='VEFF',
        ecotype='CAWH01',
        eco_file_path=eco_file,
        output_path=output_dir_str
    )

    # Step 2: Generate observations using overview and plantgro
    overview_obs, overview_ins_path = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=overview_file,
        output_path=output_dir_str
    )

    plantgro_obs, plantgro_ins_path = dpest.wheat.plantgro(
        treatment='164.0 KG N/HA IRRIG',
        variables=['LAID', 'CWAD', 'T#AD'],
        plantgro_file_path=plantgro_file,
        output_path=output_dir_str
    )

    # Step 3: Define model command and file pairs
    model_command = r'py "C:\pest18\run_dssat.py"'
    input_output_pairs = [
        (str(cul_tpl_path), cul_file),
        (str(eco_tpl_path), eco_file),
        (str(overview_ins_path), overview_file),
        (str(plantgro_ins_path), plantgro_file)
    ]

    # Step 4: Create .PST file
    dpest.pst(
        cultivar_parameters=cultivar_parameters,
        ecotype_parameters=ecotype_parameters,
        dataframe_observations=[overview_obs, plantgro_obs],
        model_comand_line=model_command,
        input_output_file_pairs=input_output_pairs,
        output_path=output_dir_str,
        pst_filename="PEST_CONTROL.pst"
    )

    # Step 5: Validate .pst file creation
    pst_file = output_dir / "PEST_CONTROL.pst"
    assert pst_file.exists(), "PEST control file was not created."

    # Step 6: Confirm first line and key content
    with open(pst_file, 'r') as file:
        lines = file.readlines()
        assert lines[0].strip().lower().startswith("pcf"), "PEST file must start with 'pcf'"
        content = ''.join(lines).lower()
        required_sections = [
            '* control data',
            '* lsqr',
            '* parameter groups',
            '* parameter data',
            '* observation groups',
            '* observation data',
            '* model command line',
            '* model input/output'
        ]
        for section in required_sections:
            assert section in content, f"Missing section: {section}"