def noptmax(pst_path, new_value=0):
    """
    Updates the NOPTMAX parameter in a PEST control (.pst) file.

    The NOPTMAX parameter specifies the number of optimization iterations or model runs that PEST will perform.
    This function allows you to set NOPTMAX to any integer value, such as 0 (run the model once, no optimization)
    or a large value for iterative optimization.

    **Required Arguments:**
    =======

        * **pst_file_path** (*str*): 
            Path to the ``.pst`` PEST control file whose NOPTMAX value you wish to update.

    **Optional Arguments:**
    =======

        * **new_value** (*int*, *default: 0*): 
            The new value for the NOPTMAX parameter. 
            For example, use ``0`` to run the model once, or ``10000`` for iterative calibration.

    **Returns:**
    =======

        * ``None``

    **Examples:**
    =======

    1. **Set NOPTMAX to 0 (single run):**

       .. code-block:: python

          from dpest.utils import noptmax

          pst_file_path = 'PEST_CONTROL.pst'
          noptmax(pst_file_path)

    2. **Set NOPTMAX to 50 (iterative optimization):**

       .. code-block:: python

          from dpest.utils import noptmax

          pst_file_path = './ENTRY1/PEST_CONTROL.pst'
          noptmax(pst_file_path, new_value = 50)
    """
    try:
        # Validation for NOPTMAX value
        if not isinstance(new_value, int):
            raise ValueError(f"NOPTMAX must be an integer. Got: {new_value}")
        if new_value not in [-2, -1, 0] and new_value <= 0:
            raise ValueError("NOPTMAX must be -2, -1, 0, or any integer greater than zero.")

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # NOPTMAX is on line 9 (index 8) in standard PEST control files
        target_line_idx = 8
        if target_line_idx >= len(lines):
            raise IndexError(f"Expected at least {target_line_idx + 1} lines in the file, but got {len(lines)}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if not values:
            raise ValueError("NOPTMAX line not found or is empty in the control file.")

        # Replace first value with new_value, preserving alignment
        current_padding = len(current_line) - len(current_line.lstrip())
        formatted_value = f"{new_value:d}"

        # Reconstruct the line, preserving the rest of the values
        new_line = " " * current_padding + formatted_value + "   " + "   ".join(values[1:]) + "\n"
        lines[target_line_idx] = new_line

        with open(pst_path, 'w') as f:
            f.writelines(lines)

    except FileNotFoundError:
        print(f"Error: The file '{pst_path}' was not found.")
    except IndexError as ie:
        print(f"IndexError: {ie}")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")