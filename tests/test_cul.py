import dpest
from pathlib import Path

def test_cul_template_generation(tmp_path):
    """Test generation of cultivar template files."""
    # Setup
    repo_root = Path(__file__).parent.parent
    input_file = repo_root / "tests/DSSAT48_data/Genotype/WHCER048.CUL"
    output_dir = tmp_path / "output"

    assert input_file.exists(), f"Input file not found: {input_file}"
    output_dir.mkdir(parents=True, exist_ok=True)

    params, tpl_path = dpest.wheat.ceres.cul(
        P='P1D, P5',
        G='G1, G2, G3',
        PHINT='PHINT',
        cultivar='MANITOU',
        cul_file_path=input_file,
        output_path=output_dir
    )

    assert tpl_path.exists(), "Template file was not created"
