def rlambda1(pst_path, new_value):
    """
    Updates the RLAMBDA1 parameter in a PEST control (.pst) file.

    The RLAMBDA1 parameter specifies the initial Marquardt lambda value for the optimization process.
    This function allows you to set RLAMBDA1 to any non-negative float value (e.g., 10.0, 1.0, 0.01).

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the ``.pst`` PEST control file whose RLAMBDA1 value you wish to update.
        * **new_value** (*float*):
            The new value for the RLAMBDA1 parameter (must be ≥ 0).

    **Returns:**
    =======
        * ``None``

    **Example:**
    =======
    
    **Set RLAMBDA1 to 5.0:**

       .. code-block:: python

          from dpest.utils import rlambda1

          pst_file_path = 'PEST_CONTROL.pst'
          rlambda1(pst_file_path, 5.0)
    """
    try:
        # Validate input
        rlambda1 = float(new_value)
        if rlambda1 < 0:
            raise ValueError("RLAMBDA1 must be zero or greater")

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # RLAMBDA1 is typically on line 6 (index 5)
        target_line_idx = 5
        if target_line_idx >= len(lines):
            raise IndexError(f"File has only {len(lines)} lines. Expected control data at line {target_line_idx+1}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if not values:
            raise ValueError("RLAMBDA1 line is empty in the control file.")

        # Replace first value with new_value, preserving alignment
        current_padding = len(current_line) - len(current_line.lstrip())
        formatted_value = f"{rlambda1:.6E}"  # Scientific notation

        # Reconstruct the line
        new_line = " " * current_padding + formatted_value + "   " + "   ".join(values[1:]) + "\n"
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