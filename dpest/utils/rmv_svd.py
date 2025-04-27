def rmv_svd(pst_path):
    """
    Removes the SVD (singular value decomposition) section from a PEST control (.pst) file.

    The SVD section is optional in a PEST control file. This function will remove it if present,
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

    1. **Removing the SVD section from a PEST Control File:**

       .. code-block:: python

          from dpest.utils import rmv_svd

          rmv_svd(
              pst_path = "PEST_CONTROL.pst"
          )

       This example removes the SVD section if it exists. If the section is not found,
       the function will notify the user that no SVD section was present to remove.
    """
    try:
        import os

        if not os.path.isfile(pst_path):
            print(f"Error: File not found: {pst_path}")
            return

        with open(pst_path, 'r') as f:
            lines = f.readlines()

        new_lines = []
        in_svd = False
        svd_found = False

        for line in lines:
            if line.strip().lower().startswith('* singular value decomposition'):
                in_svd = True
                svd_found = True
                continue
            if in_svd:
                if line.strip().startswith('*'):
                    in_lsqr = False
                    new_lines.append(line)
                continue
            new_lines.append(line)

        if svd_found:
            with open(pst_path, 'w') as f:
                f.writelines(new_lines)
            print(f"SVD (singular value decomposition) section removed successfully from {pst_path}")
        else:
            print("No SVD (singular value decomposition) section found to remove.")

    except Exception as e:
        print(f"Unexpected error while removing SVD (singular value decomposition) section: {str(e)}")