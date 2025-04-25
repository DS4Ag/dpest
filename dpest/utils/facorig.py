def facorig(pst_path, new_value):
    """
    Updates the FACORIG parameter in a PEST control (.pst) file.

    FACORIG specifies the minimum fraction of the original parameter value that can be used during optimization.
    This function allows you to set FACORIG to any float value between 0.0 and 1.0 (inclusive).

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the .pst file to modify
        * **new_value** (*float*):
            New value for FACORIG (must be between 0.0 and 1.0)

    **Returns:**
    =======
        * ``None``

    **Example:**
    =======

     **Set FACORIG to 01:**

        .. code-block:: python

            from dpest.utils import facorig

            facorig("PEST_CONTROL.pst", 0.1)
    """
    try:
        # Validate input
        facorig = float(new_value)
        if not (0.0 <= facorig <= 1.0):
            raise ValueError("FACORIG must be between 0.0 and 1.0 (inclusive)")

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # FACORIG is the 3rd value on line 7 (index 6)
        target_line_idx = 6
        if target_line_idx >= len(lines):
            raise IndexError(f"File has only {len(lines)} lines. Expected control data at line {target_line_idx+1}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if len(values) < 3:
            raise ValueError("FACORIG position not found in control data line")

        # Replace third value (FACORIG)
        values[2] = f"{facorig:.6E}"  # Scientific notation

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