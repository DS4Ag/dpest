def phiredswh(pst_path, new_value):
    """
    Updates the PHIREDSWH parameter in a PEST control (.pst) file.

    PHIREDSWH sets the objective function change threshold for switching to central derivatives.
    This function allows you to set PHIREDSWH to any float value between 0.0 and 1.0.

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the .pst file to modify
        * **new_value** (*float*):
            New value for PHIREDSWH (must be between 0.0 and 1.0)

    **Returns:**
    =======
        * ``None``

    **Example:**
    =======

    **Set PHIREDSWH to 0.1:**

        .. code-block:: python

            from dpest.utils import phiredswh

            phiredswh("PEST_CONTROL.pst", 0.1)
    """
    try:
        # Validate input
        phiredswh = float(new_value)
        if not (0.0 <= phiredswh <= 1.0):
            raise ValueError("PHIREDSWH must be between 0.0 and 1.0 (inclusive)")

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # PHIREDSWH is the 1st value on line 8 (index 7)
        target_line_idx = 7
        if target_line_idx >= len(lines):
            raise IndexError(f"File has only {len(lines)} lines. Expected control data at line {target_line_idx+1}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if not values:
            raise ValueError("PHIREDSWH line is empty in the control file.")

        # Replace first value (PHIREDSWH)
        values[0] = f"{phiredswh:.6E}"  # Scientific notation

        # Rebuild line with original formatting
        current_padding = len(current_line) - len(current_line.lstrip())
        new_line = " " * current_padding + "   ".join(values) + "\n"

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