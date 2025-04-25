def relparstp(pst_path, new_value):
    """
    Updates the RELPARSTP parameter in a PEST control (.pst) file.

    RELPARSTP specifies the maximum relative parameter change threshold for
    optimization termination. This function allows you to set RELPARSTP to
    any positive float value.

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the .pst file to modify
        * **new_value** (*float*):
            New value for RELPARSTP (must be > 0.0)

    **Returns:**
    =======
        * ``None``

    **Example:**
    =======

    **Set RELPARSTP to 0.01:**

        .. code-block:: python

            from dpest.utils import relparstp

            relparstp("PEST_CONTROL.pst", 0.01)
    """
    try:
        # Validate input
        relparstp = float(new_value)
        if relparstp <= 0.0:
            raise ValueError("RELPARSTP must be greater than zero")

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # RELPARSTP is the 5th value on line 9 (index 8)
        target_line_idx = 8
        if target_line_idx >= len(lines):
            raise IndexError(f"File has only {len(lines)} lines. Expected control data at line {target_line_idx + 1}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if len(values) < 5:
            raise ValueError("RELPARSTP position not found in control data line")

        # Replace fifth value (RELPARSTP at index 4)
        values[4] = f"{relparstp:.6E}"  # Scientific notation

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