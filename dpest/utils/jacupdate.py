def jacupdate(pst_path, new_value):
    """
    Updates the JACUPDATE parameter in a PEST control (.pst) file.

    JACUPDATE is an optional control variable that appears on the line:

        RLAMBDA1 RLAMFAC PHIRATSUF PHIREDLAM NUMLAM [JACUPDATE] [LAMFORGIVE] [DERFORGIVE]

    within the ``* control data`` section of the PEST control file.

    This function:
    - locates the ``* control data`` section,
    - finds the RLAMBDA1/RLAMFAC/PHIRATSUF/PHIREDLAM/NUMLAM line,
    - updates ``JACUPDATE`` if it already exists,
    - or appends ``JACUPDATE`` if it is not yet present.

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the .pst file to modify.
        * **new_value** (*int*):
            New value for JACUPDATE.

    **Returns:**
    =======
        * ``None``

    **Notes:**
    =======
        According to the PEST control-data layout, JACUPDATE is an optional
        variable on the control-data line:

        RLAMBDA1 RLAMFAC PHIRATSUF PHIREDLAM NUMLAM [JACUPDATE] [LAMFORGIVE] [DERFORGIVE]

        Since it is optional, some .pst files may contain only the first
        five required values on this line. In that case, this function
        appends JACUPDATE as the sixth value.

    **Example:**
    =======

     **Set JACUPDATE to 999:**

        .. code-block:: python

            from dpest.utils import jacupdate

            jacupdate("PEST_CONTROL.pst", 999)
    """
    try:
        # Validate input
        jacupdate_value = int(new_value)

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # Find the "* control data" section
        control_idx = None
        for i, line in enumerate(lines):
            if line.strip().lower() == "* control data":
                control_idx = i
                break

        if control_idx is None:
            raise ValueError("'* control data' section not found in the .pst file.")

        # Collect non-empty, non-comment lines after "* control data"
        # The 4th control-data line is:
        # RLAMBDA1 RLAMFAC PHIRATSUF PHIREDLAM NUMLAM [JACUPDATE] [LAMFORGIVE] [DERFORGIVE]
        nonempty_count = 0
        target_line_idx = None

        for i in range(control_idx + 1, len(lines)):
            stripped = lines[i].strip()

            # Stop if next section starts
            if stripped.startswith("*"):
                break

            # Skip blank lines
            if not stripped:
                continue

            nonempty_count += 1

            if nonempty_count == 4:
                target_line_idx = i
                break

        if target_line_idx is None:
            raise ValueError(
                "Could not find the RLAMBDA1/RLAMFAC/PHIRATSUF/PHIREDLAM/NUMLAM control-data line."
            )

        current_line = lines[target_line_idx]
        values = current_line.split()

        if len(values) < 5:
            raise ValueError(
                "Target control-data line has fewer than 5 required values. "
                "Could not identify JACUPDATE position safely."
            )

        # If JACUPDATE already exists, replace it.
        # Otherwise append it as the 6th value.
        if len(values) >= 6:
            values[5] = str(jacupdate_value)
        else:
            values.append(str(jacupdate_value))

        # Rebuild line preserving left padding
        current_padding = len(current_line) - len(current_line.lstrip())
        new_line = " " * current_padding + "   ".join(values) + "\n"

        lines[target_line_idx] = new_line

        with open(pst_path, 'w') as f:
            f.writelines(lines)

    except FileNotFoundError:
        print(f"Error: File '{pst_path}' not found.")
    except ValueError as ve:
        print(f"ValueError: {str(ve)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")