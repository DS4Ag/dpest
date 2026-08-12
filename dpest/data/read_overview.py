from dpest.functions import *

def read_overview(
        overview_file,
        variables=None,
        experiments=None,
        treatments=None,
        treatments_name=None,
        measured_only=True,
):
    """
    Extracts simulation data from the DSSAT ``OVERVIEW.OUT`` file for each
    treatment, including experiment and cultivar information, and returns
    a DataFrame with the parsed values.

    The ``OVERVIEW.OUT`` file contains end-of-season crop performance metrics
    and key phenological observations for each treatment within one or more
    experiments. This function parses those blocks and optionally filters the
    results by variable, experiment, treatment number, or treatment name.

    **Required Arguments**
    ======================

    * **overview_file** (*str*):
      Path to the DSSAT ``OVERVIEW.OUT`` file to read.

      Examples:

      - ``"C:/DSSAT48/Wheat/OVERVIEW.OUT"``
      - ``"C:/DSSAT48/Soybean/OVERVIEW.OUT"``

    **Optional Arguments**
    ======================

    * **variables** (*list* or *str*, *optional*):
      Variable name(s) to keep from the ``OVERVIEW.OUT`` file. These must
      match exactly the variable labels that appear in the data section
      (after the ``@`` header line).

      - A single variable can be provided as a string, e.g.
        ``"Yield at harvest maturity (kg [dm]/ha)"``.
      - Multiple variables can be provided as a list, e.g.::

          [
              "Anthesis (DAP)",
              "Maturity (DAP)",
              "Product wt (kg dm/ha;no loss)",
              "Maximum leaf area index"
          ]

      If ``None`` (default), no filtering by variable is applied.

    * **experiments** (*list* or *str*, *optional*):
      Experiment code(s) to keep, as they appear on the ``EXPERIMENT`` line
      in the header (e.g. ``"AZMC9311"``).

      - Single code as a string, e.g. ``"AZMC9311"``.
      - Multiple codes as a list, e.g. ``["AZMC9311", "AZMC9312"]``.

      If ``None``, observations from all experiments in the file are returned.

    * **treatments** (*list* or *int/str*, *optional*):
      Treatment number(s) to keep, as they appear on the ``TREATMENT``
      header line within each block (typically 1-based integers).

      - Single treatment number as an integer or string, e.g. ``1`` or ``"1"``.
      - Multiple treatment numbers as a list, e.g. ``[1, 2, 3]``.

      If ``None``, no filtering by treatment number is applied.

    * **treatments_name** (*list* or *str*, *optional*):
      Full treatment name(s) to keep, as they appear in the DSSAT interface
      and in the ``OVERVIEW.OUT`` header (e.g. ``"164.0 KG N/HA DRY"``).

      - Single treatment name as a string, e.g. ``"164.0 KG N/HA DRY"``.
      - Multiple names as a list, e.g.::

          ["164.0 KG N/HA DRY", "82.0 KG N/HA DRY"]

      If ``None``, no filtering by treatment name is applied.

    * **measured_only** (*bool*, *default: True*):
      If ``True``, rows where the measured value is missing are removed from
      the output (i.e. only observations with measured data are returned).
      If ``False``, all parsed rows are kept, including those without
      measured values.

    **Returns**
    ===========

    * *pandas.DataFrame*:
      A DataFrame with one row per variable and treatment combination,
      containing at least the following columns:

      - ``experiment``: experiment code extracted from the header.
      - ``treatment``: numeric treatment identifier.
      - ``treatment_name``: full DSSAT treatment name.
      - ``cultivar``: cultivar name extracted from the header.
      - ``variable``: variable label as printed in the ``OVERVIEW.OUT`` file.
      - ``value_simulated``: simulated value reported by DSSAT (float).
      - ``value_measured``: measured value from the DSSAT A file (float, may
        be ``NaN`` if ``measured_only=False``).

    **Examples**
    ============

    1. **Read all variables for a specific treatment**

       .. code-block:: python

           from dpest import read_overview

           df = read_overview(
               overview_file="C:/DSSAT48/Wheat/OVERVIEW.OUT",
               treatments=1,  # treatment number 1
           )

       This returns all variables for treatment 1 across all experiments in
       the ``OVERVIEW.OUT`` file, keeping only rows with measured values.

    2. **Filter by variables and experiment code**

       .. code-block:: python

           df = read_overview(
               overview_file="C:/DSSAT48/Wheat/OVERVIEW.OUT",
               variables=[
                   "Anthesis (DAP)",
                   "Maturity (DAP)",
                   "Yield at harvest maturity (kg [dm]/ha)"
               ],
               experiments="AZMC9311",
           )

       This returns only the selected phenology and yield variables for
       experiment ``AZMC9311``.

    3. **Filter by treatment name and keep missing measured values**

       .. code-block:: python

           df = read_overview(
               overview_file="C:/DSSAT48/Wheat/OVERVIEW.OUT",
               treatments_name=[
                   "164.0 KG N/HA DRY",
                   "82.0 KG N/HA DRY",
               ],
               measured_only=False,
           )

       This returns all variables for the two specified treatments, including
       rows where no measured value is available.
    """

    # Validate overview file using the validate_file() function
    validated_path = validate_file(overview_file, ".OUT")

    # Get the dictionary with the line ranges for each cultivar
    treatment_dict = simulations_lines(validated_path)  # FIX: use validated_path

    # Initialize an empty DataFrame to store all the data
    overview_df = pd.DataFrame(
        columns=[
            'EXPERIMENT',
            'TREATMENT',
            'TREATMENT_NAME',
            'cultivar',
            'VARIABLE',
            'VALUE_SIMULATED',
            'VALUE_MEASURED'
        ]
    )

    # Handle the optional list of variables
    if variables is not None:
        if not isinstance(variables, list):
            variables = [variables]
        if not variables or not all(isinstance(var, str) for var in variables):
            raise ValueError(
                "The 'variables' argument should be a non-empty string or a "
                "list of strings. For example: 'Anthesis (DAP)' or "
                "['Anthesis (DAP)', 'Maturity (DAP)', "
                "'Product wt (kg dm/ha;no loss)', "
                "'Maximum leaf area index']"
            )

    # Handle the optional list of experiments
    if experiments is not None:
        if not isinstance(experiments, list):
            experiments = [experiments]
        if (
                not experiments  # FIX: was 'experimens'
                or not all(isinstance(code, str) for code in experiments)
        ):
            raise ValueError(
                "The 'experiments' argument should be a non-empty string or "
                "a list of strings. For example: 'AZMC9311' or "
                "['AZMC9311', 'AZMC9312']"
            )

    # Handle the optional list of treatment_names
    if treatments is not None:
        if not isinstance(treatments, list):
            treatments = [treatments]
        if (
                not treatments
                or not all(isinstance(tn, (int, str)) for tn in treatments)
        ):
            raise ValueError(
                "The 'treatments' argument should be a non-empty integer "
                "or a list of integers. For example: 1 or [1, 2, 3]."
            )
        # Normalize to strings for comparison
        treatments = [str(tn) for tn in treatments]

    # Handle the optional list of treatment_numbers
    if treatments_name is not None:
        if not isinstance(treatments_name, list):
            treatments_name = [treatments_name]
        # Allow ints or strings; coerce to strings for comparison
        if not treatments_name:
            raise ValueError(
                "The 'treatment_names' argument should be a non-empty string or "
                "a list of strings. For example: '164.0 KG N/HA DRY' or "
                "['164.0 KG N/HA DRY', '82.0 KG N/HA DRY']"
            )

    with open(validated_path, 'r') as file:
        lines = file.readlines()

        # Iterate through each cultivar and extract data
        for treatment_name, blocks in treatment_dict.items():

            # Normalize to a list of (start_line, end_line) ranges
            # (this allows the same treatment_name to appear in more than one experiment)
            if not isinstance(blocks, list):
                blocks = [blocks]

            # Iterate over each block associated with the treatment_name
            for (start_line, end_line) in blocks:

                cultivar_data = []
                experiment_info = None
                model_crop = None
                cultivar = None

                # Extract experiment code from the compleate experiment name
                for i in range(start_line, end_line):
                    line = lines[i].strip()
                    if line.startswith("EXPERIMENT"):
                        experiment = line.split(":")[1].split()[0]

                        # Iterate through the lines in the specified range to find the EXPERIMENT line
                for i in range(start_line, end_line):
                    line = lines[i].strip()

                    # Look for the line containing 'MODEL'
                    if line.startswith("MODEL"):
                        # Extract model and crop names
                        model_crop = line.split(':')[1].strip()

                    if line.startswith('CROP') and 'CULTIVAR :' in line:
                        # Extract CULTIVAR information using split
                        parts = line.split('CULTIVAR :')
                        if len(parts) > 1:
                            cultivar = parts[1].split('ECOTYPE')[0].strip()
                            # Extract everything between 'CULTIVAR :' and 'ECOTYPE'

                    # Extract treatment number
                    if line.strip().startswith('TREATMENT'):
                        treatment = line.split()[1]

                    # Look for the line with simulation results (lines after @)
                    if line.startswith('@'):

                        # Store the header line to return it
                        header_line = line

                        # Extract variable name and simulated and measured values
                        for data_line in lines[i + 1:]:

                            if not data_line.strip() or data_line.startswith('*'):
                                break

                            data_line = data_line.strip().split()
                            variable_name = ' '.join(data_line[:-2])  # Get the variable name
                            simulated_value = data_line[-2]
                            measured_value = data_line[-1]

                            # Replace any value starting with '-99' with an empty string
                            simulated_value = '' if simulated_value.startswith('-99') else simulated_value
                            measured_value = '' if measured_value.startswith('-99') else measured_value

                            # Append the row data
                            cultivar_data.append({
                                'EXPERIMENT': experiment,
                                'TREATMENT': treatment,
                                'TREATMENT_NAME': treatment_name,
                                'cultivar': cultivar,
                                'VARIABLE': variable_name,
                                'VALUE_SIMULATED': simulated_value,
                                'VALUE_MEASURED': measured_value
                            })

                        # Convert to DataFrame and append to overview_df
                        cultivar_df = pd.DataFrame(cultivar_data)
                        overview_df = pd.concat([overview_df, cultivar_df], ignore_index=True)

    # Remove rows where any of the columns 'VARIABLE', 'VALUE_SIMULATED',
    # or 'VALUE_MEASURED' contain '--------'
    overview_df = overview_df[
        ~overview_df[['VARIABLE', 'VALUE_SIMULATED', 'VALUE_MEASURED']]
        .apply(lambda x: x.astype(str).str.contains('--------'))
        .any(axis=1)
    ]

    # Convert the 'VALUE_SIMULATED' and 'VALUE_MEASURED' columns to numeric values
    overview_df['VALUE_SIMULATED'] = pd.to_numeric(overview_df['VALUE_SIMULATED'], errors='coerce')
    overview_df['VALUE_MEASURED'] = pd.to_numeric(overview_df['VALUE_MEASURED'], errors='coerce')

    # Convert all column names to lowercase
    overview_df.columns = overview_df.columns.str.lower()

    # Validate that requested filter values actually exist in the data
    # Check variables
    if variables is not None:  # FIX: guard to avoid iterating over None
        vars_in_data = set(overview_df["variable"].unique())
        missing_vars = [v for v in variables if v not in vars_in_data]
        if missing_vars:
            raise ValueError(
                f"The following variables were not found: {missing_vars}.\n"
                f"Please check spelling and that they exist in the file: {validated_path}."
            )

    # Check experiments (experiment descriptions)
    if experiments is not None:
        exps_in_data = set(overview_df["experiment"].unique())
        missing_exps = [e for e in experiments if e not in exps_in_data]
        if missing_exps:
            raise ValueError(
                f"The following experiments were not found: {missing_exps}.\n"
                f"Please check spelling and that they exist in the file: {validated_path}."
            )

    # Check treatment_names
    if treatments is not None:
        tnumbs_in_data = set(overview_df["treatment"].unique())
        missing_tnumbs = [t for t in treatments if t not in tnumbs_in_data]
        if missing_tnumbs:
            raise ValueError(
                f"The following treatments were not found: {missing_tnumbs}.\n"
                f"Please check spelling and that they exist in the file: {validated_path}."
            )

    # Check treatment_name
    if treatments_name is not None:
        tnames_in_data = set(overview_df["treatments_name"].astype(str).unique())
        missing_tnames = [tn for tn in treatments_name if tn not in tnames_in_data]
        if missing_tnums:
            raise ValueError(
                f"The following treatments_name were not found: {missing_tnames}.\n"
                f"Please check spelling and that they exist in the file: {validated_path}."
            )

    # Apply filters only when the corresponding argument is provided.
    # Each filter is independent and can be combined in any order.
    if variables is not None:
        overview_df = overview_df[overview_df["variable"].isin(variables)]

    if experiments is not None:
        overview_df = overview_df[overview_df["experiment"].isin(experiments)]

    if treatments is not None:
        overview_df = overview_df[overview_df["treatment"].isin(treatments)]  # FIX: filter by name

    if treatments_name is not None:
        overview_df = overview_df[
            overview_df["treatment_name"].astype(str).isin(treatments_name)
        ]  # FIX: filter by number

    # Optionally drop rows without measured values. This is useful when the caller
    # is interested only in cases where observations exist for evaluation.
    if measured_only:
        overview_df = overview_df.dropna(subset=["value_measured"])

    return overview_df