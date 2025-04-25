def rmv_splitcols(pst_path):
    """
    Removes SPLITTHRESH/SPLITRELDIFF/SPLITACTION columns from * parameter groups section,
    overwriting the original file by default.

    **Arguments:**
    =======
    * **pst_path** (*str*): Path to existing PST file

    **Returns:**
    =======

        * ``None``

    **Example:**
    =======

    code-block:: python

        from dpest.utils import phiratsuf

        rmv_splitcols("PEST_CONTROL.pst")
    """
    # Map column names to their 0-based indices in PEST's parameter groups section
    COLUMN_MAP = {

        "PARGPNME": 0,
        "INCTYP": 1,
        "DERINC": 2,
        "DERINCLB": 3,
        "FORCEN": 4,
        "DERINCMUL": 5,
        "DERMTHD": 6,
        "SPLITTHRESH": 7,
        "SPLITRELDIFF": 8,
        "SPLITACTION": 9
    }

    # Columns to remove by name
    COLS_TO_REMOVE = ["SPLITTHRESH", "SPLITRELDIFF", "SPLITACTION"]

    with open(pst_path, 'r') as f:
        lines = f.readlines()

    in_param_groups = False
    new_lines = []

    for line in lines:
        if line.strip().startswith("* parameter groups"):
            in_param_groups = True
            new_lines.append(line)
            continue

        if in_param_groups:
            if line.strip().startswith("*"):  # Next section
                in_param_groups = False
            else:
                # Split line and remove target columns by name->index mapping
                fields = line.split()
                # Keep only fields NOT in COLS_TO_REMOVE
                cleaned_fields = [
                    field for idx, field in enumerate(fields)
                    if idx not in [COLUMN_MAP[col] for col in COLS_TO_REMOVE]
                ]
                line = "  ".join(cleaned_fields) + "\n"

        new_lines.append(line)

    with open(pst_path, 'w') as f:
        f.writelines(new_lines)