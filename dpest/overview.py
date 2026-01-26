import yaml
from dpest.functions import *

def overview(
    treatment=None,
    overview_file_path=None,
    output_path=None,
    suffix=None,
    variables=None,
    variables_classification=None,
    overview_ins_first_line=None,
    mrk="~",
    smk="!",
):
    """
    Creates a ``PEST instruction file (.INS)``. This instruction file contains
    directions for PEST to read the simulated values from the ``OVERVIEW.OUT``
    file and compare them with the corresponding observed values (originally
    entered in the DSSAT "A file"). The ``PEST instruction file (.INS)`` guides
    PEST in extracting specific model-generated observations from the
    ``OVERVIEW.OUT`` file, which includes a list of end-of-season crop
    performance metrics, and critical phenological observations used for model
    evaluation. Additionally, this module creates a tuple containing:

    1. A DataFrame with the MEASURED observations from the ``OVERVIEW.OUT``
       file (originally entered in the DSSAT "A file").
    2. The path to the generated ``PEST instruction file (.INS)``.

    **Required Arguments:**
    =======

        * **treatment** (*str*): The name of the treatment for which the
          cultivar is being calibrated. This should match exactly the treatment
          name as shown in the DSSAT application interface when an experiment
          is selected. For example, ``"164.0 KG N/HA IRRIG"`` is a treatment of
          the ``SWSW7501WH.WHX`` experiment.
        * **overview_file_path** (*str*): Path to the ``OVERVIEW.OUT`` file to
          read. Usually the file is in ``C:\\DSSAT48\\Wheat\\OVERVIEW.OUT``.

    **Optional Arguments:**
    =======

        * **output_path** (*str*, *default: current working directory*):
          Directory where the generated ``PEST instruction file (.INS)`` will
          be saved.
        * **suffix** (*str*, *default: ""*): Suffix to append to the output
          filename and variable names in the .INS file. This short code (e.g.,
          ``TRT1``, ``TRT2``, ``TRT3``) identifies different treatments used
          for calibrating the same cultivar (or ecotype) in the same
          calibration process. It must be 1–4 characters long, containing only
          uppercase letters and/or numbers. For example, if
          ``suffix="TRT1"``, the output file will be named
          ``OVERVIEW_TRT1.ins`` and variable markers will include the suffix
          (e.g., ``!Anthesis_DAP_TRT1!``). This ensures that PEST can
          distinguish between variables from different treatments, as PEST does
          not allow variables with the same name.
        * **variables** (*list* or *str*): Variable(s) from the
          ``OVERVIEW.OUT`` file that PEST will extract in case the user does
          not want to use all the variables present in the DSSAT “A file” for
          the calibration. The PEST instruction file will use these to read the
          model output. You may specify a single variable as a string (e.g.,
          ``'Anthesis (DAP)'``) or multiple variables as a list (e.g.,
          ``['Anthesis (DAP)', 'Maturity (DAP)', 'Product wt (kg dm/ha;no loss)',``
          ``'Maximum leaf area index', 'Canopy (tops) wt (kg dm/ha)', 'Above-ground N (kg/ha)']``).
        * **variables_classification** (*dict*): Mapping of variable names to
          their respective categories. If provided, it is used directly to
          classify variables. If not provided, the function will attempt to
          load crop- and model-specific classification from a configuration
          file located at ``dpest/<crop>/<model>/arguments.yml``. When
          ``variables_classification`` is ``None``, both **crop** and
          **model** become required arguments.
        * **overview_ins_first_line** (*str*, *default: "pif"*): First line of
          the ``PEST instruction file (.INS)``. This is the PEST default value
          and is obtained from the package configuration file
          (``dpest/arguments.yml``) when not provided by the user.
        * **mrk** (*str*, *default: "~"*): Primary marker delimiter character
          for the instruction file. Must be a single character and cannot be
          A–Z, a–z, 0–9, ``!``, ``[``, ``]``, ``(``, ``)``, ``:``, space, tab,
          or ``&``.
        * **smk** (*str*, *default: "!"*): Secondary marker delimiter character
          for the instruction file. Must be a single character and cannot be
          A–Z, a–z, 0–9, ``[``, ``]``, ``(``, ``)``, ``:``, space, tab, or
          ``&``.

    **Returns:**
    =======

    * *tuple*: A tuple containing:
        * *pandas.DataFrame*: A filtered DataFrame used to generate the
          ``PEST instruction file (.INS)``.
        * *str*: The full path to the generated ``PEST instruction file (.INS)``.

    **Examples:**
    =======

    1. **Basic Usage (Required arguments only, crop/model-based defaults):**

       .. code-block:: python

           from dpest import overview

           overview_observations, overview_ins_path = overview(
               treatment='164.0 KG N/HA DRY',
               overview_file_path='C:/DSSAT48/Wheat/OVERVIEW.OUT',
               crop='wheat',
               model='ceres',
           )

    2. **Specifying Variable Classifications Manually:**

       .. code-block:: python

           from dpest import overview

           overview(
               treatment='164.0 KG N/HA DRY',
               overview_file_path='C:/DSSAT48/Wheat/OVERVIEW.OUT',
               variables=[
                   'Anthesis (DAP)', 'Maturity (DAP)',
                   'Product wt (kg dm/ha;no loss)',
                   'Maximum leaf area index',
                   'Canopy (tops) wt (kg dm/ha)',
                   'Above-ground N (kg/ha)',
               ],
               variables_classification={
                   'Anthesis (DAP)': 'phenology',
                   'Maturity (DAP)': 'phenology',
                   'Product wt (kg dm/ha;no loss)': 'yield',
                   'Maximum leaf area index': 'lai',
                   'Canopy (tops) wt (kg dm/ha)': 'biomass',
                   'Above-ground N (kg/ha)': 'nitrogen',
               },
           )

    """
    # Define YAML keys used in configuration files
    yml_file_block = "OVERVIEW_FILE"
    yaml_file_variables = "INS_FILE_VARIABLES"
    yaml_variables_classification = "VARIABLES_CLASSIFICATION"
    MAX_VAR_LENGTH = 20  # In PEST, the variable names should not exceed 20 characters

    try:
        # Load package-level defaults from dpest/arguments.yml
        current_dir = os.path.dirname(os.path.abspath(__file__))
        arguments_file = os.path.join(current_dir, "arguments.yml")

        if not os.path.isfile(arguments_file):
            raise FileNotFoundError(f"YAML file not found: {arguments_file}")

        with open(arguments_file, "r") as yml_file:
            yaml_data = yaml.safe_load(yml_file)

        # Validate treatment
        if treatment is None:
            raise ValueError(
                "The 'treatment' argument is required and must be specified by the user."
            )

        # Validate marker delimiters using the validate_marker() function
        mrk = validate_marker(mrk, "mrk")
        smk = validate_marker(smk, "smk")
        if mrk == smk:
            raise ValueError("mrk and smk must be different characters.")

        # Load default arguments from the YAML file if not provided
        if overview_ins_first_line is None:
            function_arguments = yaml_data[yaml_file_variables]
            overview_ins_first_line = function_arguments["first_line"]

        # Handle the optional list of variables
        if variables is not None:
            if not isinstance(variables, list):
                variables = [variables]
            if not variables or not all(isinstance(var, str) for var in variables):
                raise ValueError(
                    "The 'variables' should be a non-empty string or a list of "
                    "strings. For example: 'Maturity (DAP)' or "
                    "['Emergence (DAP)', 'Maturity (DAP)', "
                    "'Product wt (kg dm/ha;no loss)']"
                )


        # Validate overview_file_path using the validate_file() function
        validated_path = validate_file(overview_file_path, ".OUT")

        # Read and parse the overview file
        overview_df, header_line, crop_model = extract_simulation_data(validated_path)

        print('CROP MODEL: ', crop_model)

        # Load variables_classification:
        #   - use user-provided dict if given;
        #   - otherwise, obtain crop and model from the .OUT file, and load variables
        #     classification from dpest/<crop>/<model>/arguments.yml
        if variables_classification is None:

            model = crop_model.split('-')[0].strip()[:5]
            crop = crop_model.split('-')[1].strip().lower()

            crop_model_arguments_file = get_crop_model_arguments_file_path(
                crop=crop, model=model
            )
            if not os.path.isfile(crop_model_arguments_file):
                raise FileNotFoundError(
                    f"YAML file not found for crop='{crop}' and model='{model}': "
                    f"{crop_model_arguments_file}"
                )

            with open(crop_model_arguments_file, "r") as cm_yml:
                crop_model_yaml_data = yaml.safe_load(cm_yml)

            try:
                variables_classification = crop_model_yaml_data[yml_file_block][
                    yaml_variables_classification
                ]
            except KeyError as exc:
                raise KeyError(
                    "The crop/model configuration file does not define the "
                    f"'{yml_file_block}.{yaml_variables_classification}' section "
                    f"required by the overview() function."
                ) from exc

        # Filter the DataFrame for the specified treatment
        filtered_df = overview_df.loc[
            (overview_df["treatment"] == treatment)
        ].copy()

        if filtered_df.empty:
            raise ValueError(
                f"No data found for treatment '{treatment}'. "
                "Please check if the treatment exists in the OVERVIEW.OUT file."
            )

        # Map variables to their respective groups
        filtered_df["group"] = filtered_df["variable"].map(variables_classification)

        # Remove rows where 'value_measured' column contains NaN values
        filtered_df = filtered_df.dropna(subset=["value_measured"])

        # Filter variables if a list of variables was provided by the user
        if variables is not None:
            filtered_df = filtered_df[filtered_df["variable"].isin(variables)]

        # Adjust the 'position' column to create 'position_adjusted'
        filtered_df["position_adjusted"] = (
            filtered_df["position"] - filtered_df["position"].shift(1)
        )

        # Ensure the first row retains its original position
        filtered_df.loc[
            filtered_df.index[0], "position_adjusted"
        ] = filtered_df.loc[filtered_df.index[0], "position"]

        # Transform the variable names to fit the max 20 characters required by PEST
        filtered_df = process_variable_names(filtered_df)

        # Validate suffix if provided
        if suffix is not None:
            if not isinstance(suffix, str):
                raise ValueError("Suffix must be a string.")
            if not suffix.isalnum():
                raise ValueError("Suffix must only contain letters and numbers.")
            if len(suffix) > 4:
                raise ValueError("Suffix must be at most 4 characters long.")
            suffix = "_" + suffix  # only add underscore *after* validation

            # Create a dictionary to add the treatment suffix
            replace_dict = add_suffix_to_variables(
                filtered_df["variable_name"], suffix, MAX_VAR_LENGTH
            )
            filtered_df["variable_name"] = filtered_df["variable_name"].map(
                replace_dict
            )

        # Generate the .ins file content
        output_text = ""
        for _, row in filtered_df.iterrows():
            output_text += (
                f"l{row['position_adjusted']} "
                f"{mrk}{row['variable']}{mrk} "
                f"{smk}{row['variable_name']}{smk}\n"
            )

        # Combine the content into the full .ins file structure
        ins_file_content = (
            f"{overview_ins_first_line} {mrk}\n"
            f"{mrk}{treatment}{mrk}\n"
            f"{mrk}{header_line[1:].strip()}{mrk}\n"
            f"{output_text}"
        )

        # Validate output_path
        output_path = validate_output_path(output_path)

        # Determine and validate output_filename
        if suffix:
            output_filename = os.path.basename(validated_path).replace(
                ".OUT", f"{suffix}.ins"
            )
            if not output_filename.lower().endswith(".ins"):
                output_filename += ".ins"
        else:
            output_filename = os.path.basename(validated_path).replace(".OUT", ".ins")

        # Create the path and file name for the new file
        output_new_file_path = os.path.join(output_path, output_filename)

        # Write the generated content to the .ins file
        with open(output_new_file_path, "w") as ins_file:
            ins_file.write(ins_file_content)

        print(f"OVERVIEW.INS file generated and saved to: {output_new_file_path}")

        # Remove non-useful columns from the dataframe to export
        ouput_overview_df = filtered_df[["variable_name", "value_measured", "group"]]
        return ouput_overview_df, output_new_file_path

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except FileNotFoundError as fe:
        print(f"FileNotFoundError: {fe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")