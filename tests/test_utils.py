from pathlib import Path
from dpest.utils import *

# Setup path
repo_root = Path(__file__).parent.parent
pst_file_path = repo_root / "tests/dpest_out/PEST_CONTROL.pst"


# Set RSTFLE to “restart”
rstfle(pst_file_path, "restart")


def test_rstfle_error_handling(tmp_path, capsys):
    """Test error handling for rstfle function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    rstfle(str(missing_file), "restart")
    captured = capsys.readouterr()
    assert "Error: The file" in captured.out

    # 2. Non-string input
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 3)
    rstfle(str(test_file1), 123)
    captured = capsys.readouterr()
    assert "ValueError: RSTFLE must be a string" in captured.out

    # 3. Invalid string value
    rstfle(str(test_file1), "invalid")
    captured = capsys.readouterr()
    assert "ValueError: RSTFLE must be either 'restart' or 'norestart'" in captured.out

    # 4. Insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("\n" * 2)  # Only 2 lines
    rstfle(str(short_file), "restart")
    captured = capsys.readouterr()
    assert "IndexError: Expected at least 3 lines" in captured.out

    # 5. Empty target line
    empty_line_file = tmp_path / "empty_line.pst"
    lines = ["* control\n", "\n", "\n"]  # Empty line 3
    empty_line_file.write_text("".join(lines))
    rstfle(str(empty_line_file), "restart")
    captured = capsys.readouterr()
    assert "ValueError: RSTFLE line not found or is empty" in captured.out


def test_rstfle_success(tmp_path):
    """Test successful RSTFLE updates"""
    # Create test file
    test_file = tmp_path / "valid.pst"
    original_line = "  restart  param1  param2\n"
    lines = ["* control\n", "dummy line\n", original_line]
    test_file.write_text("".join(lines))

    # Test both valid values with different cases
    for value in ["RESTART", "norestart"]:
        rstfle(str(test_file), value)

        # Verify update
        updated_lines = test_file.read_text().splitlines()
        updated_values = updated_lines[2].split()

        # Check RSTFLE value (first value, lowercase)
        assert updated_values[0] == value.lower()

        # Verify other values remain unchanged
        assert updated_values[1:] == ["param1", "param2"]

        # Check formatting preservation
        assert updated_lines[2].startswith("  "), "Leading whitespace not preserved"
        assert "  " in updated_lines[2], "Value spacing not preserved"

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


def test_rlambda1_error_handling(tmp_path, capsys):
    """Test error handling for rlambda1 function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    rlambda1(str(missing_file), 5.0)
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. ValueError: non-float input
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 6)
    rlambda1(str(test_file1), "invalid")
    captured = capsys.readouterr()
    assert "could not convert string to float" in captured.out

    # 3. ValueError: negative value
    rlambda1(str(test_file1), -1.0)
    captured = capsys.readouterr()
    assert "RLAMBDA1 must be zero or greater" in captured.out

    # 4. IndexError: insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("\n" * 5)  # Only 5 lines
    rlambda1(str(short_file), 5.0)
    captured = capsys.readouterr()
    assert "IndexError: File has only 5 lines" in captured.out

    # 5. ValueError: empty line
    empty_line_file = tmp_path / "empty_line.pst"
    lines = ["\n"] * 5 + ["\n"]  # Empty line 6
    empty_line_file.write_text("".join(lines))
    rlambda1(str(empty_line_file), 5.0)
    captured = capsys.readouterr()
    assert "RLAMBDA1 line is empty" in captured.out


def test_rlambda1_success(tmp_path):
    """Test successful RLAMBDA1 updates"""
    # Create test file with proper structure
    test_file = tmp_path / "valid.pst"
    original_line = "  1.000000E+00  2.000000E+00  3.000000E+00\n"
    lines = ["* control\n"] * 2 + ["\n"] * 3 + [original_line]
    test_file.write_text("".join(lines))

    # Test valid values
    for value, expected in [(0.0, "0.000000E+00"), (5.0, "5.000000E+00"), (0.01, "1.000000E-02")]:
        rlambda1(str(test_file), value)

        # Verify update
        updated_lines = test_file.read_text().splitlines()
        updated_values = updated_lines[5].split()

        # Check RLAMBDA1 (first value)
        assert updated_values[0] == expected

        # Verify other values remain unchanged
        assert updated_values[1] == "2.000000E+00"
        assert updated_values[2] == "3.000000E+00"

        # Check formatting preservation
        assert updated_lines[5].startswith("  "), "Leading whitespace not preserved"
        assert "   " in updated_lines[5], "Value spacing not preserved"


