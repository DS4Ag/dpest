def phiredlam(pst_path, new_value):
    """
    Updates the PHIREDLAM parameter in a PEST control (.pst) file.

    PHIREDLAM is the relative objective function reduction threshold for trying a new Marquardt lambda.
    This function allows you to set PHIREDLAM to any float value between 0.0 and 1.0 (e.g., 0.03, 0.01).

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the ``.pst`` PEST control file whose PHIREDLAM value you wish to update.
        * **new_value** (*float*):
            The new value for the PHIREDLAM parameter (must be between 0.0 and 1.0).

    **Returns:**
    =======
        * ``None``

    **Example:**
    =======

    **Set PHIREDLAM to 0.03:**
    
       .. code-block:: python

          from dpest.utils import phiredlam

          pst_file_path = 'PEST_CONTROL.pst'
          phiredlam(pst_file_path, 0.03)
    """
    try:
        # Validate input
        phiredlam = float(new_value)
        if not (0.0 <= phiredlam <= 1.0):
            raise ValueError("PHIREDLAM must be between 0.0 and 1.0 (inclusive)")

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # PHIREDLAM is the 4th value on the RLAMBDA1 line (typically line 6, index 5)
        target_line_idx = 5
        if target_line_idx >= len(lines):
            raise IndexError(f"File has only {len(lines)} lines. Expected control data at line {target_line_idx+1}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if len(values) < 4:
            raise ValueError(f"PHIREDLAM position not found. Line only has {len(values)} values.")

        # Format and replace value
        values[3] = f"{phiredlam:.6E}"  # Scientific notation

        # Reconstruct line with original formatting
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