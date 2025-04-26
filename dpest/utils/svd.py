def svd(pst_path, svdmode=None, maxsing=None, eigthresh=None, eigwrite=None):
    """
    Adds or updates the Singular Value Decomposition (SVD) section in a PEST control (.pst) file.

    The SVD section configures truncated singular value decomposition for solving ill-posed inverse problems.

    **Required Arguments:**
    =======
        * **pst_path** (*str*):
            Path to the .pst PEST control file to modify.

    **Optional Arguments:**
    =======
        * **svdmode** (*int*):
            SVD activation (0=disable, 1=enable).
            Default is 1 (enable SVD).
        * **maxsing** (*int*):
            Maximum singular values to retain (must be > 0).
            Default is 10000000.
        * **eigthresh** (*float*):
            Eigenvalue ratio threshold (0 ≤ eigthresh < 1).
            Default is 1e-6.
        * **eigwrite** (*int*):
            SVD output file control (0=no output, 1=write output).
            Default is 0.

    **Returns:**
    =======
        * ``None``

    **Examples:**
    =======

    **Examples:**
    =======

    1. **Adding an SVD Section to a PEST Control File with Default Parameters:**

       .. code-block:: python

          from dpest.utils import svd

          svd(
              pst_path = "PEST_CONTROL.pst"
          )

       This example demonstrates adding a new SVD section to a PEST control file using all default parameter values (svdmode=1, maxsing=10000000, eigthresh=1e-6, eigwrite=0). The function will insert the SVD section after any existing LSQR section or append it to the file.

    2. **Customizing SVD Parameters in an Existing PEST Control File:**

       .. code-block:: python

          from dpest.utils import svd

          svd(
              pst_path = "PEST_CONTROL.pst",
              maxsing = 500,
              eigthresh = 0.01,
              eigwrite = 1
          )

       This example updates the specified SVD parameters (maxsing, eigthresh, and eigwrite) while preserving existing values for other SVD parameters. The function will modify the existing SVD section if present, or create a new one with default values for unspecified parameters.

    3. **Disabling SVD Functionality While Maintaining Other Settings:**

       .. code-block:: python

          from dpest.utils import svd

          svd(
              pst_path = "PEST_CONTROL.pst",
              svdmode = 0
          )

       This example disables SVD mode (svdmode=0) while keeping other SVD parameters at their current values. If no SVD section exists, it will be created with disabled mode and default values for other parameters.
    """
    try:
        import os

        # Default values for SVD parameters
        defaults = {
            "svdmode": 1,
            "maxsing": 10000000,
            "eigthresh": 1e-6,
            "eigwrite": 0
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
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith('*'):
                    j += 1
                control_data_end_idx = j
                break

        if control_data_end_idx is None:
            raise ValueError("Missing required '* control data' section")

        # Check if SVD section exists and extract current values
        existing_svd = {key: defaults[key] for key in defaults}
        svd_exists = False
        svd_start_idx = None

        for i, line in enumerate(lines):
            if line.strip().startswith('* singular value decomposition'):
                svd_exists = True
                svd_start_idx = i

                try:  # Parse existing values
                    # SVDMODE line
                    if i + 1 < len(lines):
                        svdmode_line = lines[i + 1].strip().split()
                        if svdmode_line:
                            existing_svd["svdmode"] = int(svdmode_line[0])

                    # MAXSING/EIGTHRESH line
                    if i + 2 < len(lines):
                        vals = lines[i + 2].strip().split()
                        if len(vals) >= 2:
                            existing_svd["maxsing"] = int(vals[0])
                            existing_svd["eigthresh"] = float(vals[1])

                    # EIGWRITE line
                    if i + 3 < len(lines):
                        eigwrite_line = lines[i + 3].strip().split()
                        if eigwrite_line:
                            existing_svd["eigwrite"] = int(eigwrite_line[0])
                except Exception as e:
                    print(f"Warning: Error parsing SVD values: {str(e)}")

                break

        # Merge user inputs with existing/default values
        svd_values = {
            "svdmode": svdmode if svdmode is not None else existing_svd["svdmode"],
            "maxsing": maxsing if maxsing is not None else existing_svd["maxsing"],
            "eigthresh": eigthresh if eigthresh is not None else existing_svd["eigthresh"],
            "eigwrite": eigwrite if eigwrite is not None else existing_svd["eigwrite"]
        }

        # Validate values
        if svd_values["svdmode"] not in [0, 1]:
            raise ValueError("svdmode must be 0 or 1")

        if svd_values["maxsing"] <= 0:
            raise ValueError("maxsing must be > 0")

        if not (0 <= svd_values["eigthresh"] < 1):
            raise ValueError("eigthresh must be 0 ≤ value < 1")

        if svd_values["eigwrite"] not in [0, 1]:
            raise ValueError("eigwrite must be 0 or 1")

        # Format SVD section
        svd_section = [
            '* singular value decomposition\n',
            f'{svd_values["svdmode"]}\n',
            f'{svd_values["maxsing"]} {svd_values["eigthresh"]:.6E}\n',
            f'{svd_values["eigwrite"]}\n'
        ]

        # Update or add section
        if svd_exists:
            # Replace existing section
            lines[svd_start_idx:svd_start_idx + 4] = svd_section
        else:
            # Check for LSQR conflict
            lsqr_exists = any(line.strip().startswith('* lsqr') for line in lines)
            if svd_values["svdmode"] == 1 and lsqr_exists:
                print("Warning: SVD and LSQR are mutually exclusive. Adding SVD will make LSQR inactive.")

            # Insert after control data section
            lines[control_data_end_idx :control_data_end_idx ] = svd_section

        # Write updated file
        with open(pst_path, 'w') as f:
            f.writelines(lines)

        print(f"SVD section {'updated' if svd_exists else 'added'} successfully in {pst_path}")

    except FileNotFoundError as fe:
        print(f"Error: {str(fe)}")
    except ValueError as ve:
        print(f"Validation Error: {str(ve)}")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")