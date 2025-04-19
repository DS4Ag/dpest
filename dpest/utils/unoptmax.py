def unoptmax(pst_path, new_value=0):
    """
    Updates the NOPTMAX parameter in a PEST control (.pst) file.

    The NOPTMAX parameter specifies the number of optimization iterations or model runs that PEST will perform.
    This function allows you to set NOPTMAX to any integer value, such as 0 (run the model once, no optimization)
    or a large value for iterative optimization. The rest of the control file, including solver settings (e.g., LSQR),
    is preserved.

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

          from dpest.utils import unoptmax

          pst_file_path = 'PEST_CONTROL.pst'
          unoptmax(pst_file_path)

    2. **Set NOPTMAX to 10000 (iterative optimization):**

       .. code-block:: python

          from dpest.utils import unoptmax

          pst_file_path = './ENTRY1/PEST_CONTROL.pst'
          unoptmax(pst_file_path, new_value = 10000)
    """
    with open(pst_path, 'r') as f:
        lines = f.readlines()

    # NOPTMAX is on line 9 (index 8) in standard PEST control files
    target_line_idx = 8
    current_line = lines[target_line_idx]

    # Split the line by whitespace to get all values
    values = current_line.split()

    # Replace first value with new_value, preserving alignment
    # Calculate padding based on current value's width
    current_padding = len(current_line) - len(current_line.lstrip())
    formatted_value = f"{new_value:4d}"  # Right-aligned in 4 spaces

    # Reconstruct the line, preserving the rest of the values
    new_line = " " * current_padding + formatted_value + "   " + "   ".join(values[1:]) + "\n"

    lines[target_line_idx] = new_line

    with open(pst_path, 'w') as f:
        f.writelines(lines)