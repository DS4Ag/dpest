def phiratsuf(pst_path, new_value):
    """
    Updates the PHIRATSUF parameter in a PEST control (.pst) file.

    PHIRATSUF specifies the objective function reduction ratio threshold for accepting
    a lambda adjustment during optimization. This function allows you to set PHIRATSUF
    to any float value between 0 and 1 (e.g., 0.3, 0.5, 1.0).

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the .pst file to modify
        * **new_value** (*float*):
            New value for PHIRATSUF (must be between 0.0 and 1.0)

    **Returns:**
    =======
        * ``None``

    **Example:**
    =======

    **Set PHIRATSUF to 0.3**

        .. code-block:: python

            from dpest.utils import phiratsuf

            phiratsuf("PEST_CONTROL.pst", 0.3)
    """
    try:
        # Convert to float and validate range
        phiratsuf = float(new_value)
        if not (0.0 <= phiratsuf <= 1.0):
            raise ValueError("PHIRATSUF must be between 0.0 and 1.0 (inclusive)")

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # PHIRATSUF is the 3rd value on line 5 (index 5)
        target_line_idx = 5
        if target_line_idx >= len(lines):
            raise IndexError(f"File has only {len(lines)} lines. Expected control data at line {target_line_idx+1}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if len(values) < 3:
            raise ValueError(f"PHIRATSUF position not found. Line only has {len(values)} values.")

        # Replace PHIRATSUF (3rd value) with new value
        values[2] = f"{phiratsuf:.6E}"  # Scientific notation

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