from pathlib import Path
from dpest.utils import *

# Setup path
repo_root = Path(__file__).parent.parent
pst_file_path = repo_root / "tests/dpest_out/PEST_CONTROL.pst"


# Set RSTFLE to “restart”
rstfle(pst_file_path, "restart")

# Set PESTMODE to “prediction”
pestmode(pst_file_path, "prediction")


def test_pestmode_error_handling(tmp_path, capsys):
    """Test error handling for pestmode function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    pestmode(str(missing_file), "estimation")
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. Non-string input
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 3)
    pestmode(str(test_file1), 123)
    captured = capsys.readouterr()
    assert "ValueError: PESTMODE must be a string" in captured.out

    # 3. Invalid mode
    test_file2 = tmp_path / "test2.pst"
    test_file2.write_text("\n" * 3)
    pestmode(str(test_file2), "invalid_mode")
    captured = capsys.readouterr()
    assert "ValueError: PESTMODE must be one of" in captured.out

    # 4. Insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("single line\n")
    pestmode(str(short_file), "estimation")
    captured = capsys.readouterr()
    assert "IndexError: File has only 1 lines" in captured.out

    # 5. Insufficient values on line
    sparse_file = tmp_path / "sparse.pst"
    sparse_file.write_text("\n\nsingle_value\n")
    pestmode(str(sparse_file), "estimation")
    captured = capsys.readouterr()
    assert "ValueError: PESTMODE value not found" in captured.out

# Set RLAMBDA1 to 5.0
rlambda1(pst_file_path, 5.0)

# Set RLAMFAC to 2.0:
rlamfac(pst_file_path, 2.0)

# Set PHIRATSUF to 0.3
phiratsuf(pst_file_path, 0.3)

# Set PHIREDLAM to 0.03
phiredlam(pst_file_path, 0.03)

# Set NUMLAM to 10
numlam(pst_file_path, 10)


def test_numlam_error_handling(tmp_path, capsys):
    """Test error handling for numlam function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    numlam(str(missing_file), 10)
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. ValueError: non-integer input
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 6)
    numlam(str(test_file1), "invalid")
    captured = capsys.readouterr()
    assert "ValueError: NUMLAM must be an integer" in captured.out

    # 3. ValueError: zero value
    test_file2 = tmp_path / "test2.pst"
    test_file2.write_text("\n" * 6)
    numlam(str(test_file2), 0)
    captured = capsys.readouterr()
    assert "ValueError: NUMLAM cannot be zero" in captured.out

    # 4. IndexError: insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("\n" * 5)  # Only 5 lines
    numlam(str(short_file), 10)
    captured = capsys.readouterr()
    assert "IndexError: File has only 5 lines" in captured.out

    # 5. ValueError: insufficient values on line
    sparse_file = tmp_path / "sparse.pst"
    lines = ["\n"] * 5 + ["1 2 3 4\n"]  # Only 4 values on line 6
    sparse_file.write_text("".join(lines))
    numlam(str(sparse_file), 10)
    captured = capsys.readouterr()
    assert "ValueError: NUMLAM position not found" in captured.out


def test_numlam_success(tmp_path):
    """Test successful NUMLAM update"""
    test_file = tmp_path / "valid.pst"
    original_line = "1.0 2 3.0 4 5 6.0\n"  # 5th value is 5
    lines = ["\n"] * 5 + [original_line]
    test_file.write_text("".join(lines))

    # Test positive value
    numlam(str(test_file), 10)
    updated_lines = test_file.read_text().splitlines()
    assert updated_lines[5].split()[4] == "10"

    # Test negative value (valid for Parallel PEST)
    numlam(str(test_file), -1)
    updated_lines = test_file.read_text().splitlines()
    assert updated_lines[5].split()[4] == "-1"

# Set RELPARMAX to 0.2
relparmax(pst_file_path, 0.2)

# Set FACPARMAX to 2.0
facparmax(pst_file_path, 2.0)

