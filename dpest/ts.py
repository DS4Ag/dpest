import yaml
from dpest.functions import *

def ts(
    ts_file_path = None,
    treatment = None, 
    variables = None, 
    output_path = None,
    suffix = None,
    variables_classification = None,
    ts_ins_first_line = None,
    mrk = '~',
    smk = '!',
):

    """
    Creates a ``PEST instruction file (.INS)`` for DSSAT **time-series** output
    files. This instruction file contains directions for PEST to read simulated
    time-series values from daily DSSAT outputs (e.g. ``PlantGro.OUT``,
    ``PlantN.OUT``, ``PlantC.OUT``, ``PlantGrf.OUT``, ``SoilNi.OUT``,
    ``SoilWat.OUT``, ``SoilTemp.OUT``) and to match them with the corresponding
    measured values stored in the DSSAT T file.

    The time-series output files supported by this function share a common
    tabular format where the first three columns are::

        @YEAR DOY   DAS

    The ``PEST instruction file (.INS)`` guides PEST in extracting specific
    model-generated observations at specific time points for the variables
    specified by the user. Additionally, this module creates a tuple containing:

    1) A DataFrame with the MEASURED observations (entered by the user in the
       DSSAT T file) for the specified variables.
    2) The path to the generated ``PEST instruction file (.INS)``.

    **Required Arguments**

    * **ts_file_path** (*str*):
        Path to the DSSAT time-series output file to read. This can be any
        daily DSSAT output with ``@YEAR DOY DAS`` as the first three header
        columns, for example:

        - ``C:/DSSAT48/Soybean/PlantGro.OUT``
        - ``C:/DSSAT48/Soybean/PlantN.OUT``
        - ``C:/DSSAT48/Soybean/PlantC.OUT``
        - ``C:/DSSAT48/Soybean/SoilNi.OUT``
        - ``C:/DSSAT48/Soybean/SoilWat.OUT``

    * **treatment** (*str*):
        Name of the treatment for which the cultivar is being calibrated.
        This must match exactly the treatment name as shown in the DSSAT
        interface when an experiment is selected (i.e. the value that appears
        in the ``TREATMENT`` line of the output header).

        Example: ``"164.0 KG N/HA IRRIG"`` or ``"76 Equidist BRAGG"``.

    * **variables** (*list* or *str*):
        Variable code(s) from the DSSAT T file (and thus present in the header
        of the selected time-series output file) that PEST will extract. The
        instruction file uses these codes to read the model output at the
        specified dates.

        - A single variable can be provided as a string, e.g. ``"LAID"``.
        - Multiple variables can be provided as a list, e.g.
          ``["LWAD", "SWAD", "GWAD", "RWAD", "CWAD", "HIAD", "PWAD"]``.

    **Optional Arguments**
    ======================

    * **output_path** (*str*, *default: current working directory*):
        Directory where the generated ``PEST instruction file (.INS)`` will be
        saved. If not provided, the current working directory is used.

    * **suffix** (*str*, *default: ""*):
        Suffix to append to the output filename and variable names in the
        .INS file. This short code (e.g. ``"TRT1"``, ``"TRT2"``) identifies
        different treatments used for calibrating the same cultivar in the same
        calibration process. It must be 1–4 characters long and alphanumeric.

        For example, if ``suffix="TRT1"`` and
        ``ts_file_path="C:/DSSAT48/Wheat/PlantGro.OUT"``, the output
        file will be named ``PlantGro_TRT1.ins`` and markers will look like
        ``!LAID_75167_TRT1!``.

    * **variables_classification** (*dict*, *optional*):
        Mapping of variable codes to their respective categories (groups).
        When provided, this dictionary is used directly, with the format::

            {"LAID": "lai", "CWAD": "biomass", ...}

        When ``variables_classification`` is ``None``, the function loads a
        global classification from the package configuration file
        (``dpest/arguments.yml``, key ``VARIABLES_CLASSIFICATION_GLOBAL``),
        and maps each variable code to its group from that dictionary.

    * **ts_ins_first_line** (*str*, *default: "pif"*):
        First line of the ``PEST instruction file (.INS)``. By default this
        is read from the package configuration (key ``INS_FILE_VARIABLES`` in
        ``dpest/arguments.yml``) when not provided.

    * **mrk** (*str*, *default: "~"*):
        Primary marker delimiter character for the instruction file. Must be a
        single character and cannot be A–Z, a–z, 0–9, ``!``, ``[``, ``]``,
        ``(``, ``)``, ``:``, space, tab, or ``&``.

    * **smk** (*str*, *default: "!"*):
        Secondary marker delimiter character for the instruction file. Must be
        a single character and cannot be A–Z, a–z, 0–9, ``[``, ``]``, ``(``,
        ``)``, ``:``, space, tab, or ``&``.

    **Internal behaviour**
    ======================

    * The function parses the header of the selected time-series file to
      determine the experiment code, model, and crop name for the specified
      treatment.
    * From the crop name and the ``SIMULATION_CROP_MODELS`` section in
      ``dpest/arguments.yml``, it infers the DSSAT crop code (e.g. ``WH``,
      ``SB``, ``MZ``) and constructs the name of the T file as
      ``<EXPCODE>.<CROPCODE>T`` (e.g. ``SWSW7501.WHT``, ``CLMO8501.SBT``).
    * The T file is then read to obtain the measured time-series values for
      the requested variables and dates, which are used to build the DataFrame
      and the .INS file.

    **Returns**
    ===========

    * *tuple*:

        * *pandas.DataFrame*:
            A DataFrame containing the measured values for the selected
            variables and dates, with columns:

            - ``variable_name`` (including date and optional suffix)
            - ``value_measured`` (float)
            - ``group`` (classification group)

        * *str*:
            Full path to the generated ``PEST instruction file (.INS)``.

    **Examples**
    ============

    1. **PlantGro time series (Soybean)**

       .. code-block:: python

          from dpest import ts

          plantgro_observations, plantgro_ins_path = ts(
              treatment='76 Equidist BRAGG',
              pts_file_path='C:/DSSAT48/Soybean/PlantGro.OUT',
              variables=['LWAD', 'SWAD', 'GWAD', 'RWAD', 'CWAD',
                         'HIAD', 'PWAD', 'LN%D', 'SH%D', 'HIPD', 'SLAD'],
          )

       This creates a ``PlantGro.ins`` file and a DataFrame with the measured
       values for the selected plant growth variables for treatment
       ``"76 Equidist BRAGG"``.

    2. **PlantN time series (Soybean)**

       .. code-block:: python

          from dpest import ts

          plantn_observations, plantn_ins_path = ts(
              treatment='76 Equidist BRAGG',
              ts_file_path='C:/DSSAT48/Soybean/PlantN.OUT',
              variables=['LN%D', 'SN%D'],
          )

       This reads nitrogen-related time-series variables from ``PlantN.OUT``
       and creates a matching instruction file and DataFrame. Global variable
       classifications are used unless a custom mapping is supplied.

    3. **Soil water time series**

       .. code-block:: python

          from dpest import ts

          soilwat_observations, soilwat_ins_path = ts(
              treatment='76 Equidist BRAGG',
              ts_file_path='C:/DSSAT48/Soybean/SoilWat.OUT',
              variables=['SW1D', 'SW2D', 'SW3D'],
          )

       This reads daily soil water content in the top layers from
       ``SoilWat.OUT`` and builds a PEST instruction file for those variables.
    """

    # Define default variables:
    yaml_file_variables = 'INS_FILE_VARIABLES'
    yaml_variables_classification = 'VARIABLES_CLASSIFICATION_GLOBAL'
    yaml_sim_models_key = 'SIMULATION_CROP_MODELS'
    MAX_VAR_LENGTH = 20  # In PEST, the variable names should not exceed 20 characters

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

        # Validate yaml_data
        if yaml_data is None:
            raise ValueError("The 'yaml_data' argument is required and must be specified by the user.")

        # Validate marker delimiters using the validate_marker() function
        mrk = validate_marker(mrk, "mrk")
        smk = validate_marker(smk, "smk")
        # Ensure mrk and smk are different
        if mrk == smk:
            raise ValueError("mrk and smk must be different characters.")

        # Validate variables_classification
        if variables_classification is None:
            variables_classification = yaml_data[yaml_variables_classification]

        if ts_ins_first_line is None:
            # Load default arguments from the YAML file if not provided
            function_arguments = yaml_data[yaml_file_variables]
            ts_ins_first_line = function_arguments['first_line']

        # Validate ts_file_path
        validated_path = validate_file(ts_file_path, '.OUT')

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
        t_df.to_csv('t_df.csv', index=False)

        # Load and filter data for all variables
        dates_variable_values_dict = filter_dataframe(t_df, treatment, treatment_number_name, variables)

        # Check if the filter_dataframe returned an empty dictionary (indicating an error)
        if not dates_variable_values_dict:
            raise ValueError(f"No valid data found for treatment '{treatment}' with variables {variables}")

        # Get the header and first simulation date
        header_line, date_first_sim = get_header_and_first_sim(validated_path)

        # Calculate days dictionary days after first simulation
        days_dict = calculate_days_dict(dates_variable_values_dict, date_first_sim)

        # adjust the days after first simulation
        adjusted_days_dict = adjust_days_dict(days_dict)

        # Validate suffix if provided
        if suffix is not None:
            if not suffix.isalnum():
                raise ValueError("Suffix must only contain letters and numbers.")
            if len(suffix) > 4:
                raise ValueError("Suffix must be at most 4 characters long.")
            suffix = '_' + suffix

        # Process each variable and generate output text
        output_text = ""

        if suffix is not None:
            for date, (days, variables) in adjusted_days_dict.items():
                positions = find_variable_position(header_line, variables)
                line = f"l{days}"
                current_position = 1  # Start at position 1 after 'l{days}'

                for variable in sorted(positions, key=positions.get):
                    position = positions[variable]
                    w_count = position - current_position
                    line += ' w' * w_count + f" {smk}{variable}_{date}{suffix}{smk}"
                    current_position = position + 1  # Move to next position after this variable

                output_text += line + "\n"

        else:
            for date, (days, variables) in adjusted_days_dict.items():
                positions = find_variable_position(header_line, variables)
                line = f"l{days}"
                current_position = 1  # Start at position 1 after 'l{days}'

                for variable in sorted(positions, key=positions.get):
                    position = positions[variable]
                    w_count = position - current_position
                    line += ' w' * w_count + f" {smk}{variable}_{date}{smk}"
                    current_position = position + 1  # Move to next position after this variable

                output_text += line + "\n"

        # Validate output_path
        output_path = validate_output_path(output_path)

        # Determine and validate output_filename
        if suffix:
            # Extract the file name
            output_filename = os.path.basename(validated_path).replace('.OUT', f'{suffix}.ins')

            # Ensure it ends with '.ins'
            if not output_filename.lower().endswith('.ins'):
                output_filename += '.ins'
        else:
            # Default behavior if output_filename not provided
            output_filename = os.path.basename(validated_path).replace('.OUT', '.ins')

        # Create output text file
        ts_ins_file_path = os.path.join(output_path, output_filename)

        # Construct the content for the new .ins file
        ins_file_content = f"{ts_ins_first_line} {mrk}\n{mrk}{treatment}{mrk}\n{mrk}{header_line[1:].strip()}{mrk}\n{output_text}"

        #--------- GET THE GROUP NAME OF THE VARIABLES
        dates_variable_values_data = [
            {
                'date': date,
                'variable': variable,
                'value_measured': value,
                'variable_name': f"{variable}_{date}"
            }
            for date, variables in dates_variable_values_dict.items()
            for variable, value in variables.items()
        ]

        # Create the DataFrame
        dates_variable_values_df = pd.DataFrame(dates_variable_values_data)

        # Map variables to their respective groups
        dates_variable_values_df['group'] = dates_variable_values_df['variable'].map(variables_classification)

        # Convert 'value_measured' column to float
        dates_variable_values_df['value_measured'] = dates_variable_values_df['value_measured'].astype(float)

        # Add the siffix to the variable_name
        if suffix is not None:
            dates_variable_values_df['variable_name'] = dates_variable_values_df['variable_name'] + suffix

        # Select and reorder the columns
        result_df = dates_variable_values_df[['variable_name', 'value_measured', 'group']]

        # Write the content to the .ins file
        with open(ts_ins_file_path, 'w') as ins_file:
            ins_file.write(ins_file_content)

        print(f"{output_filename} file generated and saved to: {ts_ins_file_path}")

        return result_df, ts_ins_file_path

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except FileNotFoundError as fe:
        print(f"FileNotFoundError: {fe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")