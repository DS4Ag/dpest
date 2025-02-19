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
    Create a PEST instruction (.ins) file from an OVERVIEW.OUT file based on specified filters.

    Args:
        treatment (str): The treatment to filter the data. (Required)
        overview_file_path (str): Path to the OVERVIEW.OUT file to read. (Required)
        output_path (str, optional): Directory where the generated .ins file will be saved.
                                     Defaults to the current working directory if not provided.
        variable_classifications (dict, optional): Mapping of variable names to their respective categories.
                                                   Defaults to values from the YAML configuration if not provided.      
        overview_ins_first_line (str, optional): The first line of the .ins file. Defaults to the value in the YAML configuration.
        mrk (str, optional): Primary marker delimiter character for the instruction file. Defaults to '~'.
        smk (str, optional): Secondary marker delimiter character for the instruction file. Defaults to '!'.

    Returns:
        pandas.DataFrame: A filtered DataFrame used to generate the .ins file.
        str: The full path to the generated TPL file (output_new_file_path).

    Raises:
        ValueError: If any required parameters are missing or invalid.
        FileNotFoundError: If the OVERVIEW.OUT file cannot be found.
        Exception: For any other unexpected errors.
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