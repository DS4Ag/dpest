import pandas as pd
import dpest
from pathlib import Path
import pytest

def test_pst(tmp_path):
    """Test creation of a PEST control file (.PST) with all required inputs."""

    # Define test file paths
    repo_root = Path(__file__).parent.parent
    cul_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.CUL"
    eco_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.ECO"
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"

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


def test_pst_missing_both_parameters(tmp_path, capsys):
    """Test error when both cultivar and ecotype parameters are missing"""
    # Setup valid observations and files
    repo_root = Path(__file__).parent.parent
    overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"
    plantgro_file = repo_root / "tests/DSSAT48/Wheat/PlantGro.OUT"

    overview_obs, _ = dpest.wheat.overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path=str(overview_file),
        output_path=str(tmp_path)
    )

    input_output_pairs = [
        (str(tmp_path / "dummy.ins"), str(plantgro_file))
    ]

    # Call pst without any parameters
    dpest.pst(
        cultivar_parameters=None,
        ecotype_parameters=None,
        dataframe_observations=[overview_obs],
        model_comand_line='dummy_command',
        input_output_file_pairs=input_output_pairs,
        output_path=str(tmp_path)
    )

    captured = capsys.readouterr()
    assert "At least one of `cultivar_parameters` or `ecotype_parameters`" in captured.out
    assert not (tmp_path / "PEST_CONTROL.pst").exists()


def test_pst_invalid_cultivar_type(tmp_path, capsys):
    """Test invalid cultivar_parameters type"""
    # Use valid ecotype parameters
    repo_root = Path(__file__).parent.parent
    eco_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.ECO"
    ecotype_params, _ = dpest.wheat.ceres.eco(
        PHEN='P1, P2FR1',  # Valid parameters from existing test
        VERN='VEFF',
        ecotype='CAWH01',  # Valid existing ecotype
        eco_file_path=str(eco_file),
        output_path=str(tmp_path)
    )

    dpest.pst(
        cultivar_parameters="invalid_string",  # Invalid type
        ecotype_parameters=ecotype_params,
        dataframe_observations=[pd.DataFrame()],
        model_comand_line='dummy',
        input_output_file_pairs=[('dummy.tpl', str(eco_file))],
        output_path=str(tmp_path)
    )

    captured = capsys.readouterr()
    assert "must be a dictionary" in captured.out
    assert not (tmp_path / "PEST_CONTROL.pst").exists()


def test_pst_missing_cul_extension(tmp_path, capsys):
    """Test missing .CUL file when using cultivar params"""
    # Get valid cultivar params
    repo_root = Path(__file__).parent.parent
    cul_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.CUL"
    cultivar_params, _ = dpest.wheat.ceres.cul(
        P='P1D, P5',  # From working test
        G='G1, G2, G3',
        PHINT='PHINT',
        cultivar='MANITOU',  # Valid existing cultivar
        cul_file_path=str(cul_file),
        output_path=str(tmp_path)
    )

    # Invalid pairs without .CUL
    dpest.pst(
        cultivar_parameters=cultivar_params,
        dataframe_observations=[pd.DataFrame()],
        model_comand_line='dummy',
        input_output_file_pairs=[('dummy.tpl', 'invalid.txt')],
        output_path=str(tmp_path)
    )

    captured = capsys.readouterr()
    assert "must have a '.CUL' extension" in captured.out
    assert not (tmp_path / "PEST_CONTROL.pst").exists()


def test_pst_missing_out_extension(tmp_path, capsys):
    """Test missing .OUT file in pairs"""
    # Get valid params
    repo_root = Path(__file__).parent.parent
    cul_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.CUL"
    cultivar_params, tpl_path = dpest.wheat.ceres.cul(
        P='P1D, P5',
        G='G1, G2, G3',
        PHINT='PHINT',
        cultivar='MANITOU',
        cul_file_path=str(cul_file),
        output_path=str(tmp_path)
    )

    # Valid CUL pair but no OUT
    dpest.pst(
        cultivar_parameters=cultivar_params,
        dataframe_observations=[pd.DataFrame()],
        model_comand_line='dummy',
        input_output_file_pairs=[(str(tpl_path), str(cul_file))],  # No .OUT
        output_path=str(tmp_path)
    )

    captured = capsys.readouterr()
    assert "must have a '.OUT' extension" in captured.out
    assert not (tmp_path / "PEST_CONTROL.pst").exists()