# Set RLAMFAC to 2.0:
rlamfac(pst_file_path, 2.0)


def test_rlamfac_error_handling(tmp_path, capsys):
    """Test error handling for rlamfac function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    rlamfac(str(missing_file), 2.0)
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. ValueError: non-float input
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 6)
    rlamfac(str(test_file1), "invalid")
    captured = capsys.readouterr()
    assert "could not convert string to float" in captured.out

    # 3. ValueError: zero value
    rlamfac(str(test_file1), 0.0)
    captured = capsys.readouterr()
    assert "RLAMFAC must not be zero" in captured.out

    # 4. IndexError: insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("\n" * 5)  # Only 5 lines
    rlamfac(str(short_file), 2.0)
    captured = capsys.readouterr()
    assert "IndexError: File has only 5 lines" in captured.out

    # 5. ValueError: insufficient values
    sparse_file = tmp_path / "sparse.pst"
    lines = ["\n"] * 5 + ["single_value\n"]  # Only 1 value on line 6
    sparse_file.write_text("".join(lines))
    rlamfac(str(sparse_file), 2.0)
    captured = capsys.readouterr()
    assert "RLAMFAC value not found" in captured.out


def test_rlamfac_success(tmp_path):
    """Test successful RLAMFAC updates"""
    # Create test file with proper structure
    test_file = tmp_path / "valid.pst"
    original_line = "  1.000000E+00  2.000000E+00  3.000000E+00\n"
    lines = ["* control\n"] * 2 + ["\n"] * 3 + [original_line]
    test_file.write_text("".join(lines))

    # Test positive and negative values
    for value, expected in [(2.0, "2.000000E+00"), (-3.0, "-3.000000E+00")]:
        rlamfac(str(test_file), value)

        # Verify update
        updated_lines = test_file.read_text().splitlines()
        updated_values = updated_lines[5].split()

        # Check RLAMFAC (second value)
        assert updated_values[1] == expected

        # Verify other values remain unchanged
        assert updated_values[0] == "1.000000E+00"
        assert updated_values[2] == "3.000000E+00"

        # Check formatting preservation
        assert updated_lines[5].startswith("  "), "Leading whitespace not preserved"
        assert "   " in updated_lines[5], "Value spacing not preserved"

# Set PHIRATSUF to 0.3
phiratsuf(pst_file_path, 0.3)

def test_phiratsuf_error_handling(tmp_path, capsys):
    """Test error handling for phiratsuf function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    phiratsuf(str(missing_file), 0.3)
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. ValueError: <0
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 6)
    phiratsuf(str(test_file1), -0.1)
    captured = capsys.readouterr()
    assert "ValueError: PHIRATSUF must be between 0.0 and 1.0" in captured.out

    # 3. ValueError: >1
    phiratsuf(str(test_file1), 1.1)
    captured = capsys.readouterr()
    assert "ValueError: PHIRATSUF must be between 0.0 and 1.0" in captured.out

    # 4. IndexError: insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("\n" * 5)  # Only 5 lines
    phiratsuf(str(short_file), 0.3)
    captured = capsys.readouterr()
    assert "IndexError: File has only 5 lines" in captured.out

    # 5. ValueError: insufficient values
    sparse_file = tmp_path / "sparse.pst"
    lines = ["\n"] * 5 + ["1 2\n"]  # Only 2 values on line 6
    sparse_file.write_text("".join(lines))
    phiratsuf(str(sparse_file), 0.3)
    captured = capsys.readouterr()
    assert "ValueError: PHIRATSUF position not found" in captured.out


def test_phiratsuf_success(tmp_path):
    """Test successful PHIRATSUF update"""
    # Create test file with proper structure
    test_file = tmp_path / "valid.pst"
    original_line = "  1.000000E+00  2.000000E+00  3.000000E-01  4.000000E+00\n"
    lines = ["* control\n", "\n", "\n", "\n", "\n", original_line]
    test_file.write_text("".join(lines))

    # Update PHIRATSUF value
    phiratsuf(str(test_file), 0.5)

    # Verify changes
    updated_lines = test_file.read_text().splitlines()
    updated_values = updated_lines[5].split()

    # Check updated value (3rd position)
    assert updated_values[2] == "5.000000E-01"

    # Verify other values remain unchanged
    assert updated_values[0] == "1.000000E+00"
    assert updated_values[1] == "2.000000E+00"
    assert updated_values[3] == "4.000000E+00"

    # Check formatting preservation
    assert updated_lines[5].startswith("  "), "Leading whitespace not preserved"

