def nphinored(pst_path, new_value):
    """
    Updates the NPHINORED parameter in a PEST control (.pst) file.

    NPHINORED specifies the number of iterations without objective function reduction
    to trigger optimization termination. This function allows you to set NPHINORED
    to any integer value greater than zero.

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the .pst file to modify
        * **new_value** (*int*):
            New value for NPHINORED (must be an integer > 0)

    **Returns:**
    =======
        * ``None``

    **Example:**
    =======

    **Set NPHINORED to 5:**
    
        .. code-block:: python

            from dpest.utils import nphinored

            nphinored("PEST_CONTROL.pst", 5)
    """
    try:
        # Validate input
        if not isinstance(new_value, int):
            raise ValueError("NPHINORED must be an integer")
        if new_value <= 0:
            raise ValueError("NPHINORED must be greater than zero")

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # NPHINORED is the 4th value on line 9 (index 8)
        target_line_idx = 8
        if target_line_idx >= len(lines):
            raise IndexError(f"File has only {len(lines)} lines. Expected control data at line {target_line_idx + 1}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if len(values) < 4:
            raise ValueError("NPHINORED position not found in control data line")

        # Replace fourth value (NPHINORED)
        values[3] = f"{new_value}"

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