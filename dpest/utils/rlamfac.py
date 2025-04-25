def rlamfac(pst_path, new_value):
    """
    Updates the RLAMFAC parameter in a PEST control (.pst) file.

    The RLAMFAC parameter is the factor by which the Marquardt lambda is adjusted during optimization.
    This function allows you to set RLAMFAC to any float value (positive or negative, but not zero).

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the ``.pst`` PEST control file whose RLAMFAC value you wish to update.
        * **new_value** (*float*):
            The new value for the RLAMFAC parameter.

    **Returns:**
    =======
        * ``None``

    **Example:**
    =======
    
    **Set RLAMFAC to 2.0:**

       .. code-block:: python

          from dpest.utils import rlamfac

          pst_file_path = 'PEST_CONTROL.pst'
          rlamfac(pst_file_path, 2.0)

    """
    try:
        # Validate input
        rlamfac = float(new_value)
        if rlamfac == 0.0:
            raise ValueError("RLAMFAC must not be zero (can be positive or negative, but not zero).")

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # RLAMFAC is the 2nd value on the RLAMBDA1 line (typically line 6, index 5)
        target_line_idx = 5
        if target_line_idx >= len(lines):
            raise IndexError(f"File has only {len(lines)} lines. Expected control data at line {target_line_idx+1}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if len(values) < 2:
            raise ValueError("RLAMFAC value not found in the expected position in the control file.")

        # Format the new RLAMFAC value in scientific notation
        formatted_value = f"{rlamfac:.6E}"

        # Replace the second value (RLAMFAC)
        values[1] = formatted_value

        # Reconstruct the line, preserving alignment
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