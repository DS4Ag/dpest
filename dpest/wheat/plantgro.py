import yaml
from dpest.functions import *

def plantgro(
    plantgro_file_path = None,
    treatment = None, 
    variables = None, 
    output_path = None,
    variable_classifications = None,
    plantgro_ins_first_line = None,
    mrk = '~',
    smk = '!',
):
    """
    Creates a ``PEST instruction file (.INS)``. This instruction file contains directions for PEST to read the simulated time-series values from the ``PlantGro.OUT`` file, which includes various plant growth metrics throughout the growing season. The  ``PEST instruction file (.INS)`` guides PEST in extracting specific model-generated observations for specific time points from the ``PlantGro.OUT`` file for the variables specified by the user. Additionally, this module creates a tuple containing: 1) A DataFrame with the MEASURED observations (entered by the user in the DSSAT "T file") for the specified variables, and 2) the path to the generated ``PEST instruction file (.INS)``.

    **Required Arguments:**
    =======

        * **plantgro_file_path** (*str*): Path to the ``PlantGro.OUT`` file to read. Usually located in ``C:\DSSAT48\Wheat\PlantGro.OUT``.
        * **treatment** (*str*): The name of the treatment for which the cultivar is being calibrated. This should match exactly the treatment name as shown in the DSSAT application interface when an experiment is selected. For example, "164.0 KG N/HA IRRIG" is a treatment of the ``SWSW7501WH.WHX`` experiment.
        * **variables** (*list* or *str*): Variable(s) from the DSSAT "T file" (and thus present in the PlantGro.OUT file) that PEST will extract. The PEST instruction file will use these to read the model output. You may specify a single variable as a string (e.g., ``'LAID'``) or multiple variables as a list (e.g., ``['LAID', 'CWAD', 'T#AD']``).

    **Optional Arguments:**
    =======

        * **output_path** (*str*, *default: current working directory*): Directory where the generated ``PEST instruction file (.INS)`` will be saved.
        * **variable_classifications** (*dict*): Mapping of ``variable`` names to their respective categories. If not provided, defaults to a pre-configured classification scheme defined in the package. Users can override this by providing their own dictionary in the format ``{variable: variable_group, …}``. Variables group names should be less than 12 characters.
        * **plantgro_ins_first_line** (*str*, *default: "pif"*): First line of the ``PEST instruction file (.INS)``. This is the PEST default value and should not be changed without good reason.
        * **mrk** (*str*, *default: "~"*): Primary marker delimiter character for the instruction file. Must be a single character and cannot be A-Z, a-z, 0-9, !, [, ], (, ), :, space, tab, or &.
        * **smk** (*str*, *default: "!"*): Secondary marker delimiter character for the instruction file. Must be a single character and cannot be A-Z, a-z, 0-9, [, ], (, ), :, space, tab, or &.

    **Returns:**
    =======

    * *tuple*: A tuple containing:
        * *pandas.DataFrame*: A filtered DataFrame used to generate the ``PEST instruction file (.INS)``.
        * *str*: The full path to the generated ``PEST instruction file (.INS)``.

    **Examples:**
    =======

    1. **Basic Usage (Multiple Variables):**

       .. code-block:: python

          from dpestool.wheat import plantgro

          # Call the module with multiple variables
          plantgro_observations, plantgro_ins_path = plantgro(
              plantgro_file_path = 'C:/DSSAT48/Wheat/PlantGro.OUT',
              treatment = '164.0 KG N/HA IRRIG',
              variables = ['LAID', 'CWAD', 'T#AD']
          )

          # The returned tuple and path are saved in the variables, can be used with any name that the user prefer, to call them later

       This example creates a ``PEST instruction file (.INS)`` for multiple variables from the ``PlantGro.OUT`` file. Note that the returned tuple ``(plantgro_observations, plantgro_ins_path)`` is captured. The ``plantgro_observations`` DataFrame will be used later to create the observations and observations group sections in the pst file (to be loaded in the ``dataframe_observations`` argument of the pst module). The ``plantgro_ins_path`` will be used in the ``input_output_file_pairs`` argument of the pst module to match the original ``PlantGro.OUT`` file to the instruction file when creating the PST control file.

    2. **Single Variable Usage:**

       .. code-block:: python

          from dpestool.wheat import plantgro

          # Call the module with a single variable
          plantgro_observations, plantgro_ins_path = plantgro(
              plantgro_file_path = 'C:/DSSAT48/Wheat/PlantGro.OUT',
              treatment = '164.0 KG N/HA IRRIG',
              variables = 'LAID',
              variable_classifications = {
                  'LAID': 'lai'
              }
          )

       This example demonstrates how to use the module with a single variable. The ``variables`` argument can accept either a list of strings or a single string. Note that the returned tuple ``(plantgro_observations, plantgro_ins_path)`` is captured, which will be used later in the ``PEST control file (.PST)`` creation process.
    """

    # Define default variables:
    yml_file_block = 'PLANTGRO_FILE'
    yaml_file_variables = 'INS_FILE_VARIABLES'
    yaml_variable_classifications = 'VARIABLE_CLASSIFICATIONS'

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

        # Validate plantgro_file_path
        validate_file(plantgro_file_path, '.OUT')

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

        # Validate variable_classifications
        if variable_classifications is None:
            variable_classifications = yaml_data[yml_file_block][yaml_variable_classifications]

        if plantgro_ins_first_line is None:
            # Load default arguments from the YAML file if not provided
            function_arguments = yaml_data[yml_file_block][yaml_file_variables]
            plantgro_ins_first_line = function_arguments['first_line']

        # Get treatment number
        treatment_dict = simulations_lines(plantgro_file_path)

        # Get dictionaries with treatment name and treatement number, and treatment and experiment code
        treatment_number_name, treatment_experiment_name = extract_treatment_info_plantgrowth(plantgro_file_path, treatment_dict)

        # Make the path for the WHT file
        wht_file_path = os.path.join(os.path.dirname(plantgro_file_path),  treatment_experiment_name.get(treatment) + '.WHT')

        # Get the dataframe from the WHT file data
        wht_df = wht_filedata_to_dataframe(wht_file_path)

        # Load and filter data for all variables
        dates_variable_values_dict = filter_dataframe(wht_df, treatment, treatment_number_name, variables)

        # Check if the filter_dataframe returned an empty dictionary (indicating an error)
        if not dates_variable_values_dict:
            raise ValueError(f"No valid data found for treatment '{treatment}' with variables {variables}")

        # Get the header and first simulation date
        header_line, date_first_sim = get_header_and_first_sim(plantgro_file_path)

        # Calculate days dictionary and adjust it
        days_dict = calculate_days_dict(dates_variable_values_dict, date_first_sim)

        adjusted_days_dict = adjust_days_dict(days_dict)

        # Process each variable and generate output text
        output_text = ""

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

        # Create output text file
        plantgro_ins_filename = os.path.basename(plantgro_file_path).replace('.OUT', '.ins')
        plantgro_ins_file_path = os.path.join(output_path, plantgro_ins_filename)

        # Construct the content for the new .ins file
        ins_file_content = f"{plantgro_ins_first_line} {mrk}\n{mrk}{treatment}{mrk}\n{mrk}{header_line[1:].strip()}{mrk}\n{output_text}"

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
        dates_variable_values_df['group'] = dates_variable_values_df['variable'].map(variable_classifications)

        # Convert 'value_measured' column to float
        dates_variable_values_df['value_measured'] = dates_variable_values_df['value_measured'].astype(float)

        # Select and reorder the columns
        result_df = dates_variable_values_df[['variable_name', 'value_measured', 'group']]

        # Write the content to the .ins file
        with open(plantgro_ins_file_path, 'w') as ins_file:
            ins_file.write(ins_file_content)

        print(f"PlantGro.INS file generated and saved to: {plantgro_ins_file_path}")

        return result_df, plantgro_ins_file_path

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except FileNotFoundError as fe:
        print(f"FileNotFoundError: {fe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")