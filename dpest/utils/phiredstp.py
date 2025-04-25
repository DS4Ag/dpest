def phiredstp(pst_path, new_value):
    """
    Updates the PHIREDSTP parameter in a PEST control (.pst) file.

    PHIREDSTP specifies the relative objective function reduction threshold for optimization termination.
    This function allows you to set PHIREDSTP to any positive float value.

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the .pst file to modify
        * **new_value** (*float*):
            New value for PHIREDSTP (must be greater than 0.0)

    **Returns:**
    =======
        * ``None``

    **Example:**
    =======

    **Set PHIREDSTP to 0.01:**

        .. code-block:: python

            from dpest.utils import phiredstp

            phiredstp("PEST_CONTROL.pst", 0.01)
    """
    try:
        # Validate input
        phiredstp = float(new_value)
        if phiredstp <= 0.0:
            raise ValueError("PHIREDSTP must be greater than zero")

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # PHIREDSTP is the 2nd value on line 9 (index 8)
        target_line_idx = 8
        if target_line_idx >= len(lines):
            raise IndexError(f"File has only {len(lines)} lines. Expected control data at line {target_line_idx+1}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if len(values) < 2:
            raise ValueError("PHIREDSTP position not found in control data line")

        # Replace second value (PHIREDSTP)
        values[1] = f"{phiredstp:.6E}"  # Scientific notation

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