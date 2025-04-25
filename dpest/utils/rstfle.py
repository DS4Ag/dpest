def rstfle(pst_path, new_value):
    """
    Updates the RSTFLE parameter in a PEST control (.pst) file.

    The RSTFLE parameter instructs PEST whether to write restart data. It should be set to "restart" or "norestart".
    This function allows you to set RSTFLE to either value.

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the ``.pst`` PEST control file whose RSTFLE value you wish to update.
        * **new_value** (*str*):
            The new value for the RSTFLE parameter ("restart" or "norestart").

    **Returns:**
    =======
        * ``None``

    **Examples:**
    =======

    1. **Set RSTFLE to "restart":**

       .. code-block:: python

          from dpest.utils import rstfle

          pst_file_path = 'PEST_CONTROL.pst'
          rstfle(pst_file_path, "restart")

    2. **Set RSTFLE to "norestart":**

       .. code-block:: python

          from dpest.utils import rstfle

          pst_file_path = './ENTRY1/PEST_CONTROL.pst'
          rstfle(pst_file_path, "norestart")

    """
    allowed = {"restart", "norestart"}
    try:
        # Validate the RSTFLE value
        if not isinstance(new_value, str):
            raise ValueError("RSTFLE must be a string.")
        if new_value.lower() not in allowed:
            raise ValueError(
                f"RSTFLE must be either 'restart' or 'norestart' (case-insensitive). Got: '{new_value}'"
            )

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # RSTFLE is on line 2 (index 1) in standard PEST control files
        target_line_idx = 2
        if target_line_idx >= len(lines):
            raise IndexError(f"Expected at least {target_line_idx + 1} lines in the file, but got {len(lines)}.")

        current_line = lines[target_line_idx]
        values = current_line.split()

        if not values:
            raise ValueError("RSTFLE line not found or is empty in the control file.")

        # Replace first value with new_value, preserving alignment
        current_padding = len(current_line) - len(current_line.lstrip())
        formatted_value = new_value.lower()

        # Reconstruct the line, preserving the rest of the values
        new_line = " " * current_padding + formatted_value + " " + " ".join(values[1:]) + "\n"
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