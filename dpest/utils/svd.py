def svd(pst_path, svdmode=None, maxsing=None, eigthresh=None, eigwrite=None):
    """
    Adds or updates the Singular Value Decomposition (SVD) section in a PEST control (.pst) file.

    This function post-processes an existing ``PEST control file (.PST)`` to configure the
    ``* singular value decomposition`` section, following the recommendations of the PEST manual
    (Doherty 2015). It can be used to enable or disable SVD, or to adjust the truncation
    behavior through ``maxsing`` and ``eigthresh``.

    When SVD is enabled (``SVDMODE = 1``), this function will remove any existing
    ``* lsqr`` section to avoid confusion and ensure that only SVD is active in the
    control file.

    **Required Arguments:**
    =======

        * **pst_path** (*str*):
            Path to the ``PEST control file (.PST)`` to modify.

    **Optional Arguments:**
    =======

        * **svdmode** (*int*, *optional*):
            SVD activation flag (0 = disable SVD, 1 = enable SVD).
            If not provided, the current value in the file is preserved.
            If no SVD section exists, the default is 1 (enable SVD).

        * **maxsing** (*int*, *optional*):
            Maximum number of singular values to retain (must be > 0).
            If not provided, the behavior is:
              - If an SVD section already exists, use the existing ``MAXSING`` value.
              - If no SVD section exists, automatically set ``MAXSING`` equal to the
                number of adjustable parameters in the PST file.

        * **eigthresh** (*float*, *optional*):
            Eigenvalue ratio threshold at which singular value truncation occurs,
            with constraint ``0 <= eigthresh < 1``.
            If not provided, the behavior is:
              - If an SVD section already exists, use the existing ``EIGTHRESH`` value.
              - If no SVD section exists, default to ``5e-7``.

        * **eigwrite** (*int*, *optional*):
            SVD output file control flag (0 = write only singular values, 1 = write singular
            values and eigenvectors) to the ``case.svd`` file.
            If not provided, the behavior is:
              - If an SVD section already exists, use the existing ``EIGWRITE`` value.
              - If no SVD section exists, default to 0.

    **Returns:**
    =======

        * ``None``

        The function updates the ``PEST control file (.PST)`` in place. It will either modify
        an existing ``* singular value decomposition`` section or insert a new one. If SVD
        is enabled, any existing LSQR section is removed.

    **Examples:**
    =======

    1. **Adding an SVD Section Using Recommended Defaults:**

       .. code-block:: python

          from dpest.utils import svd

          # PEST_CONTROL.pst already exists (e.g., created by dpest.pst)
          svd(
              pst_path = "PEST_CONTROL.pst"
          )

       This example adds an SVD section using:
       ``svdmode = 1``,
       ``maxsing = npar`` (number of adjustable parameters),
       ``eigthresh = 5e-7``,
       ``eigwrite = 0``,
       and removes any existing ``* lsqr`` section.

    2. **Customizing SVD Parameters in an Existing PEST Control File:**

       .. code-block:: python

          from dpest.utils import svd

          svd(
              pst_path  = "PEST_CONTROL.pst",
              maxsing   = 500,
              eigthresh = 1e-4,
              eigwrite  = 1
          )

       This example updates the specified SVD parameters (``MAXSING``, ``EIGTHRESH``,
       and ``EIGWRITE``) while preserving the existing or default value of ``SVDMODE``.
       If SVD is enabled (``SVDMODE = 1``), any LSQR section is removed so only SVD
       remains active.

    3. **Disabling SVD While Keeping Other Settings:**

       .. code-block:: python

          from dpest.utils import svd

          svd(
              pst_path = "PEST_CONTROL.pst",
              svdmode  = 0
          )

       This example disables SVD (``SVDMODE = 0``) while keeping current or default
       values for ``MAXSING``, ``EIGTHRESH``, and ``EIGWRITE``. Any LSQR section is
       left unchanged because SVD is not being activated.
    """
    try:
        import os
        import pyemu

        # Default values for SVD parameters (used only when no SVD section exists)
        defaults = {
            "svdmode": 1,        # enable SVD by default
            "maxsing": None,     # will be set to npar when needed
            "eigthresh": 5e-7,   # recommended default
            "eigwrite": 0        # only singular values
        }

        # Verify file exists
        if not os.path.isfile(pst_path):
            raise FileNotFoundError(f"File not found: {pst_path}")

        # Read the PST file as text
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

        # Load PST with pyEMU to get number of parameters (npar)
        try:
            pst_obj = pyemu.Pst(pst_path)
            npar = pst_obj.npar
        except Exception as e:
            raise RuntimeError(f"Unable to read PST with pyEMU to determine npar: {str(e)}")

        # Initialize existing SVD values (from file or defaults)
        existing_svd = {key: defaults.get(key) for key in defaults}
        svd_exists = False
        svd_start_idx = None

        # If an SVD section exists, parse it
        for i, line in enumerate(lines):
            if line.strip().lower().startswith('* singular value decomposition'):
                svd_exists = True
                svd_start_idx = i

                try:
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

        # If no existing SVD section, set defaults that depend on npar
        if not svd_exists:
            if existing_svd["maxsing"] is None:
                existing_svd["maxsing"] = npar
            if existing_svd["eigthresh"] is None:
                existing_svd["eigthresh"] = defaults["eigthresh"]
            if existing_svd["svdmode"] is None:
                existing_svd["svdmode"] = defaults["svdmode"]
            if existing_svd["eigwrite"] is None:
                existing_svd["eigwrite"] = defaults["eigwrite"]

        # Merge user inputs with existing/default values
        svd_values = {
            "svdmode": svdmode if svdmode is not None else existing_svd["svdmode"],
            "maxsing": maxsing if maxsing is not None else existing_svd["maxsing"],
            "eigthresh": eigthresh if eigthresh is not None else existing_svd["eigthresh"],
            "eigwrite": eigwrite if eigwrite is not None else existing_svd["eigwrite"]
        }

        # If maxsing is still None for some reason, fall back to npar
        if svd_values["maxsing"] is None:
            svd_values["maxsing"] = npar

        # Validate values
        if svd_values["svdmode"] not in [0, 1]:
            raise ValueError("svdmode must be 0 or 1")
        if svd_values["maxsing"] <= 0:
            raise ValueError("maxsing must be > 0")
        if not (0 <= svd_values["eigthresh"] < 1):
            raise ValueError("eigthresh must be 0 ≤ value < 1")
        if svd_values["eigwrite"] not in [0, 1]:
            raise ValueError("eigwrite must be 0 or 1")

        # If SVD is enabled, remove any existing LSQR section entirely
        if svd_values["svdmode"] == 1:
            i = 0
            while i < len(lines):
                if lines[i].strip().lower().startswith('* lsqr'):
                    del lines[i:i+4]
                    print("Info: SVD enabled; existing LSQR section removed.")
                    break
                i += 1

        # Format SVD section
        svd_section = [
            '* singular value decomposition\n',
            f'{svd_values["svdmode"]}\n',
            f'{svd_values["maxsing"]} {svd_values["eigthresh"]:.6E}\n',
            f'{svd_values["eigwrite"]}\n'
        ]

        # Update or add section
        if svd_exists:
            lines[svd_start_idx:svd_start_idx + 4] = svd_section
        else:
            lines[control_data_end_idx:control_data_end_idx] = svd_section

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