def test_pst_invalid_observations_type(tmp_path, capsys):
    """Test invalid observations type"""
    # Get valid params
    repo_root = Path(__file__).parent.parent
    cul_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.CUL"
    cultivar_params, tpl_path = dpest.wheat.ceres.cul(
        P='P1D, P5',
        G='G1, G2, G3',
        PHINT='PHINT',
        cultivar='MANITOU',
        cul_file_path=str(cul_file),
        output_path=str(tmp_path)
    )

    # Invalid observations type
    dpest.pst(
        cultivar_parameters=cultivar_params,
        dataframe_observations="not_a_dataframe",
        model_comand_line='dummy',
        input_output_file_pairs=[
            (str(tpl_path), str(cul_file)),
            ('dummy.ins', 'dummy.out')  # Valid OUT
        ],
        output_path=str(tmp_path)
    )

    captured = capsys.readouterr()
    assert "must be a DataFrame or a list of DataFrames" in captured.out
    assert not (tmp_path / "PEST_CONTROL.pst").exists()

    ##################################

    def test_pst_invalid_ecotype_type(tmp_path, capsys):
        """Test error when ecotype_parameters is not a dict"""
        # Setup valid cultivar parameters
        repo_root = Path(__file__).parent.parent
        cul_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.CUL"
        cultivar_params, cul_tpl = dpest.wheat.ceres.cul(
            P='P1D, P5',
            G='G1, G2, G3',
            PHINT='PHINT',
            cultivar='MANITOU',  # Valid existing cultivar
            cul_file_path=str(cul_file),
            output_path=str(tmp_path)
        )

        # Setup valid observations
        overview_file = repo_root / "tests/DSSAT48/Wheat/OVERVIEW.OUT"
        overview_obs, _ = dpest.wheat.overview(
            treatment='164.0 KG N/HA IRRIG',
            overview_file_path=str(overview_file),
            output_path=str(tmp_path)
        )

        # Call pst with invalid ecotype_parameters type (string instead of dict)
        dpest.pst(
            cultivar_parameters=cultivar_params,
            ecotype_parameters="invalid_string",  # <-- Invalid type
            dataframe_observations=[overview_obs],
            model_comand_line='dummy',
            input_output_file_pairs=[
                (str(cul_tpl), str(cul_file)),
                ('dummy.ins', 'dummy.out')  # Valid OUT file
            ],
            output_path=str(tmp_path)
        )

        # Verify error handling
        captured = capsys.readouterr()
        assert "`ecotype_parameters`, if provided, must be a dictionary" in captured.out
        assert not (tmp_path / "PEST_CONTROL.pst").exists()


def test_pst_dataframe_observations_required(tmp_path, capsys):
    """Test that dataframe_observations must be provided in pst function."""
    repo_root = Path(__file__).parent.parent
    cul_file = repo_root / "tests/DSSAT48/Genotype/WHCER048.CUL"
    cultivar_params, cul_tpl = dpest.wheat.ceres.cul(
        P='P1D, P5',
        G='G1, G2, G3',
        PHINT='PHINT',
        cultivar='MANITOU',
        cul_file_path=str(cul_file),
        output_path=str(tmp_path)
    )

    # Setup valid input_output_file_pairs
    input_output_pairs = [
        (str(cul_tpl), str(cul_file)),
        ('dummy.ins', 'dummy.out')
    ]

    # Call pst with dataframe_observations=None
    dpest.pst(
        cultivar_parameters=cultivar_params,
        ecotype_parameters=None,
        dataframe_observations=None,
        model_comand_line='dummy',
        input_output_file_pairs=input_output_pairs,
        output_path=str(tmp_path)
    )

    captured = capsys.readouterr()
    assert "`dataframe_observations` must be provided." in captured.out
    assert not (tmp_path / "PEST_CONTROL.pst").exists()