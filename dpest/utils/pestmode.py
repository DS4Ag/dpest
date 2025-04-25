def pestmode(pst_path, new_value):
    """
    Updates the PESTMODE parameter in a PEST control (.pst) file.

    The PESTMODE parameter specifies PEST's mode of operation.
    Allowed values: "estimation", "prediction", "regularisation", "pareto" (case-insensitive).
    The rest of the control file is preserved.

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the .pst file to modify
        * **new_value** (*str*):
            New value for PESTMODE (must be one of the allowed modes)

    **Returns:**
    =======
        * ``None``

    **Example:**
    =======

    **Set PESTMODE to "prediction"**

    .. code-block:: python

        from dpest.utils import pestmode

        pestmode("PEST_CONTROL.pst", "prediction")
    """
    allowed_modes = {"estimation", "prediction", "regularisation", "pareto"}
    try:
        # Validate input
        if not isinstance(new_value, str):
            raise ValueError("PESTMODE must be a string.")
        pestmode = new_value.strip().lower()
        if pestmode not in allowed_modes:
            raise ValueError(
                f"PESTMODE must be one of {allowed_modes} (case-insensitive). Got: '{new_value}'"
            )

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # PESTMODE is the 2nd value on line 2 (index 1)
        target_line_idx = 2
        if target_line_idx >= len(lines):
            raise IndexError(f"File has only {len(lines)} lines. Expected control data at line {target_line_idx+1}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if len(values) < 2:
            raise ValueError("PESTMODE value not found in the expected position in the control file.")

        # Replace the second value (PESTMODE)
        values[1] = pestmode

        # Reconstruct the line, preserving alignment
        current_padding = len(current_line) - len(current_line.lstrip())
        new_line = " " * current_padding + " ".join(values) + "\n"

        lines[target_line_idx] = new_line

        with open(pst_path, 'w') as f:
            f.writelines(lines)

    except FileNotFoundError:
        print(f"Error: File '{pst_path}' not found.")
    except ValueError as ve:
        print(f"ValueError: {str(ve)}")
    except IndexError as ie:
        print(f"IndexError: {str(ie)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")