from dpest.functions import *

def uts(
        uts_file_path=None,
        treatment=None,
        variables=None,
        nspaces_year_header=None,
        nspaces_doy_header = None,
        nspaces_columns_header = None,
):
    """
    Updates DSSAT **time-series** output (``.OUT``) files by adding rows to ensure that simulated values exist for all measured
    observation dates. This situation arises during the calibration process when PEST attempts to compare a measured
    value from the DSSAT "T file" to a corresponding simulated value in the ` **time-series** output (``.OUT``) file. If the simulation
    ends *before* the date of a measured observation, PEST will terminate the calibration process due to a missing
    observation error. This often occurs when measurements, such as remote sensing data, are taken close to the plant's
    maturity phase.

    This module addresses this issue by adding rows to the  **time-series** output (``.OUT``) file file with default values (0),
    extending the simulation period to cover all measured observation dates. The format of the time-series file is preserved. The first three columns must be::

        @YEAR DOY   DAS

    and the remaining columns correspond to daily simulated variables (for example, from
    ``PlantGro.OUT``, ``PlantN.OUT``, ``PlantC.OUT``, ``PlantGrf.OUT``, ``SoilNi.OUT``,
    ``SoilWat.OUT``, ``SoilTemp.OUT``).

    **Example Scenario:**
    =======

    Suppose the ``PlantGro.OUT`` simulation results extend to the year 2022 and day of year (DOY) 102.

    However, the DSSAT "T file" contains measurements for the same treatment with the following dates:

    * 2022 DOY 031
    * 2022 DOY 046
    * 2022 DOY 060
    * 2022 DOY 070
    * 2022 DOY 083
    * 2022 DOY 095
    * 2022 DOY 109

    In this case, PEST  will throw an error and terminate the calibration because the because the time-series
    output file does not contain information for the last ``DOY`` variable. The ``uts()``
    module adds the time series for the days that do not have an observation. The last row added with some
    values are similar to:

    .. code-block:: none

       2022  103   224     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0

    **Required Arguments:**
    =======

        * **uts_file_path** (*str*):
          Path to the DSSAT time-series output (``.OUT``) file to update. This can be any
          daily DSSAT output with ``@YEAR DOY DAS`` as the first three header columns, for example:

          - ``C:/DSSAT48/Wheat/PlantGro.OUT``
          - ``C:/DSSAT48/Wheat/PlantN.OUT``
          - ``C:/DSSAT48/Wheat/PlantC.OUT``
          - ``C:/DSSAT48/Wheat/SoilNi.OUT``
          - ``C:/DSSAT48/Wheat/SoilWat.OUT``

        * **treatment** (*str*): The name of the treatment for which the cultivar is being calibrated. This should
        match exactly the treatment name as shown in the DSSAT application interface when an experiment is selected.
        For example, "164.0 KG N/HA IRRIG" is a treatment of the ``SWSW7501WH.WHX`` experiment.
        * **variables** (*list* or *str*): Variable(s) from the DSSAT "T file" (and thus present in the time-series output file)
        that PEST will extract. The PEST instruction file will use these to read the model output. You may specify a
        single variable as a string (e.g., ``'LAID'``) or multiple variables as a list (e.g., ``['LAID', 'CWAD', 'T#AD']``).

    **Optional Arguments:**
    =======

        * **nspaces_year_header** (*int*, *default: 5*): Number of spaces reserved for the year header in
        the ``.OUT`` file. It is unlikely that the format of the ``.OUT`` file changes in a way that
        necessitates modifying this value.
        * **nspaces_doy_header** (*int*, *default: 4*): Number of spaces reserved for the day-of-year header in
        the ``.OUT`` file. It is unlikely that the format of the time-series output files changes in a way
        that necessitates modifying this value.
        * **nspaces_columns_header** (*int*, *default: 6*): Number of spaces reserved for other columns in the
        ``.OUT`` file. It is unlikely that the format of the time-series output files changes in a way that
        necessitates modifying this value.

    **Returns:**
    =======

        * ``None``

    **Examples:**
    =======

    1. **Basic Usage (List of variables):**

       .. code-block:: python

          from dpest import uts

          uts(
              plantgro_file_path='C:/DSSAT48/Wheat/PlantGro.OUT',
              treatment='164.0 KG N/HA IRRIG',
              variables=['LAID', 'CWAD', 'T#AD']
          )

       This example demonstrates the basic usage of the module with a list of variables (``LAID``, ``CWAD``, and ``T#AD``).
       If the simulation end date in the existing ``PlantGro.OUT`` file is earlier than the latest measurement date in
       the DSSAT "T file", then the ``PlantGro.OUT`` file will be extended by adding new rows. The values of all variables
       present in the ``PlantGro.OUT`` file will be set to ``0`` in the added rows.

    2. **Basic Usage (Single variable):**

       .. code-block:: python

          from dpest import uts

          uts(
              plantgro_file_path='C:/DSSAT48/Wheat/PlantGro.OUT',
              treatment='164.0 KG N/HA IRRIG',
              variables='LAID'
          )

       This example demonstrates the basic usage of the module when only one variable (``LAID``) is specified. If the
       simulation end date in the existing ``PlantGro.OUT`` file is earlier than the latest measurement date in the
       DSSAT "T file", then the ``PlantGro.OUT`` file will be extended by adding new rows. The values of all variables
       present in the ``PlantGro.OUT`` file will be set to 0 in the added rows.
    """
    rows_added = 0  # Initialize
    yaml_sim_models_key = 'SIMULATION_CROP_MODELS'

    try:
        ## Get the yaml_data
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to arguments.yml
        arguments_file = os.path.join(current_dir, 'arguments.yml')
        # Ensure the YAML file exists
        if not os.path.isfile(arguments_file):
            raise FileNotFoundError(f"YAML file not found: {arguments_file}")
        # Load YAML configuration
        with open(arguments_file, 'r') as yml_file:
            yaml_data = yaml.safe_load(yml_file)

        # Validate uts_file_path
        validated_path = validate_file(uts_file_path, '.OUT')

        # Validate treatment
        if not treatment or not isinstance(treatment, str):
            raise ValueError("The 'treatment' must be a non-empty string.")

        # Convert 'variables' to a list if it's not already a list
        if not isinstance(variables, list):
            variables = [variables]

        # Validate that 'variables' is a non-empty list of strings
        if not variables or not all(isinstance(var, str) for var in variables):
            raise ValueError(
                "The 'variables' should be a non-empty string or a list of strings. For example: 'LAID' or ['LAID', 'CWAD']")

        # Assign default values if None and validate integer input
        if nspaces_year_header is None:
            nspaces_year_header = 5
        elif not isinstance(nspaces_year_header, int):
            raise ValueError("nspaces_year_header must be an integer.")

        if nspaces_doy_header is None:
            nspaces_doy_header = 4
        elif not isinstance(nspaces_doy_header, int):
            raise ValueError("nspaces_doy_header must be an integer.")

        if nspaces_columns_header is None:
            nspaces_columns_header = 6
        elif not isinstance(nspaces_columns_header, int):
            raise ValueError("nspaces_columns_header must be an integer.")

        # Get treatment range
        treatment_range = simulations_lines(validated_path)[treatment]

        # Read growth file
        ts_file_df = read_growth_file(validated_path, treatment_range)

        # Get treatment number
        treatment_dict = simulations_lines(validated_path)

        # Get dictionaries with treatment name, treatement number, treatment and experiment code
        treatment_number_name, treatment_experiment_name, treatment_crop_name = \
            extract_treatment_info_plantgrowth(validated_path, treatment_dict)

        crop_name_from_header = treatment_crop_name.get(treatment)
        if crop_name_from_header is None:
            raise ValueError(f"Could not determine crop name for treatment '{treatment}'.")

        # Load simulation crop/model mappings
        sim_models = yaml_data.get(yaml_sim_models_key, {})

        # Find the crop entry whose alias list (lower‑cased) contains crop_name_from_header
        crop_code = None
        for crop_key, crop_info in sim_models.items():
            aliases = [a.lower() for a in crop_info.get('crop_aliases', [])]
            if crop_name_from_header.lower() in aliases:
                crop_code = aliases[1] if len(aliases) > 1 else aliases[0]
                break

        if crop_code is None:
            raise ValueError(
                f"Could not infer crop code from crop name '{crop_name_from_header}'. "
                "Check SIMULATION_CROP_MODELS in arguments.yml."
            )

        experiment_code = treatment_experiment_name.get(treatment)
        if experiment_code is None:
            raise ValueError(f"Could not determine experiment code for treatment '{treatment}'.")

        # Build T‑file name: <EXPCODE><CROPCODE>T, e.g. SWSW7501 + WH + T -> SWSW7501WHT
        t_file_name = f"{experiment_code}.{crop_code.upper()}T"
        t_file_path = os.path.join(os.path.dirname(validated_path), t_file_name)

        # Get the dataframe from the T file data
        t_df = wht_filedata_to_dataframe(t_file_path)

        # Load and filter data for all variables and get the measured year
        dates_variable_values_dict = filter_dataframe(t_df, treatment, treatment_number_name, variables)

        # Check if the filter_dataframe returned an empty dictionary (indicating an error)
        if not dates_variable_values_dict:
            raise ValueError(f"No valid data found for treatment '{treatment}' with variables {variables}")

        # Get the year and day of the year and join it as one unique number
        year_sim = int(str(ts_file_df['@YEAR'].iloc[-1]) + f"{ts_file_df['DOY'].iloc[-1]:03}")

        # Handle both 4-digit and 2-digit years for year_measured
        year_measured_key_str = str(list(dates_variable_values_dict.keys())[-1])

        if len(year_measured_key_str) == 5:  # If year_measured has a 2-digit year
            year_measured_year = int(year_measured_key_str[:2])
            doy_measured = int(year_measured_key_str[2:])

            # Determine the correct century for the 2-digit year
            century = year_sim // 100000  # Get the century from year_sim
            year_measured = int(f"{century}{year_measured_year:02d}{doy_measured:03d}")
        else:  # If year_measured has a 4-digit year
            year_measured = int(year_measured_key_str)

        # Create the new rows to insert
        if year_sim < year_measured:
            number_rows_add = year_measured - year_sim

            # Get the new rows using the new_rows() function
            new_rows = new_rows_add(ts_file_df, number_rows_add)

            # Read the existing file and store its contents
            with open(uts_file_path, 'r') as file:
                lines = file.readlines()

            # Identify the line where the headers are defined (e.g., '@YEAR')
            header_line = next(line for line in lines if '@YEAR' in line)

            # Extract column headers to maintain correct order
            headers = header_line.strip().split()

            # Convert each dictionary into a formatted row string
            new_rows_dic = []
            for row_data in new_rows:
                row = (
                        str(row_data.get('@YEAR', 0)).rjust(nspaces_year_header) +
                        str(row_data.get('DOY', 0)).rjust(nspaces_doy_header) +
                        ''.join(str(row_data.get(col, 0)).rjust(nspaces_columns_header) for col in headers if
                                col not in ['@YEAR', 'DOY']) +
                        '\n'
                )
                new_rows_dic.append(row)

            # Add new rows to the lines list
            lines[treatment_range[1]:treatment_range[1]] = new_rows_dic

            # Update the rows_added counter
            rows_added = len(new_rows)

            # Write the updated content back to the file
            with open(validated_path, 'w') as file:
                file.writelines(lines)

            # Add messages about rows added (now inside the try block)
        if rows_added > 0:
            print(f"{validated_path} update: {rows_added} row{'s' if rows_added > 1 else ''} added successfully.")
        else:
            print(f"{validated_path} status: No update required.")

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except FileNotFoundError as fe:
        print(f"FileNotFoundError: {fe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")