def test_facparmax_error_branches(tmp_path, capsys):
    """Test error handling for facparmax function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    facparmax(str(missing_file), 2.0)
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. ValueError: <=1.0
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 7 + "1 2 3\n")
    facparmax(str(test_file1), 0.5)
    captured = capsys.readouterr()
    assert "ValueError: FACPARMAX must be greater than 1.0" in captured.out

    # 3. IndexError: insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("header\n")
    facparmax(str(short_file), 2.0)
    captured = capsys.readouterr()
    assert "IndexError: File has only" in captured.out

    # 4. ValueError: insufficient values on line
    sparse_file = tmp_path / "sparse.pst"
    lines = ["\n"] * 6 + ["single_value\n"]
    sparse_file.write_text("".join(lines))
    facparmax(str(sparse_file), 2.0)
    captured = capsys.readouterr()
    assert "ValueError: FACPARMAX position not found" in captured.out

# Set FACORIG to 01
facorig(pst_file_path, 0.1)

def test_facorig_error_branches(tmp_path, capsys):
    # 1. FileNotFoundError
    missing_file = tmp_path / "no_such_file.pst"
    facorig(str(missing_file), 0.5)
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. ValueError: out of range
    test_file = tmp_path / "test1.pst"
    test_file.write_text("\n" * 7 + "1 2 3\n")  # 8 lines, dummy content
    facorig(str(test_file), 1.5)
    captured = capsys.readouterr()
    assert "ValueError: FACORIG must be between 0.0 and 1.0" in captured.out

    # 3. IndexError: too few lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("only one line\n")
    facorig(str(short_file), 0.5)
    captured = capsys.readouterr()
    assert "IndexError: File has only" in captured.out

    # 4. ValueError: too few values on line
    bad_line_file = tmp_path / "badline.pst"
    lines = ["\n"] * 6 + ["one two\n"]
    bad_line_file.write_text("".join(lines))
    facorig(str(bad_line_file), 0.5)
    captured = capsys.readouterr()
    assert "ValueError: FACORIG position not found in control data line" in captured.out

# Set PHIREDSWH to 0.1
phiredswh(pst_file_path, 0.1)

# Set NOPTMAX to 50 (iterative optimization)
noptmax(pst_file_path, new_value = 50)

def test_noptmax_error_handling(tmp_path, capsys):
    """Test error handling for noptmax function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    noptmax(str(missing_file))
    captured = capsys.readouterr()
    assert "Error: The file" in captured.out

    # 2. ValueError: non-integer input
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 9)
    noptmax(str(test_file1), "invalid")
    captured = capsys.readouterr()
    assert "ValueError: NOPTMAX must be an integer" in captured.out

    # 3. ValueError: invalid value (-3)
    test_file2 = tmp_path / "test2.pst"
    test_file2.write_text("\n" * 9)
    noptmax(str(test_file2), -3)
    captured = capsys.readouterr()
    assert "ValueError: NOPTMAX must be -2, -1, 0" in captured.out

    # 4. IndexError: insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("\n" * 8)  # Only 8 lines
    noptmax(str(short_file))
    captured = capsys.readouterr()
    assert "IndexError: Expected at least 9 lines" in captured.out

    # 5. ValueError: empty NOPTMAX line (CORRECTED)
    empty_line_file = tmp_path / "empty_line.pst"
    lines = ["\n"] * 9  # 9 empty lines (index 8 exists but is empty)
    empty_line_file.write_text("".join(lines))
    noptmax(str(empty_line_file))
    captured = capsys.readouterr()
    assert "ValueError: NOPTMAX line not found" in captured.out

# Set PHIREDSTP to 0.01
phiredstp(pst_file_path, 0.01)

# Set NPHISTP to 3
nphistp(pst_file_path, 3)