# Set PHIREDLAM to 0.03
phiredlam(pst_file_path, 0.03)


def test_phiredlam_error_handling(tmp_path, capsys):
    """Test error handling for phiredlam function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    phiredlam(str(missing_file), 0.03)
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. ValueError: <0
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 6)
    phiredlam(str(test_file1), -0.1)
    captured = capsys.readouterr()
    assert "ValueError: PHIREDLAM must be between 0.0 and 1.0" in captured.out

    # 3. ValueError: >1
    phiredlam(str(test_file1), 1.1)
    captured = capsys.readouterr()
    assert "ValueError: PHIREDLAM must be between 0.0 and 1.0" in captured.out

    # 4. IndexError: insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("\n" * 5)  # Only 5 lines
    phiredlam(str(short_file), 0.03)
    captured = capsys.readouterr()
    assert "IndexError: File has only 5 lines" in captured.out

    # 5. ValueError: insufficient values
    sparse_file = tmp_path / "sparse.pst"
    lines = ["\n"] * 5 + ["1 2 3\n"]  # Only 3 values on line 6
    sparse_file.write_text("".join(lines))
    phiredlam(str(sparse_file), 0.03)
    captured = capsys.readouterr()
    assert "ValueError: PHIREDLAM position not found" in captured.out


def test_phiredlam_success(tmp_path):
    """Test successful PHIREDLAM update"""
    # Create test file with proper structure
    test_file = tmp_path / "valid.pst"
    original_line = "  1.000E+00  2.000E+00  3.000E-01  4.000E-02  5.000E+00\n"
    lines = ["* control\n", "\n", "\n", "\n", "\n", original_line]
    test_file.write_text("".join(lines))

    # Test with different valid values
    for value, expected in [(0.03, "3.000000E-02"), (0.5, "5.000000E-01")]:
        phiredlam(str(test_file), value)

        # Verify update
        updated_lines = test_file.read_text().splitlines()
        updated_values = updated_lines[5].split()

        # Check PHIREDLAM (4th value)
        assert updated_values[3] == expected

        # Verify other values remain unchanged
        assert updated_values[0] == "1.000E+00"

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


def test_relparmax_error_handling(tmp_path, capsys):
    """Test error handling for relparmax function"""
    # 1. FileNotFoundError (unchanged)
    missing_file = tmp_path / "missing.pst"
    relparmax(str(missing_file), 0.2)
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. Type Error: non-float input
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 7)
    relparmax(str(test_file1), "invalid")
    captured = capsys.readouterr()
    assert "could not convert string to float" in captured.out  # Updated assertion

    # 3. Value Error: <=0 values (unchanged)
    relparmax(str(test_file1), 0.0)
    captured = capsys.readouterr()
    assert "RELPARMAX must be greater than zero" in captured.out

    relparmax(str(test_file1), -0.5)
    captured = capsys.readouterr()
    assert "RELPARMAX must be greater than zero" in captured.out

    # 4. IndexError: insufficient lines (unchanged)
    short_file = tmp_path / "short.pst"
    short_file.write_text("\n" * 6)
    relparmax(str(short_file), 0.2)
    captured = capsys.readouterr()
    assert "IndexError: File has only 6 lines" in captured.out

    # 5. ValueError: empty line (unchanged)
    empty_line_file = tmp_path / "empty_line.pst"
    lines = ["\n"] * 6 + ["\n"]
    empty_line_file.write_text("".join(lines))
    relparmax(str(empty_line_file), 0.2)
    captured = capsys.readouterr()
    assert "RELPARMAX line is empty" in captured.out


def test_relparmax_success(tmp_path):
    """Test successful RELPARMAX update"""
    # Create test file with proper structure
    test_file = tmp_path / "valid.pst"
    original_line = "  1.000000E+00  2.000000E+00  3.000000E+00\n"
    lines = ["* control\n"] * 2 + ["\n"] * 4 + [original_line]
    test_file.write_text("".join(lines))

    # Test different valid values
    for value, expected in [(0.2, "2.000000E-01"), (5.0, "5.000000E+00")]:
        relparmax(str(test_file), value)

        # Verify update
        updated_lines = test_file.read_text().splitlines()
        updated_values = updated_lines[6].split()

        # Check RELPARMAX (first value)
        assert updated_values[0] == expected

        # Verify other values remain unchanged
        assert updated_values[1] == "2.000000E+00"
        assert updated_values[2] == "3.000000E+00"

        # Check formatting preservation
        assert updated_lines[6].startswith("  "), "Leading whitespace not preserved"
        assert "   " in updated_lines[6], "Value spacing not preserved"

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


def test_phiredswh_error_handling(tmp_path, capsys):
    """Test error handling for phiredswh function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    phiredswh(str(missing_file), 0.1)
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. ValueError: <0
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 8)
    phiredswh(str(test_file1), -0.1)
    captured = capsys.readouterr()
    assert "ValueError: PHIREDSWH must be between 0.0 and 1.0" in captured.out

    # 3. ValueError: >1
    phiredswh(str(test_file1), 1.1)
    captured = capsys.readouterr()
    assert "ValueError: PHIREDSWH must be between 0.0 and 1.0" in captured.out

    # 4. IndexError: insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("\n" * 7)  # Only 7 lines
    phiredswh(str(short_file), 0.1)
    captured = capsys.readouterr()
    assert "IndexError: File has only 7 lines" in captured.out

    # 5. ValueError: empty line
    empty_line_file = tmp_path / "empty_line.pst"
    lines = ["\n"] * 7 + ["\n"]  # Empty line 8
    empty_line_file.write_text("".join(lines))
    phiredswh(str(empty_line_file), 0.1)
    captured = capsys.readouterr()
    assert "ValueError: PHIREDSWH line is empty" in captured.out


