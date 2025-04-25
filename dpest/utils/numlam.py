def numlam(pst_path, new_value):
    """
    Updates the NUMLAM parameter in a PEST control (.pst) file.

    NUMLAM specifies the maximum number of Marquardt lambda values that PEST will try during each iteration.
    This function allows you to set NUMLAM to any integer value (e.g., 10, 5, -1). Valid values are:
    - ≥1 (standard PEST)
    - <0 (for Parallel PEST or BEOPEST)
    Zero is not allowed.

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the ``.pst`` PEST control file whose NUMLAM value you wish to update.
        * **new_value** (*int*):
            The new value for the NUMLAM parameter.

    **Returns:**
    =======
        * ``None``

    **Example:**
    =======

    **Set NUMLAM to 10:**
    
       .. code-block:: python

          from dpest.utils import numlam

          pst_file_path = 'PEST_CONTROL.pst'
          numlam(pst_file_path, 10)

    """
    try:
        # Validate input
        if not isinstance(new_value, int):
            raise ValueError(f"NUMLAM must be an integer. Got: {type(new_value)}")
        if new_value == 0:
            raise ValueError("NUMLAM cannot be zero. Use ≥1 (standard) or <0 (Parallel/BEOPEST).")

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # NUMLAM is the 5th value on the RLAMBDA1 line (typically line 6, index 5)
        target_line_idx = 5
        if target_line_idx >= len(lines):
            raise IndexError(f"File has only {len(lines)} lines. Expected control data at line {target_line_idx + 1}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if len(values) < 5:
            raise ValueError(f"NUMLAM position not found. Line only has {len(values)} values.")

        # Format and replace
        values[4] = f"{new_value}"
        current_padding = len(current_line) - len(current_line.lstrip())
        new_line = " " * current_padding + " ".join(values) + "\n"
        lines[target_line_idx] = new_line

        with open(pst_path, 'w') as f:
            f.writelines(lines)

    except FileNotFoundError:
        print(f"Error: File '{pst_path}' not found.")
    except IndexError as e:
        print(f"IndexError: {str(e)}")
    except ValueError as e:
        print(f"ValueError: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")