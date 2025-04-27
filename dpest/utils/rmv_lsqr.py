def rmv_lsqr(pst_path):
    """
    Removes the LSQR section from a PEST control (.pst) file.

    The LSQR section is optional in a PEST control file. This function will remove it if present,
    and inform the user whether the section was found and removed or did not exist.

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the .pst PEST control file to modify.

    **Returns:**
    =======
        * ``None``

    **Examples:**
    =======

    1. **Removing the LSQR Section from a PEST Control File:**

       .. code-block:: python

          from dpest.utils import rmv_lsqr

          rmv_lsqr(
              pst_path = "PEST_CONTROL.pst"
          )

       This example removes the LSQR section if it exists. If the section is not found,
       the function will notify the user that no LSQR section was present to remove.
    """
    try:
        import os

        if not os.path.isfile(pst_path):
            print(f"Error: File not found: {pst_path}")
            return

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        in_lsqr = False
        lsqr_found = False

        for line in lines:
            if line.strip().lower().startswith('* lsqr'):
                in_lsqr = True
                lsqr_found = True
                continue
            if in_lsqr:
                if line.strip().startswith('*'):
                    in_lsqr = False
                    new_lines.append(line)
                continue
            new_lines.append(line)

        if lsqr_found:
            with open(pst_path, 'w') as f:
                f.writelines(new_lines)
            print(f"LSQR section removed successfully from {pst_path}")
        else:
            print("No LSQR section found to remove.")

    except Exception as e:
        print(f"Unexpected error while removing LSQR section: {str(e)}")
