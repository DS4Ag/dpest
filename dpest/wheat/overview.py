import yaml
from dpest.functions import *

def overview(
    treatment = None,
    overview_file_path = None,
    output_path = None,
    variable_classifications = None,
    overview_ins_first_line = None,
    mrk = '~',
    smk = '!',
):
    """
    Creates a ``PEST instruction file (.INS)``. This instruction file contains directions for PEST to read the simulated values from the ``OVERVIEW.OUT`` file and compare them with the corresponding observed values (originally entered in the DSSAT "A file"). The ``PEST instruction file (.INS)`` guides PEST in extracting specific model-generated observations from the ``OVERVIEW.OUT`` file, which includes a list of end-of-season crop performance metrics, and critical phenological observations used for model evaluation. Additionally, this module creates a tuple containing:

    1. A DataFrame with the MEASURED observations from the ``OVERVIEW.OUT`` file (originally entered in the DSSAT "A file").
    2. The path to the generated ``PEST instruction file (.INS)``.

    **Required Arguments:**
    =======

        * **treatment** (*str*): The name of the treatment for which the cultivar is being calibrated. This should match exactly the treatment name as shown in the DSSAT application interface when an experiment is selected. For example, "164.0 KG N/HA IRRIG" is a treatment of the ``SWSW7501WH.WHX`` experiment.
        * **overview_file_path** (*str*): Path to the ``OVERVIEW.OUT`` file to read. Usually the file is in ``C:\DSSAT48\Wheat\OVERVIEW.OUT``.

    **Optional Arguments:**
    =======

        * **output_path** (*str*, *default: current working directory*): Directory where the generated ``PEST instruction file (.INS)`` will be saved.
        * **variable_classifications** (*dict*): Mapping of variable names to their respective categories. If not provided, defaults to a pre-configured classification scheme defined in the package. Users can override this by providing their own dictionary to define the variables from the *MAIN GROWTH AND DEVELOPMENT VARIABLES section of the ``OVERVIEW.OUT`` DSSAT file, using the format ``{variable: variable_group, …}``. Variables group names should be less than 12 characters.
        * **overview_ins_first_line** (*str*, *default: "pif"*): First line of the ``PEST instruction file (.INS)``. This is the PEST default value and should not be changed without good reason.
        * **mrk** (*str*, *default: "~"*) Primary marker delimiter character for the instruction file. Must be a single character and cannot be A-Z, a-z, 0-9, !, [, ], (, ), :, space, tab, or &.
        * **smk** (*str*, *default: "!"*) Secondary marker delimiter character for the instruction file. Must be a single character and cannot be A-Z, a-z, 0-9, [, ], (, ), :, space, tab, or &.

    **Returns:**
    =======

    * *tuple*: A tuple containing:
        * *pandas.DataFrame*: A filtered DataFrame used to generate the ``PEST instruction file (.INS)``.
        * *str*: The full path to the generated ``PEST instruction file (.INS)``.

    **Examples:**
    =======

    1. **Basic Usage (Required Arguments Only):**

       .. code-block:: python

          from dpestool.wheat import overview

          # Call the module with only the required arguments
          overview_observations, overview_ins_path = overview(
              treatment = '164.0 KG N/HA DRY',
              overview_file_path = 'C:/DSSAT48/Wheat/OVERVIEW.OUT'
          )

          # The returned tuple and path are saved in the variables, can be used with any name that the user prefer, to call them later

       This example creates a ``PEST instruction file (.INS)`` using only the required arguments. Note that the returned tuple ``(overview_observations, overview_ins_path)`` is captured. The ``overview_observations`` DataFrame  will be used later to create the observations and observations group sections in the pst file (loaded in the ``dataframe_observations`` argument of the pst module). The ``overview_ins_path`` will be used in the ``input_output_file_pairs`` argument of the pst module to match the original ``OVERVIEW.OUT`` file to the instruction file.

    2. **Specifying Variable Classifications:**

       .. code-block:: python

          from dpestool.wheat import overview

          # Call the module specifying variable classifications
          overview(
              treatment = '164.0 KG N/HA DRY',
              overview_file_path = 'C:/DSSAT48/Wheat/OVERVIEW.OUT',
              variable_classifications = {
                  'Anthesis (DAP)': 'phenology',
                  'Maturity (DAP)': 'phenology',
                  'Product wt (kg dm/ha;no loss)': 'yield',
                  'Maximum leaf area index': 'lai',
                  'Canopy (tops) wt (kg dm/ha)': 'biomass',
                  'Above-ground N (kg/ha)': 'nitrogen'
              }
          )

       This example demonstrates how to specify the ``variable_classifications`` argument to group specific variables. In this case, the returned tuple is not saved, but the ``PEST instruction file (.INS)`` is still created at the specified location. If you want to use the cultivar parameters and path for the ``pst`` module, the returned tuple should be saved in two variables. Additionally, the example shows how the  ``variable_classifications`` optional variable should be entered as a dictionary.
    """

    # Define default variables:
    yml_file_block = 'OVERVIEW_FILE'
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

        # Validate treatment
        if treatment is None:
            raise ValueError("The 'treatment' argument is required and must be specified by the user.")

        # Validate overview_file_path using the validate_file() function
        validated_path = validate_file(overview_file_path, '.OUT')

        # Validate marker delimiters using the validate_marker() function
        mrk = validate_marker(mrk, "mrk")
        smk = validate_marker(smk, "smk")
        # Ensure mrk and smk are different
        if mrk == smk:
            raise ValueError("mrk and smk must be different characters.")

        # Load default arguments from the YAML file if not provided
        if overview_ins_first_line is None:
            function_arguments = yaml_data[yml_file_block][yaml_file_variables]
            overview_ins_first_line = function_arguments['first_line']

        if variable_classifications is None:
            variable_classifications = yaml_data[yml_file_block][yaml_variable_classifications]

        # Read and parse the overview file
        overview_df, header_line = extract_simulation_data(overview_file_path)

        # Filter the DataFrame for the specified treatment and cultivar
        filtered_df = overview_df.loc[
            (overview_df['treatment'] == treatment)
        ].copy()

        # Check if the filtered DataFrame is empty
        if filtered_df.empty:
            raise ValueError(
                f"No data found for treatment '{treatment}'. Please check if the treatment exists in the OVERVIEW.OUT file.")

        # Map variables to their respective groups
        filtered_df['group'] = filtered_df['variable'].map(variable_classifications)

        # Remove rows where 'value_measured' column contains NaN values
        filtered_df = filtered_df.dropna(subset=['value_measured'])

        # Adjust the 'position' column to create 'position_adjusted'
        filtered_df['position_adjusted'] = filtered_df['position'] - filtered_df['position'].shift(1)

        # Ensure the first row retains its original position
        filtered_df.loc[filtered_df.index[0], 'position_adjusted'] = filtered_df.loc[filtered_df.index[0], 'position']

        # Transform the variable names from the OVERVIEW file fit the max 20 characters required by PEST
        filtered_df = process_variable_names(filtered_df)

        # Generate the .ins file content
        output_text = ""
        for _, row in filtered_df.iterrows():
            output_text += f"l{row['position_adjusted']} {mrk}{row['variable']}{mrk} {smk}{row['variable_name']}{smk}\n"

        # Combine the content into the full .ins file structure
        ins_file_content = f"{overview_ins_first_line} {mrk}\n{mrk}{treatment}{mrk}\n{mrk}{header_line[1:].strip()}{mrk}\n{output_text}"

        # Validate output_path
        output_path = validate_output_path(output_path)

        # Create the path and file name for the new file
        output_filename = os.path.basename(overview_file_path).replace('.OUT', '.ins')
        output_new_file_path = os.path.join(output_path, output_filename)

        # Write the generated content to the .ins file
        with open(output_new_file_path, 'w') as ins_file:
            ins_file.write(ins_file_content)

        print(f"OVERVIEW.INS file generated and saved to: {output_new_file_path}")

        # Remove non-useful columns from the dataframe to export
        ouput_overview_df = filtered_df[['variable_name', 'value_measured', 'group']]
        return ouput_overview_df, output_new_file_path

    except ValueError as ve:
        print(f"ValueError: {ve}")
    # except FileNotFoundError as fe:
    #     print(f"FileNotFoundError: {fe}")
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")