import os

def regularisation(
    pst_path,
    phimlim,
    phimaccept,
    fracphim=0.1,
    memsave=None,
    wfinit=1.0,
    wfmin=1e-10,
    wfmax=1e10,
    linreg=None,       # "linreg" / "nonlinreg" / None
    regcontinue=None,  # "continue" / "nocontinue" / None
    wffac=1.3,
    wftol=1e-2,
    iregadj=0,
    noptregadj=None,
    regweightrat=None,
    regsingthresh=None,
):
    """
    Adds or updates the ``* regularisation`` section in a PEST control (.pst) file
    and sets ``PESTMODE`` to ``regularisation`` in the ``* control data`` section.

    This function post-processes an existing ``PEST control file (.PST)`` to configure
    PEST for Tikhonov regularisation, following the recommendations in the PEST manual
    (Doherty 2015, Chapter 9). It can be used to:

      * switch PEST into regularisation mode (``PESTMODE = regularisation``),
      * define the target and acceptable measurement objective functions
        (``PHIMLIM``, ``PHIMACCEPT``),
      * control how the regularisation weight factor is initialised and updated, and
      * optionally activate subspace‑enhanced regularisation via ``IREGADJ``.

    When called, this function will:

      * set the second token on the first ``* control data`` line to
        ``regularisation`` (PESTMODE),
      * insert a new ``* regularisation`` section at the end of the file or update
        an existing one, and
      * leave all other sections and content unchanged.

    **Required Arguments:**
    =======

        * **pst_path** (*str*):
            Path to the ``PEST control file (.PST)`` to modify.

        * **phimlim** (*float*):
            Target measurement objective function (``PHIMLIM``). PEST aims for
            this value while keeping the regularisation objective function as low
            as possible. Must be greater than 0.

        * **phimaccept** (*float*):
            Acceptable measurement objective function (``PHIMACCEPT``). This
            should typically be 5–10% higher than ``PHIMLIM`` to give PEST
            “room to move” when balancing measurement and regularisation
            objective functions. Must be greater than ``phimlim``.

    **Optional Arguments:**
    =======

        * **fracphim** (*float*, *default: 0.1*):
            ``FRACPHIM`` in the PEST manual. Must satisfy
            ``0.0 < fracphim < 1.0``. When provided, PEST recalculates an
            effective ``PHIMLIM`` at each iteration as
            ``max(user_PHIMLIM, fracphim * current_phi_m)`` so that the
            measurement objective function target is reduced gradually rather
            than being set unrealistically low from the start.

        * **memsave** (*str*, *optional*):
            Optional memory‑saving flag (``MEMSAVE``). If provided, must be
            either ``"memsave"`` or ``"nomemsave"``. If ``None``, this variable
            is omitted from the section.

        * **wfinit** (*float*, *default: 1.0*):
            Initial regularisation weight factor (``WFINIT``). Used as the
            starting value for the iterative procedure that finds an appropriate
            regularisation weight factor on the first iteration.

        * **wfmin** (*float*, *default: 1e-10*):
            Minimum permissible value for the regularisation weight factor
            (``WFMIN``).

        * **wfmax** (*float*, *default: 1e10*):
            Maximum permissible value for the regularisation weight factor
            (``WFMAX``).

        * **linreg** (*str*, *optional*):
            Optional ``LINREG`` control flag to indicate whether all
            regularisation constraints are linear. If provided, must be either
            ``"linreg"`` or ``"nonlinreg"``. If ``None``, this flag is omitted
            and PEST’s default behaviour is used. This text variable appears on
            the second line of the regularisation section and can be placed in
            any order relative to ``regcontinue``.

        * **regcontinue** (*str*, *optional*):
            Optional ``REGCONTINUE`` control flag. If provided, must be either
            ``"continue"`` or ``"nocontinue"``. When set to ``"continue"``,
            PEST continues iterating after ``PHIMLIM`` is achieved in order to
            further reduce the regularisation objective function, stopping only
            when other convergence criteria are met. As with ``linreg``, this
            text variable appears on the second regularisation line, in any
            order relative to ``linreg``.

        * **wffac** (*float*, *default: 1.3*):
            ``WFFAC`` (> 1.0). Multiplicative factor used when bracketing the
            regularisation weight factor during its iterative calculation for
            each iteration. Recommended values are around 1.3.

        * **wftol** (*float*, *default: 1e-2*):
            ``WFTOL`` (> 0). Relative tolerance for convergence of the
            regularisation weight factor calculation. Recommended values are
            between ``1e-3`` and ``1e-2``.

        * **iregadj** (*int*, *default: 0*):
            ``IREGADJ`` setting (0–5) controlling differential weighting of
            regularisation groups or items:

              - 0: no inter‑group weight adjustment (global regularisation
                factor only).
              - 1, 2, 3: group‑based adjustment strategies.
              - 4, 5: subspace‑enhanced regularisation using SVD of the
                weighted Jacobian (requires ``noptregadj`` and
                ``regweightrat``, and for 5 also ``regsingthresh``).

        * **noptregadj** (*int*, *optional*):
            ``NOPTREGADJ``. Required when ``iregadj`` is 4 or 5 and ignored
            otherwise. Specifies the iteration interval at which regularisation
            weights are recalculated (e.g. 1 = every iteration, 3 = every third
            iteration).

        * **regweightrat** (*float*, *optional*):
            ``REGWEIGHTRAT``. Required when ``iregadj`` is 4 or 5 and ignored
            otherwise. Specifies the ratio of the largest to the smallest
            regularisation weight after compression (typical values are
            between 10 and 100).

        * **regsingthresh** (*float*, *optional*):
            ``REGSINGTHRESH``. Required when ``iregadj`` is 5 and ignored
            otherwise. Defines the singular value ratio used to separate the
            calibration solution space from the calibration null space for the
            purposes of assigning two distinct weight levels to regularisation
            constraints.

    **Returns:**
    =======

        * ``None``

        The function updates the ``PEST control file (.PST)`` in place. It sets
        ``PESTMODE = regularisation`` in the control‑data section and either
        inserts a new ``* regularisation`` section or overwrites an existing
        one with the supplied settings.

    **Examples:**
    =======

    1. **Enable regularisation with recommended defaults (no subspace enhancement):**

       .. code-block:: python

          from dpest.utils import regularisation

          regularisation(
              pst_path    = "PEST_CONTROL.pst",
              phimlim     = 125.0,
              phimaccept  = 130.0,
              fracphim    = 0.1,
              wfinit      = 1.0,
              wfmin       = 1.0e-10,
              wfmax       = 1.0e10,
              wffac       = 1.3,
              wftol       = 1.0e-2,
              iregadj     = 0,
          )

       This example switches PEST into regularisation mode and adds a
       ``* regularisation`` section using commonly recommended defaults,
       without any automatic inter‑group weight adjustment.

    2. **Regularisation with composite‑sensitivity‑based group adjustment (IREGADJ = 1):**

       .. code-block:: python

          from dpest.utils import regularisation

          regularisation(
              pst_path    = "PEST_CONTROL.pst",
              phimlim     = 200.0,
              phimaccept  = 210.0,
              fracphim    = 0.1,
              wfinit      = 1.0,
              wfmin       = 1.0e-10,
              wfmax       = 1.0e10,
              wffac       = 1.3,
              wftol       = 1.0e-2,
              iregadj     = 1,
          )

       Here, PEST automatically adjusts weights across regularisation groups
       so that their composite sensitivities are balanced, while still using a
       single global regularisation weight factor per iteration.

    3. **Subspace‑enhanced regularisation (IREGADJ = 4):**

       .. code-block:: python

          from dpest.utils import regularisation

          regularisation(
              pst_path       = "PEST_CONTROL.pst",
              phimlim        = 150.0,
              phimaccept     = 157.5,
              fracphim       = 0.1,
              wfinit         = 1.0,
              wfmin          = 1.0e-10,
              wfmax          = 1.0e10,
              wffac          = 1.3,
              wftol          = 1.0e-2,
              iregadj        = 4,
              noptregadj     = 3,
              regweightrat   = 50.0,
          )

       This example enables subspace‑enhanced regularisation in which
       regularisation weights are adjusted on an item‑by‑item basis using SVD
       of the weighted Jacobian. Weights are recomputed every third
       optimisation iteration and compressed so that the ratio of the largest
       to the smallest weight is 50.

    4. **Subspace‑enhanced regularisation with two‑level weights (IREGADJ = 5):**

       .. code-block:: python

          from dpest.utils import regularisation

          regularisation(
              pst_path       = "PEST_CONTROL.pst",
              phimlim        = 150.0,
              phimaccept     = 157.5,
              fracphim       = 0.1,
              wfinit         = 1.0,
              wfmin          = 1.0e-10,
              wfmax          = 1.0e10,
              wffac          = 1.3,
              wftol          = 1.0e-2,
              iregadj        = 5,
              noptregadj     = 2,
              regweightrat   = 20.0,
              regsingthresh  = 1.0e-5,
          )

       In this configuration, each regularisation constraint is assigned one of
       two weight levels based on its projection onto the calibration solution
       space, with the ratio of null‑space to solution‑space weights equal to
       ``regweightrat``.
    """

    # Basic validation
    if not os.path.isfile(pst_path):
        raise FileNotFoundError(f"File not found: {pst_path}")

    if not (phimlim > 0.0):
        raise ValueError("phimlim must be > 0.0")

    if not (phimaccept > phimlim):
        raise ValueError("phimaccept should be > phimlim (typically 5–10% higher).")

    if not (0.0 < fracphim < 1.0):
        raise ValueError("fracphim must be between 0.0 and 1.0 (recommended ~0.1).")

    if wffac <= 1.0:
        raise ValueError("wffac must be greater than 1.0")

    if wftol <= 0.0:
        raise ValueError("wftol must be > 0.0")

    if iregadj not in (0, 1, 2, 3, 4, 5):
        raise ValueError("iregadj must be one of {0,1,2,3,4,5}")

    if iregadj in (4, 5):
        if noptregadj is None or regweightrat is None:
            raise ValueError("noptregadj and regweightrat are required for iregadj 4 or 5")
        if iregadj == 5 and regsingthresh is None:
            raise ValueError("regsingthresh is required for iregadj 5")

    # Read file
    with open(pst_path, "r") as f:
        lines = f.readlines()

    # 1) Ensure PESTMODE = regularisation in * control data
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("* control data"):
            # next line should contain PESTMODE as the second token
            j = i + 1
            if j < len(lines):
                parts = lines[j].split()
                if len(parts) >= 2:
                    parts[1] = "regularisation"
                    # preserve leading spaces
                    pad = len(lines[j]) - len(lines[j].lstrip())
                    lines[j] = " " * pad + " ".join(parts) + "\n"
            break

    # 2) Build regularisation section text
    # First line
    line1_tokens = [f"{phimlim:.7g}", f"{phimaccept:.7g}", f"{fracphim:.7g}"]
    if memsave is not None:
        line1_tokens.append(memsave)

    line1 = " ".join(line1_tokens) + "\n"

    # Second line
    line2_tokens = [f"{wfinit:.7g}", f"{wfmin:.7g}", f"{wfmax:.7g}"]
    # Optional LINREG and/or REGCONTINUE may follow in any order
    if linreg is not None:
        line2_tokens.append(linreg)
    if regcontinue is not None:
        line2_tokens.append(regcontinue)
    line2 = " ".join(line2_tokens) + "\n"

    # Third line
    line3_tokens = [f"{wffac:.7g}", f"{wftol:.7g}", str(int(iregadj))]
    if iregadj in (4, 5):
        line3_tokens.append(str(int(noptregadj)))
        line3_tokens.append(f"{regweightrat:.7g}")
        if iregadj == 5:
            line3_tokens.append(f"{regsingthresh:.7g}")
    line3 = " ".join(line3_tokens) + "\n"

    reg_section = [
        "* regularisation\n",
        line1,
        line2,
        line3,
    ]

    # 3) Insert or replace * regularisation section at the end of the file
    start_idx = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("* regularisation"):
            start_idx = i
            break

    if start_idx is not None:
        # Replace existing section (assume current section is 4 lines or more;
        # we overwrite 4 lines and leave any trailing comments untouched)
        lines[start_idx:start_idx + 4] = reg_section
    else:
        # Append at the end, ensuring a newline separator
        if lines and not lines[-1].endswith("\n"):
            lines[-1] = lines[-1] + "\n"
        lines.extend(reg_section)

    # 4) Write back
    with open(pst_path, "w") as f:
        f.writelines(lines)

    print(f"Regularisation section added/updated successfully in {pst_path}")
    print("PESTMODE set to 'regularisation' in * control data.")