def test_phiredswh_success(tmp_path):
    """Test successful PHIREDSWH update"""
    # Create test file with proper structure
    test_file = tmp_path / "valid.pst"
    original_line = "  1.000000E-01  2.000000E+00  3.000000E-03\n"
    lines = ["* control\n"] * 2 + ["\n"] * 5 + [original_line]
    test_file.write_text("".join(lines))

    # Test different valid values
    for value, expected in [(0.01, "1.000000E-02"), (0.5, "5.000000E-01")]:
        phiredswh(str(test_file), value)

        # Verify update
        updated_lines = test_file.read_text().splitlines()
        updated_values = updated_lines[7].split()

        # Check PHIREDSWH (first value)
        assert updated_values[0] == expected

        # Verify other values remain unchanged
        assert updated_values[1] == "2.000000E+00"
        assert updated_values[2] == "3.000000E-03"

        # Check formatting preservation
        assert updated_lines[7].startswith("  "), "Leading whitespace not preserved"
        assert "   " in updated_lines[7], "Value spacing not preserved"


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


def test_phiredstp_error_handling(tmp_path, capsys):
    """Test error handling for phiredstp function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    phiredstp(str(missing_file), 0.01)
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. ValueError: <=0
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 9)
    phiredstp(str(test_file1), 0.0)
    captured = capsys.readouterr()
    assert "ValueError: PHIREDSTP must be greater than zero" in captured.out

    # 3. IndexError: insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("\n" * 8)  # Only 8 lines
    phiredstp(str(short_file), 0.01)
    captured = capsys.readouterr()
    assert "IndexError: File has only 8 lines" in captured.out

    # 4. ValueError: insufficient values
    sparse_file = tmp_path / "sparse.pst"
    lines = ["\n"] * 8 + ["single_value\n"]
    sparse_file.write_text("".join(lines))
    phiredstp(str(sparse_file), 0.01)
    captured = capsys.readouterr()
    assert "ValueError: PHIREDSTP position not found" in captured.out


def test_phiredstp_success(tmp_path):
    """Test successful PHIREDSTP update"""
    # Create test file with proper structure
    test_file = tmp_path / "valid.pst"
    original_line = "  1.000000E+00  2.000000E-02  3.000000E+00\n"
    lines = ["* control\n"] * 2 + ["\n"] * 6 + [original_line]
    test_file.write_text("".join(lines))

    # Update PHIREDSTP value
    phiredstp(str(test_file), 0.001)

    # Verify changes
    updated_lines = test_file.read_text().splitlines()
    updated_values = updated_lines[8].split()

    # Check PHIREDSTP value (2nd position)
    assert updated_values[1] == "1.000000E-03"

    # Verify other values remain unchanged
    assert updated_values[0] == "1.000000E+00"
    assert updated_values[2] == "3.000000E+00"

    # Check formatting preservation
    assert updated_lines[8].startswith("  "), "Leading whitespace not preserved"
    assert "   " in updated_lines[8], "Value spacing not preserved"


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


def test_relparstp_error_handling(tmp_path, capsys):
    """Test error handling for relparstp function"""
    # 1. FileNotFoundError
    missing_file = tmp_path / "missing.pst"
    relparstp(str(missing_file), 0.01)
    captured = capsys.readouterr()
    assert "Error: File" in captured.out

    # 2. ValueError: non-float input
    test_file1 = tmp_path / "test1.pst"
    test_file1.write_text("\n" * 9)
    relparstp(str(test_file1), "invalid")
    captured = capsys.readouterr()
    assert "could not convert string to float" in captured.out

    # 3. ValueError: <=0 values
    relparstp(str(test_file1), 0.0)
    captured = capsys.readouterr()
    assert "RELPARSTP must be greater than zero" in captured.out

    relparstp(str(test_file1), -0.5)
    captured = capsys.readouterr()
    assert "RELPARSTP must be greater than zero" in captured.out

    # 4. IndexError: insufficient lines
    short_file = tmp_path / "short.pst"
    short_file.write_text("\n" * 8)  # Only 8 lines
    relparstp(str(short_file), 0.01)
    captured = capsys.readouterr()
    assert "IndexError: File has only 8 lines" in captured.out

    # 5. ValueError: insufficient values
    sparse_file = tmp_path / "sparse.pst"
    lines = ["\n"] * 8 + ["1 2 3 4\n"]  # Only 4 values on line 9
    sparse_file.write_text("".join(lines))
    relparstp(str(sparse_file), 0.01)
    captured = capsys.readouterr()
    assert "RELPARSTP position not found" in captured.out


def test_relparstp_success(tmp_path):
    """Test successful RELPARSTP update"""
    # Create test file with proper structure
    test_file = tmp_path / "valid.pst"
    original_line = "  1.000000E+00  2.000000E+00  3.000000E+00  4.000000E+00  5.000000E-02\n"
    lines = ["* control\n"] * 2 + ["\n"] * 6 + [original_line]
    test_file.write_text("".join(lines))

    # Update RELPARSTP value
    relparstp(str(test_file), 0.001)

    # Verify changes
    updated_lines = test_file.read_text().splitlines()
    updated_values = updated_lines[8].split()

    # Check RELPARSTP value (5th position)
    assert updated_values[4] == "1.000000E-03"

    # Verify other values remain unchanged
    assert updated_values[0] == "1.000000E+00"
    assert updated_values[1] == "2.000000E+00"
    assert updated_values[2] == "3.000000E+00"
    assert updated_values[3] == "4.000000E+00"

    # Check formatting preservation
    assert updated_lines[8].startswith("  "), "Leading whitespace not preserved"
    assert "   " in updated_lines[8], "Value spacing not preserved"


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


def test_lsqr_add_new_section(tmp_path, capsys):
    """Test adding new LSQR section with defaults"""
    # Create minimal PEST file
    test_file = tmp_path / "test.pst"
    content = [
        "* control data\n",
        "1 1 1 1 1\n",
        "* model\n"
    ]
    test_file.write_text("".join(content))

    # Add LSQR with defaults
    lsqr(str(test_file))

    # Verify output
    captured = capsys.readouterr()
    assert "LSQR section added successfully" in captured.out

    # Verify section content
    updated = test_file.read_text().splitlines()
    assert "* lsqr" in updated
    assert "1" in updated[3]  # lsqrmode
    assert "1.000000E-04 1.000000E-04 2.800000E+01 28" in updated[4]
    assert "0" in updated[5]


def test_lsqr_update_existing(tmp_path, capsys):
    """Test updating existing LSQR section"""
    # Create file with LSQR section
    test_file = tmp_path / "test.pst"
    content = [
        "* control data\n",
        "1 1 1 1 1\n",
        "* lsqr\n",
        "1\n",
        "1e-4 1e-4 28.0 28\n",
        "0\n",
        "* model\n"
    ]
    test_file.write_text("".join(content))

    # Update parameters
    lsqr(str(test_file), lsqr_atol=1e-6, lsqr_itnlim=50)

    # Verify output
    captured = capsys.readouterr()
    assert "LSQR section updated successfully" in captured.out

    # Verify updates
    updated = test_file.read_text().splitlines()
    assert "1.000000E-06 1.000000E-04 2.800000E+01 50" in updated[4]


def test_lsqr_invalid_parameters(tmp_path, capsys):
    """Test parameter validation"""
    test_file = tmp_path / "test.pst"
    test_file.write_text("* control data\n\n* model\n")

    # Test invalid lsqrmode
    lsqr(str(test_file), lsqrmode=2)
    captured = capsys.readouterr()
    assert "lsqrmode must be 0 or 1" in captured.out

    # Test negative atol
    lsqr(str(test_file), lsqr_atol=-1)
    captured = capsys.readouterr()
    assert "lsqr_atol must be greater than or equal to 0" in captured.out

    # Test negative btol (NEW)
    lsqr(str(test_file), lsqr_btol=-1)
    captured = capsys.readouterr()
    assert "lsqr_btol must be greater than or equal to 0" in captured.out

    # Test negative conlim (NEW)
    lsqr(str(test_file), lsqr_conlim=-1)
    captured = capsys.readouterr()
    assert "lsqr_conlim must be greater than or equal to 0" in captured.out

    # Test invalid itnlim
    lsqr(str(test_file), lsqr_itnlim=0)
    captured = capsys.readouterr()
    assert "lsqr_itnlim must be an integer greater than 0" in captured.out

    # Test invalid lsqrwrite (NEW)
    lsqr(str(test_file), lsqrwrite=2)
    captured = capsys.readouterr()
    assert "lsqrwrite must be 0 or 1" in captured.out


def test_lsqr_file_not_found(capsys):
    """Test handling of missing file"""
    lsqr("non_existent.pst")
    captured = capsys.readouterr()
    assert "File not found" in captured.out


def test_lsqr_svd_warning(tmp_path, capsys):
    """Test SVD incompatibility warning"""
    test_file = tmp_path / "test.pst"
    content = [
        "* control data\n",
        "* singular value decomposition\n",
        "svd_params\n",
        "* model\n"
    ]
    test_file.write_text("".join(content))

    lsqr(str(test_file), lsqrmode=1)
    captured = capsys.readouterr()
    assert "Warning: LSQR and SVD cannot be used together" in captured.out


def test_lsqr_malformed_existing(tmp_path, capsys):
    """Test handling of malformed existing section"""
    test_file = tmp_path / "test.pst"
    content = [
        "* control data\n",
        "* lsqr\n",
        "invalid\n",
        "values\n",
        "* model\n"
    ]
    test_file.write_text("".join(content))

    lsqr(str(test_file), lsqrmode=0)
    captured = capsys.readouterr()
    assert "Warning: Error parsing existing LSQR values" in captured.out
    assert "LSQR section updated successfully" in captured.out

    updated = test_file.read_text().splitlines()
    assert "0" in updated[2]  # Verify lsqrmode was updated


def test_lsqr_case_insensitivity(tmp_path):
    """Test case-insensitive section detection"""
    test_file = tmp_path / "test.pst"
    content = [
        "* CONTROL DATA\n",
        "* LSQR\n",
        "1\n",
        "* MODEL\n"
    ]
    test_file.write_text("".join(content))

    lsqr(str(test_file), lsqrwrite=1)
    updated = test_file.read_text().splitlines()
    assert "1" in updated[4]  # lsqrwrite line

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


def test_svd_add_new_section(tmp_path, capsys):
    """Test adding new SVD section with defaults"""
    # Create minimal PEST file
    test_file = tmp_path / "test.pst"
    content = [
        "* control data\n",
        "1 1 1 1 1\n",
        "* model\n"
    ]
    test_file.write_text("".join(content))

    # Add SVD with defaults
    svd(str(test_file))

    # Verify output
    captured = capsys.readouterr()
    assert "SVD section added successfully" in captured.out

    # Verify section content
    updated = test_file.read_text().splitlines()
    assert "* singular value decomposition" in updated
    assert "1" in updated[3]  # svdmode
    assert "10000000 1.000000E-06" in updated[4]
    assert "0" in updated[5]


def test_svd_update_existing(tmp_path, capsys):
    """Test updating existing SVD section"""
    # Create file with SVD section
    test_file = tmp_path / "test.pst"
    content = [
        "* control data\n",
        "1 1 1 1 1\n",
        "* singular value decomposition\n",
        "1\n",
        "500 1e-4\n",
        "0\n",
        "* model\n"
    ]
    test_file.write_text("".join(content))

    # Update parameters
    svd(str(test_file), maxsing=1000, eigthresh=0.01, eigwrite=1)

    # Verify output
    captured = capsys.readouterr()
    assert "SVD section updated successfully" in captured.out

    # Verify updates
    updated = test_file.read_text().splitlines()
    assert "1000 1.000000E-02" in updated[4]
    assert "1" in updated[5]


def test_svd_parameter_validation(tmp_path, capsys):
    """Test parameter validation"""
    test_file = tmp_path / "test.pst"
    test_file.write_text("* control data\n\n* model\n")

    # Test invalid svdmode
    svd(str(test_file), svdmode=2)
    captured = capsys.readouterr()
    assert "svdmode must be 0 or 1" in captured.out

    # Test invalid maxsing
    svd(str(test_file), maxsing=0)
    captured = capsys.readouterr()
    assert "maxsing must be > 0" in captured.out

    # Test invalid eigthresh
    svd(str(test_file), eigthresh=1.5)
    captured = capsys.readouterr()
    assert "eigthresh must be 0 ≤ value < 1" in captured.out

    # Test invalid eigwrite
    svd(str(test_file), eigwrite=2)
    captured = capsys.readouterr()
    assert "eigwrite must be 0 or 1" in captured.out


def test_svd_file_not_found(capsys):
    """Test handling of missing file"""
    svd("non_existent.pst")
    captured = capsys.readouterr()
    assert "File not found" in captured.out


def test_svd_lsqr_conflict(tmp_path, capsys):
    """Test LSQR conflict warning"""
    test_file = tmp_path / "test.pst"
    content = [
        "* control data\n",
        "* lsqr\n",
        "lsqr_params\n",
        "* model\n"
    ]
    test_file.write_text("".join(content))

    svd(str(test_file))
    captured = capsys.readouterr()
    assert "Warning: SVD and LSQR are mutually exclusive" in captured.out


def test_svd_malformed_existing(tmp_path, capsys):
    """Test handling of malformed existing section"""
    test_file = tmp_path / "test.pst"
    content = [
        "* control data\n",
        "* singular value decomposition\n",
        "invalid\n",
        "values\n",
        "here\n",
        "* model\n"
    ]
    test_file.write_text("".join(content))

    svd(str(test_file), svdmode=0)
    captured = capsys.readouterr()
    assert "Error parsing SVD values" in captured.out
    assert "SVD section updated successfully" in captured.out

    updated = test_file.read_text().splitlines()
    assert "0" in updated[2]  # Verify svdmode was updated


def test_svd_case_insensitivity(tmp_path):
    """Test case-insensitive section detection"""
    test_file = tmp_path / "test.pst"
    content = [
        "* CONTROL DATA\n",
        "* SINGULAR VALUE DECOMPOSITION\n",
        "1\n",
        "* MODEL\n"
    ]
    test_file.write_text("".join(content))

    svd(str(test_file), maxsing=500)
    updated = test_file.read_text().splitlines()
    assert "500" in updated[3]


def test_svd_disable_mode(tmp_path, capsys):
    """Test disabling SVD mode"""
    test_file = tmp_path / "test.pst"
    content = [
        "* control data\n",
        "* singular value decomposition\n",
        "1\n",
        "1000 0.1\n",
        "1\n",
        "* model\n"
    ]
    test_file.write_text("".join(content))

    svd(str(test_file), svdmode=0)
    captured = capsys.readouterr()
    assert "SVD section updated successfully" in captured.out

    updated = test_file.read_text().splitlines()
    assert "0" in updated[2]  # svdmode line
    assert "1000 1.000000E-01" in updated[3]  # other params preserved

def test_svd_missing_control_section(tmp_path, capsys):
    """Test handling missing control data section"""
    test_file = tmp_path / "test.pst"
    content = [
        "* model\n",
        "model_data\n"
    ]
    test_file.write_text("".join(content))

    svd(str(test_file))
    captured = capsys.readouterr()
    assert "Missing required '* control data' section" in captured.out



# Removing the LSQR Section from a PEST Control File
rmv_splitcols(pst_file_path)

def test_rmv_lsqr_successful_removal(tmp_path, capsys):
    """Test removal of existing LSQR section"""
    # Create test file with LSQR section
    test_file = tmp_path / "test.pst"
    content = [
        "* control\n",
        "dummy line\n",
        "* lsqr\n",
        "lsqr_param1 1.0\n",
        "lsqr_param2 2.0\n",
        "* model\n",
        "model_data\n"
    ]
    test_file.write_text("".join(content))

    # Run function
    rmv_lsqr(str(test_file))

    # Verify output
    captured = capsys.readouterr()
    assert "LSQR section removed successfully" in captured.out

    # Verify file content
    updated_content = test_file.read_text().splitlines()
    assert "* lsqr" not in updated_content
    assert "lsqr_param1" not in updated_content
    assert "* model" in updated_content
    assert "model_data" in updated_content


def test_rmv_lsqr_no_section(tmp_path, capsys):
    """Test handling when no LSQR section exists"""
    # Create test file without LSQR
    test_file = tmp_path / "test.pst"
    content = [
        "* control\n",
        "* model\n",
        "model_data\n"
    ]
    test_file.write_text("".join(content))

    # Run function
    rmv_lsqr(str(test_file))

    # Verify output
    captured = capsys.readouterr()
    assert "No LSQR section found" in captured.out

    # Verify file remains unchanged
    assert test_file.read_text() == "".join(content)


def test_rmv_lsqr_case_insensitivity(tmp_path, capsys):
    """Test case-insensitive section detection"""
    test_file = tmp_path / "test.pst"
    content = [
        "* CONTROL\n",
        "* LSQR\n",
        "parameters\n",
        "* MODEL\n"
    ]
    test_file.write_text("".join(content))

    rmv_lsqr(str(test_file))

    updated_content = test_file.read_text()
    assert "* LSQR" not in updated_content
    assert "* MODEL" in updated_content


def test_rmv_lsqr_file_not_found(capsys):
    """Test handling of missing file"""
    rmv_lsqr("non_existent_file.pst")
    captured = capsys.readouterr()
    assert "Error: File not found" in captured.out


def test_rmv_lsqr_section_at_end(tmp_path, capsys):
    """Test LSQR section at end of file"""
    test_file = tmp_path / "test.pst"
    content = [
        "* control\n",
        "* lsqr\n",
        "param1\n",
        "param2\n"  # No following section
    ]
    test_file.write_text("".join(content))

    rmv_lsqr(str(test_file))

    updated_content = test_file.read_text().splitlines()
    assert len(updated_content) == 1  # Only "* control" remains
    assert "* control" in updated_content[0]


def test_rmv_svd_no_section(tmp_path, capsys):
    """Test handling when no SVD section exists"""
    # Create test file without SVD
    test_file = tmp_path / "test.pst"
    content = [
        "* control data\n",
        "* model\n",
        "model_data\n"
    ]
    test_file.write_text("".join(content))

    # Run function
    rmv_svd(str(test_file))

    # Verify output
    captured = capsys.readouterr()
    assert "No SVD (singular value decomposition) section found to remove" in captured.out

    # Verify file remains unchanged
    assert test_file.read_text() == "".join(content)


def test_rmv_svd_case_insensitivity(tmp_path):
    """Test case-insensitive section detection"""
    test_file = tmp_path / "test.pst"
    content = [
        "* CONTROL DATA\n",
        "* SINGULAR VALUE DECOMPOSITION\n",
        "parameters\n",
        "* MODEL\n"
    ]
    test_file.write_text("".join(content))

    rmv_svd(str(test_file))
    updated_content = test_file.read_text()
    assert "* SINGULAR VALUE DECOMPOSITION" not in updated_content
    assert "* MODEL" in updated_content


def test_rmv_svd_file_not_found(capsys):
    """Test handling of missing file"""
    rmv_svd("non_existent_file.pst")
    captured = capsys.readouterr()
    assert "Error: File not found" in captured.out


def test_rmv_svd_section_at_end(tmp_path, capsys):
    """Test SVD section at end of file"""
    test_file = tmp_path / "test.pst"
    content = [
        "* control data\n",
        "* singular value decomposition\n",
        "param1\n",
        "param2\n"  # No following section
    ]
    test_file.write_text("".join(content))

    rmv_svd(str(test_file))

    updated_content = test_file.read_text().splitlines()
    assert len(updated_content) == 1  # Only control data remains
    assert "* control data" in updated_content[0]


def test_rmv_svd_malformed_section(tmp_path, capsys):
    """Test malformed SVD section without closing"""
    test_file = tmp_path / "test.pst"
    content = [
        "* control data\n",
        "* singular value decomposition\n",
        "malformed_param\n",
        "another_line\n"
    ]
    test_file.write_text("".join(content))

    rmv_svd(str(test_file))

    updated_content = test_file.read_text().splitlines()
    assert "* control data" in updated_content[0]
    assert len(updated_content) == 1  # All SVD-related lines removed


def test_rmv_svd_successful_removal(tmp_path, capsys):
    """Test removal of existing SVD section"""
    # Create test file with SVD section
    test_file = tmp_path / "test.pst"
    content = [
        "* control data\n",
        "dummy line\n",
        "* singular value decomposition\n",
        "svd_param1 1.0\n",
        "svd_param2 2.0\n",
        "* model\n",
        "model_data\n"
    ]
    test_file.write_text("".join(content))

    # Run function
    rmv_svd(str(test_file))

    # Verify output
    captured = capsys.readouterr()
    assert "SVD (singular value decomposition) section removed successfully" in captured.out

    # Verify file content
    updated_content = test_file.read_text().splitlines()
    assert "* singular value decomposition" not in updated_content
    assert "svd_param1" not in updated_content
    assert "* model" in updated_content
    assert "model_data" in updated_content  # Will now pass after typo fix