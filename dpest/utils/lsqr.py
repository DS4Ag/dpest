def lsqr(pst_path, lsqrmode=None, lsqr_atol=None, lsqr_btol=None,
          lsqr_conlim=None, lsqr_itnlim=None, lsqrwrite=None):
    """
    Adds or updates the LSQR section in a PEST control (.pst) file.

    The LSQR section configures PEST to use the LSQR algorithm for solving the inverse problem.
    This is especially useful for large models with many parameters.

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the .pst PEST control file to modify.

    **Optional Arguments:**
    =======
        * **lsqrmode** (*int*):
            LSQR mode (must be 0 or 1).
            Default is 1 (enable LSQR).
        * **lsqr_atol** (*float*):
            LSQR algorithm atol variable (must be ≥ 0).
            Default is 1e-4.
        * **lsqr_btol** (*float*):
            LSQR algorithm btol variable (must be ≥ 0).
            Default is 1e-4.
        * **lsqr_conlim** (*float*):
            LSQR algorithm conlim variable (must be ≥ 0).
            Default is 28.0.
        * **lsqr_itnlim** (*int*):
            LSQR algorithm itnlim variable (must be > 0).
            Default is 28.
        * **lsqrwrite** (*int*):
            Write LSQR file flag (must be 0 or 1).
            Default is 0 (don't write LSQR file).

    **Returns:**
    =======
        * ``None``

    **Examples:**
    =======

    1. **Adding an LSQR Section to a PEST Control File with Default Parameters:**

       .. code-block:: python

          from dpest.utils import lsqr

          lsqr(
              pst_path = "PEST_CONTROL.pst"
          )

       This example demonstrates adding a new LSQR section to a PEST control file using all default parameter values (lsqrmode=1, lsqr_atol=1e-4, lsqr_btol=1e-4, lsqr_conlim=28.0, lsqr_itnlim=28, lsqrwrite=0). The function will insert the LSQR section after any existing SVD section or append it to the file.

    2. **Updating Specific LSQR Parameters in an Existing PEST Control File:**

       .. code-block:: python

          from dpest.utils import lsqr

          lsqr(
              pst_path = "PEST_CONTROL.pst",
              lsqr_atol = 1e-6,
              lsqr_btol = 1e-6,
              lsqr_itnlim = 50
          )

       This example updates only the specified LSQR parameters (lsqr_atol, lsqr_btol, and lsqr_itnlim) while preserving existing values for other LSQR parameters. The function will modify the existing LSQR section if present, or create a new one with default values for unspecified parameters.

    3. **Disabling LSQR Mode While Maintaining Other Settings:**

       .. code-block:: python

          from dpest.utils import lsqr

          lsqr(
              pst_path = "PEST_CONTROL.pst",
              lsqrmode = 0
          )

       This example disables LSQR mode (lsqrmode=0) while keeping other LSQR parameters at their current values. If no LSQR section exists, it will be created with disabled mode and default values for other parameters.
    """
    try:
        import os

        # Default values for LSQR parameters
        defaults = {
            "lsqrmode": 1,
            "lsqr_atol": 1e-4,
            "lsqr_btol": 1e-4,
            "lsqr_conlim": 28.0,
            "lsqr_itnlim": 28,
            "lsqrwrite": 0
        }

        # Verify file exists
        if not os.path.isfile(pst_path):
            raise FileNotFoundError(f"File not found: {pst_path}")

        # Read the PST file
        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # Find the end of the control data section
        control_data_end_idx = None
        for i, line in enumerate(lines):
            if line.strip().lower().startswith('* control data'):
                # Find the end of control data section
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith('*'):
                    j += 1
                control_data_end_idx = j
                break

        if control_data_end_idx is None:
            raise ValueError(
                "This file does not contain a '* control data' section and is not a valid PEST control file.")

        # Check if LSQR section exists and extract current values
        existing_lsqr = {key: defaults[key] for key in defaults}
        lsqr_exists = False
        lsqr_start_idx = None

        for i, line in enumerate(lines):
            if line.strip().startswith('* lsqr'):
                lsqr_exists = True
                lsqr_start_idx = i

                # Try to extract existing values
                try:
                    # LSQRMODE (line after header)
                    if i + 1 < len(lines):
                        lsqrmode_line = lines[i + 1].strip().split()
                        if lsqrmode_line:
                            existing_lsqr["lsqrmode"] = int(lsqrmode_line[0])

                    # LSQR_ATOL, LSQR_BTOL, LSQR_CONLIM, LSQR_ITNLIM (3rd line)
                    if i + 2 < len(lines):
                        atol_btol_conlim_itnlim_line = lines[i + 2].strip().split()
                        if len(atol_btol_conlim_itnlim_line) >= 4:
                            existing_lsqr["lsqr_atol"] = float(atol_btol_conlim_itnlim_line[0])
                            existing_lsqr["lsqr_btol"] = float(atol_btol_conlim_itnlim_line[1])
                            existing_lsqr["lsqr_conlim"] = float(atol_btol_conlim_itnlim_line[2])
                            existing_lsqr["lsqr_itnlim"] = int(float(atol_btol_conlim_itnlim_line[3]))

                    # LSQRWRITE (4th line)
                    if i + 3 < len(lines):
                        lsqrwrite_line = lines[i + 3].strip().split()
                        if lsqrwrite_line:
                            existing_lsqr["lsqrwrite"] = int(lsqrwrite_line[0])
                except Exception as e:
                    print(f"Warning: Error parsing existing LSQR values: {e}")
                    # If parsing fails, we'll use defaults or user-provided values

                break

        # Use provided values if present, otherwise use existing values
        lsqr_values = {
            "lsqrmode": lsqrmode if lsqrmode is not None else existing_lsqr["lsqrmode"],
            "lsqr_atol": lsqr_atol if lsqr_atol is not None else existing_lsqr["lsqr_atol"],
            "lsqr_btol": lsqr_btol if lsqr_btol is not None else existing_lsqr["lsqr_btol"],
            "lsqr_conlim": lsqr_conlim if lsqr_conlim is not None else existing_lsqr["lsqr_conlim"],
            "lsqr_itnlim": lsqr_itnlim if lsqr_itnlim is not None else existing_lsqr["lsqr_itnlim"],
            "lsqrwrite": lsqrwrite if lsqrwrite is not None else existing_lsqr["lsqrwrite"]
        }

        # Validate LSQR values
        if lsqr_values["lsqrmode"] not in [0, 1]:
            raise ValueError("lsqrmode must be 0 or 1")

        if lsqr_values["lsqr_atol"] < 0:
            raise ValueError("lsqr_atol must be greater than or equal to 0")

        if lsqr_values["lsqr_btol"] < 0:
            raise ValueError("lsqr_btol must be greater than or equal to 0")

        if lsqr_values["lsqr_conlim"] < 0:
            raise ValueError("lsqr_conlim must be greater than or equal to 0")

        if not isinstance(lsqr_values["lsqr_itnlim"], int) or lsqr_values["lsqr_itnlim"] <= 0:
            raise ValueError("lsqr_itnlim must be an integer greater than 0")

        if lsqr_values["lsqrwrite"] not in [0, 1]:
            raise ValueError("lsqrwrite must be 0 or 1")

        # Format LSQR section
        lsqr_section = [
            '* lsqr\n',
            f'{lsqr_values["lsqrmode"]}\n',
            f'{lsqr_values["lsqr_atol"]:.6E} {lsqr_values["lsqr_btol"]:.6E} {lsqr_values["lsqr_conlim"]:.6E} {lsqr_values["lsqr_itnlim"]}\n',
            f'{lsqr_values["lsqrwrite"]}\n'
        ]

        # Update or add LSQR section
        if lsqr_exists:
            # Replace existing section
            lines[lsqr_start_idx:lsqr_start_idx + 4] = lsqr_section
        else:
            # Check for existing SVD section
            svd_exists = False
            for i, line in enumerate(lines):
                if line.strip().startswith('* singular value decomposition'):
                    svd_exists = True
                    # If user is enabling LSQR (mode=1), warn about SVD incompatibility
                    if lsqr_values["lsqrmode"] == 1:
                        print("Warning: LSQR and SVD cannot be used together. Adding LSQR will make SVD inactive.")
                    break

            # Insert LSQR section after control data section
            lines[control_data_end_idx :control_data_end_idx ] = lsqr_section

        # Write updated file
        with open(pst_path, 'w') as f:
            f.writelines(lines)

        print(f"LSQR section {'updated' if lsqr_exists else 'added'} successfully in {pst_path}")

    except FileNotFoundError as fe:
        print(f"Error: {str(fe)}")
    except ValueError as ve:
        print(f"Error: {str(ve)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")