def test_nphistp_error_handling(tmp_path, capsys):
    """Test error handling for nphistp function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    nphistp(str(missing_file), 3)
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. ValueError: non-integer input
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 9)
    nphistp(str(test_file1), "invalid")
    captured = capsys.readouterr()
    assert "ValueError: NPHISTP must be an integer" in captured.out

    # 3. ValueError: <=0 value
    test_file2 = tmp_path / "test2.pst"
    test_file2.write_text("\n" * 9)
    nphistp(str(test_file2), 0)
    captured = capsys.readouterr()
    assert "ValueError: NPHISTP must be greater than zero" in captured.out

    # 4. IndexError: insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("\n" * 8)  # Only 8 lines
    nphistp(str(short_file), 3)
    captured = capsys.readouterr()
    assert "IndexError: File has only 8 lines" in captured.out

    # 5. ValueError: insufficient values on line
    sparse_file = tmp_path / "sparse.pst"
    lines = ["\n"] * 8 + ["1 2\n"]  # Only 2 values on line 9
    sparse_file.write_text("".join(lines))
    nphistp(str(sparse_file), 3)
    captured = capsys.readouterr()
    assert "ValueError: NPHISTP position not found" in captured.out


def test_nphistp_success(tmp_path):
    """Test successful NPHISTP update"""
    test_file = tmp_path / "valid.pst"
    original_line = "1.0 2.0 3 4.0 5.0\n"
    lines = ["\n"] * 8 + [original_line]
    test_file.write_text("".join(lines))

    # Update NPHISTP value
    nphistp(str(test_file), 5)

    # Verify update
    updated_lines = test_file.read_text().splitlines()
    updated_values = updated_lines[8].split()
    assert updated_values[2] == "5"

# Set NPHINORED to 5
nphinored(pst_file_path, 5)

def test_nphinored_error_handling(tmp_path, capsys):
    """Test error handling for nphinored function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    nphinored(str(missing_file), 5)
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. ValueError: non-integer input
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 9)
    nphinored(str(test_file1), "invalid")
    captured = capsys.readouterr()
    assert "ValueError: NPHINORED must be an integer" in captured.out

    # 3. ValueError: <=0 value
    test_file2 = tmp_path / "test2.pst"
    test_file2.write_text("\n" * 9)
    nphinored(str(test_file2), 0)
    captured = capsys.readouterr()
    assert "ValueError: NPHINORED must be greater than zero" in captured.out

    # 4. IndexError: insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("\n" * 8)  # Only 8 lines
    nphinored(str(short_file), 5)
    captured = capsys.readouterr()
    assert "IndexError: File has only 8 lines" in captured.out

    # 5. ValueError: insufficient values on line
    sparse_file = tmp_path / "sparse.pst"
    lines = ["\n"] * 8 + ["1 2 3\n"]  # Only 3 values on line 9
    sparse_file.write_text("".join(lines))
    nphinored(str(sparse_file), 5)
    captured = capsys.readouterr()
    assert "ValueError: NPHINORED position not found" in captured.out

def test_nphinored_success(tmp_path):
    """Test successful NPHINORED update"""
    test_file = tmp_path / "valid.pst"
    lines = ["\n"] * 8 + ["1 2 3 4 5\n"]  # Valid

# Set RELPARSTP to 0.01
relparstp(pst_file_path, 0.01)

# Set NRELPAR to 3
nrelpar(pst_file_path, 3)


def test_nrelpar_error_handling(tmp_path, capsys):
    """Test error handling for nrelpar function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    nrelpar(str(missing_file), 3)
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. ValueError: non-integer input
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 9)
    nrelpar(str(test_file1), "invalid")
    captured = capsys.readouterr()
    assert "ValueError: NRELPAR must be an integer" in captured.out

    # 3. ValueError: <=0 value
    test_file2 = tmp_path / "test2.pst"
    test_file2.write_text("\n" * 9)
    nrelpar(str(test_file2), 0)
    captured = capsys.readouterr()
    assert "ValueError: NRELPAR must be greater than zero" in captured.out

    # 4. IndexError: insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("\n" * 8)  # Only 8 lines
    nrelpar(str(short_file), 3)
    captured = capsys.readouterr()
    assert "IndexError: File has only 8 lines" in captured.out

    # 5. ValueError: insufficient values on line
    sparse_file = tmp_path / "sparse.pst"
    lines = ["\n"] * 8 + ["1 2 3 4 5\n"]  # Only 5 values on line 9
    sparse_file.write_text("".join(lines))
    nrelpar(str(sparse_file), 3)
    captured = capsys.readouterr()
    assert "ValueError: NRELPAR position not found" in captured.out


def test_nrelpar_success(tmp_path):
    """Test successful NRELPAR update"""
    test_file = tmp_path / "valid.pst"
    original_line = "1.0 2 3.0 4 5.0 6 7.0\n"  # 6th value is 6
    lines = ["\n"] * 8 + [original_line]
    test_file.write_text("".join(lines))

    # Update NRELPAR value
    nrelpar(str(test_file), 5)

    # Verify update
    updated_lines = test_file.read_text().splitlines()
    updated_values = updated_lines[8].split()
    assert updated_values[5] == "5", "NRELPAR value not updated correctly"
    assert len(updated_values) == 7, "Number of values should remain unchanged"

# Updating Specific LSQR Parameters in an Existing PEST Control File
lsqr(
    pst_path = pst_file_path,
    lsqr_atol = 1e-6,
    lsqr_btol = 1e-6,
    lsqr_itnlim = 50
)

# Disabling LSQR Mode While Maintaining Other Settings
lsqr(
    pst_path = pst_file_path,
    lsqrmode = 0
)

# Adding an SVD Section to a PEST Control File with Default Parameters
svd(
    pst_path = pst_file_path
)

# Customizing SVD Parameters in an Existing PEST Control File
svd(
    pst_path = pst_file_path,
    maxsing = 500,
    eigthresh = 0.01,
    eigwrite = 1
)

# Removing the LSQR Section from a PEST Control File
rmv_splitcols(pst_file_path)