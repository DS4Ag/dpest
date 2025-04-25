def facparmax(pst_path, new_value):
    """
    Updates the FACPARMAX parameter in a PEST control (.pst) file.

    FACPARMAX specifies the maximum factor by which parameters can change during optimization.
    This function allows you to set FACPARMAX to any float value greater than 1.0.

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the .pst file to modify
        * **new_value** (*float*):
            New value for FACPARMAX (must be greater than 1.0)

    **Returns:**
    =======
        * ``None``

    **Example:**
    =======

    **Set FACPARMAX  to 2.0:**

        .. code-block:: python

             from dpest.utils import facparmax

            facparmax("PEST_CONTROL.pst", 2.0)
    """
    try:
        # Validate input
        facparmax = float(new_value)
        if facparmax <= 1.0:
            raise ValueError("FACPARMAX must be greater than 1.0")

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # FACPARMAX is the 2nd value on line 7 (index 6)
        target_line_idx = 6
        if target_line_idx >= len(lines):
            raise IndexError(f"File has only {len(lines)} lines. Expected control data at line {target_line_idx+1}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if len(values) < 2:
            raise ValueError("FACPARMAX position not found in control data line")

        # Replace second value (FACPARMAX)
        values[1] = f"{facparmax:.6E}"  # Scientific notation

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