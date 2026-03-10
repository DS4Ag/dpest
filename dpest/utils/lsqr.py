def lsqr(pst_path, lsqrmode=None, lsqr_atol=None, lsqr_btol=None,
         lsqr_conlim=None, lsqr_itnlim=None, lsqrwrite=None):
    """
    Adds or updates the LSQR section in a PEST control (.pst) file.

    The LSQR section configures PEST to use the LSQR algorithm for solving the inverse
    problem. This is especially useful for large models with many parameters. Default
    values follow the recommendations from the PEST manual (Doherty 2015) for finite-
    difference derivatives and least-squares problems.

    When LSQR is enabled (``LSQRMODE = 1``), this function will remove any existing
    ``* singular value decomposition`` section to avoid confusion and ensure that
    only LSQR is active in the control file.

    **Required Arguments:**
    =======

        * **pst_path** (*str*):
            Path to the ``PEST control file (.PST)`` to modify.

    **Optional Arguments:**
    =======

        * **lsqrmode** (*int*, *optional*):
            LSQR mode flag (0 = disable LSQR, 1 = enable LSQR).
            If not provided, the current value in the file is preserved.
            If no LSQR section exists, the default is 1 (enable LSQR).

        * **lsqr_atol** (*float*, *optional*):
            LSQR algorithm ``ATOL`` variable (must be ≥ 0).
            This is an estimate of the relative error in the data defining the matrix A
            (equivalent to Q^(1/2) J in PEST). For finite-difference derivatives, a value
            of ``1e-4`` generally works well.
            If not provided:
              - Uses the current value if an LSQR section exists.
              - Otherwise defaults to ``1e-4``.

        * **lsqr_btol** (*float*, *optional*):
            LSQR algorithm ``BTOL`` variable (must be ≥ 0).
            This is an estimate of the relative error in the data defining the right-hand
            side vector b. For PEST, a value of ``1e-4`` generally works well.
            If not provided:
              - Uses the current value if an LSQR section exists.
              - Otherwise defaults to ``1e-4``.

        * **lsqr_conlim** (*float*, *optional*):
            LSQR algorithm ``CONLIM`` variable (must be ≥ 0).
            This is an upper limit on the apparent condition number of A. Iterations are
            terminated if the estimated condition number exceeds this value, to prevent
            very small singular values from causing unwanted solution growth. The PEST
            manual suggests values in the range 1000 to 1/relpr; for PEST applications,
            ``1000.0`` generally works well.
            If not provided:
              - Uses the current value if an LSQR section exists.
              - Otherwise defaults to ``1000.0``.

        * **lsqr_itnlim** (*int*, *optional*):
            LSQR algorithm ``ITNLIM`` variable (must be > 0).
            This is an upper limit on the number of LSQR iterations. In LSQR documentation,
            suggested values are:
              - itnlim = m/2 for well-conditioned systems with clustered singular values;
              - itnlim = 4*m otherwise,
            where m is the number of columns of A. In the PEST context, m is the number
            of adjustable parameters. The PEST manual therefore recommends setting
            ``LSQR_ITNLIM = 4 * number_of_adjustable_parameters``.
            If not provided:
              - Uses the current value if an LSQR section exists.
              - Otherwise defaults to ``4 * npar`` where npar is read from the PST file.

        * **lsqrwrite** (*int*, *optional*):
            Flag controlling LSQR output file (0 or 1).
            If set to 1, LSQR output is written to ``case.lsq``; this file can become
            large. If not desired, set to 0.
            If not provided:
              - Uses the current value if an LSQR section exists.
              - Otherwise defaults to 0 (no LSQR output file).

    **Returns:**
    =======

        * ``None``

        The function updates the ``PEST control file (.PST)`` in place, either modifying an
        existing ``* lsqr`` section or inserting a new one. If LSQR is enabled, any existing
        SVD section is removed.

    **Examples:**
    =======

    1. **Adding an LSQR Section Using Recommended Defaults:**

       .. code-block:: python

          from dpest.utils import lsqr

          # PEST_CONTROL.pst already exists (e.g., created by dpest.pst)
          lsqr(
              pst_path = "PEST_CONTROL.pst"
          )

       This example adds an LSQR section using:
       ``lsqrmode = 1``,
       ``lsqr_atol = 1e-4``,
       ``lsqr_btol = 1e-4``,
       ``lsqr_conlim = 1000.0``,
       ``lsqr_itnlim = 4 * npar``,
       ``lsqrwrite = 0``,
       and removes any existing ``* singular value decomposition`` section.

    2. **Updating Specific LSQR Parameters in an Existing PEST Control File:**

       .. code-block:: python

          from dpest.utils import lsqr

          lsqr(
              pst_path   = "PEST_CONTROL.pst",
              lsqr_atol  = 1e-6,
              lsqr_btol  = 1e-6,
              lsqr_conlim= 2000.0,
              lsqr_itnlim= 50
          )

       This example updates only the specified LSQR parameters (``LSQR_ATOL``,
       ``LSQR_BTOL``, ``LSQR_CONLIM``, and ``LSQR_ITNLIM``) while preserving existing
       values for other LSQR parameters.

    3. **Disabling LSQR Mode While Maintaining Other Settings:**

       .. code-block:: python

          from dpest.utils import lsqr

          lsqr(
              pst_path  = "PEST_CONTROL.pst",
              lsqrmode  = 0
          )

       This example disables LSQR mode (``LSQRMODE = 0``) while keeping other LSQR
       parameters at their current or default values. Any existing SVD section is
       left unchanged because LSQR is not being activated.
    """
    try:
        import os
        import pyemu
        import numbers

        # Default values for LSQR parameters (used only when no LSQR section exists)
        defaults = {
            "lsqrmode": 1,         # enable LSQR by default
            "lsqr_atol": 1e-4,     # recommended for FD derivatives
            "lsqr_btol": 1e-4,     # recommended for FD derivatives
            "lsqr_conlim": 1000.0, # recommended "generally works well"
            "lsqr_itnlim": None,   # will be set to 4 * npar when needed
            "lsqrwrite": 0         # no LSQR output file by default
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
            raise ValueError(
                "This file does not contain a '* control data' section and is not a valid PEST control file."
            )

        # Load PST with pyEMU to get number of parameters for ITNLIM default
        try:
            pst_obj = pyemu.Pst(pst_path)
            npar = pst_obj.npar
        except Exception as e:
            raise RuntimeError(f"Unable to read PST with pyEMU to determine npar: {str(e)}")

        # Check if LSQR section exists and extract current values
        existing_lsqr = {key: defaults[key] for key in defaults}
        lsqr_exists = False
        lsqr_start_idx = None

        for i, line in enumerate(lines):
            if line.strip().lower().startswith('* lsqr'):
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
                        vals = lines[i + 2].strip().split()
                        if len(vals) >= 4:
                            existing_lsqr["lsqr_atol"] = float(vals[0])
                            existing_lsqr["lsqr_btol"] = float(vals[1])
                            existing_lsqr["lsqr_conlim"] = float(vals[2])
                            existing_lsqr["lsqr_itnlim"] = int(float(vals[3]))

                    # LSQRWRITE (4th line)
                    if i + 3 < len(lines):
                        lsqrwrite_line = lines[i + 3].strip().split()
                        if lsqrwrite_line:
                            existing_lsqr["lsqrwrite"] = int(lsqrwrite_line[0])
                except Exception as e:
                    print(f"Warning: Error parsing existing LSQR values: {e}")
                break

        # If no existing LSQR section, set defaults that depend on npar
        if not lsqr_exists and existing_lsqr["lsqr_itnlim"] is None:
            existing_lsqr["lsqr_itnlim"] = 4 * npar

        # Use provided values if present, otherwise use existing/default values
        lsqr_values = {
            "lsqrmode": lsqrmode if lsqrmode is not None else existing_lsqr["lsqrmode"],
            "lsqr_atol": lsqr_atol if lsqr_atol is not None else existing_lsqr["lsqr_atol"],
            "lsqr_btol": lsqr_btol if lsqr_btol is not None else existing_lsqr["lsqr_btol"],
            "lsqr_conlim": lsqr_conlim if lsqr_conlim is not None else existing_lsqr["lsqr_conlim"],
            "lsqr_itnlim": lsqr_itnlim if lsqr_itnlim is not None else existing_lsqr["lsqr_itnlim"],
            "lsqrwrite": lsqrwrite if lsqrwrite is not None else existing_lsqr["lsqrwrite"]
        }

        # If lsqr_itnlim is still None for some reason, fall back to 4 * npar
        if lsqr_values["lsqr_itnlim"] is None:
            lsqr_values["lsqr_itnlim"] = 4 * npar

        # Normalize integer-like types
        if isinstance(lsqr_values["lsqr_itnlim"], numbers.Integral):
            lsqr_values["lsqr_itnlim"] = int(lsqr_values["lsqr_itnlim"])

        # Validate LSQR values
        if lsqr_values["lsqrmode"] not in [0, 1]:
            raise ValueError("lsqrmode must be 0 or 1")
        if lsqr_values["lsqr_atol"] < 0:
            raise ValueError("lsqr_atol must be greater than or equal to 0")
        if lsqr_values["lsqr_btol"] < 0:
            raise ValueError("lsqr_btol must be greater than or equal to 0")
        if lsqr_values["lsqr_conlim"] < 0:
            raise ValueError("lsqr_conlim must be greater than or equal to 0")
        if lsqr_values["lsqr_itnlim"] <= 0:
            raise ValueError("lsqr_itnlim must be an integer greater than 0")
        if lsqr_values["lsqrwrite"] not in [0, 1]:
            raise ValueError("lsqrwrite must be 0 or 1")

        # If LSQR is enabled, remove any existing SVD section entirely
        if lsqr_values["lsqrmode"] == 1:
            i = 0
            while i < len(lines):
                if lines[i].strip().lower().startswith('* singular value decomposition'):
                    # Remove 4-line SVD block
                    del lines[i:i+4]
                    print("Info: LSQR enabled; existing SVD section removed.")
                    # Do not increment i, list has shrunk; but break is fine since we assume one SVD section
                    break
                i += 1

        # Format LSQR section
        lsqr_section = [
            '* lsqr\n',
            f'{lsqr_values["lsqrmode"]}\n',
            f'{lsqr_values["lsqr_atol"]:.6E} {lsqr_values["lsqr_btol"]:.6E} {lsqr_values["lsqr_conlim"]:.6E} {lsqr_values["lsqr_itnlim"]}\n',
            f'{lsqr_values["lsqrwrite"]}\n'
        ]

        # Update or add LSQR section
        if lsqr_exists:
            lines[lsqr_start_idx:lsqr_start_idx + 4] = lsqr_section
        else:
            lines[control_data_end_idx:control_data_end_idx] = lsqr_section

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
