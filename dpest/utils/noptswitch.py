def noptswitch(pst_path, new_value=1):
    """
    Updates the NOPTSWITCH parameter in a PEST control (.pst) file.

    The NOPTSWITCH parameter determines the iteration before which PEST will not switch to
    central derivatives computation. This function allows you to set NOPTSWITCH to any integer
    value greater than or equal to 1.

    **Required Arguments:**
    =======

        * **pst_path** (*str*):
            Path to the ``.pst`` PEST control file whose NOPTSWITCH value you wish to update.

    **Optional Arguments:**
    =======

        * **new_value** (*int*, *default: 1*):
            The new value for the NOPTSWITCH parameter. Must be an integer greater than or equal to 1.

    **Returns:**
    =======

        * ``None``

    **Examples:**
    =======

    1. **Set NOPTSWITCH to 3 (delay central derivatives until 3rd iteration):**

       .. code-block:: python

          from dpest.utils import noptswitch

          pst_file_path = 'PEST_CONTROL.pst'
          noptswitch(pst_file_path, 3)
    """
    try:
        # Validation for NOPTSWITCH value
        if not isinstance(new_value, int) or new_value < 1:
            raise ValueError("NOPTSWITCH must be an integer greater than or equal to 1.")

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # PHIREDSWH and NOPTSWITCH are on line 8 (index 7) in standard PEST control files
        target_line_idx = 7  # Corrected from 6 to 7
        if target_line_idx >= len(lines):
            raise IndexError(f"Expected at least {target_line_idx + 1} lines in the file, but got {len(lines)}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if not values:
            raise ValueError("PHIREDSWH/NOPTSWITCH line not found or is empty in the control file.")

        # If only PHIREDSWH is present, append NOPTSWITCH
        if len(values) == 1:
            values.append(str(new_value))
        else:
            values[1] = str(new_value)

        # Preserve original spacing
        current_padding = len(current_line) - len(current_line.lstrip())
        new_line = " " * current_padding + "   ".join(values) + "\n"
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