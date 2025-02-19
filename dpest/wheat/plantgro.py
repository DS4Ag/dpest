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
    Create a PEST instructions (.ins) file for time series data.

    Args:
        - plantgro_file_path (str): Path to the PlantGro.OUT file
        - treatment (str): Treatment name
        - variables (list): variable or list of variables to process
        - output_path (str, optional): Path to save the output file. If None, uses current working directory.
        - variable_classifications (dict, optional): Mapping of variable names to their respective categories.
                                                   Defaults to values from the YAML configuration if not provided.
        - plantgro_ins_first_line (str, optional): The first line of the .ins file. Defaults to the value in the YAML configuration.
        mrk (str, optional): Primary marker delimiter character for the instruction file. Defaults to '~'.
        smk (str, optional): Secondary marker delimiter character for the instruction file. Defaults to '!'.

    Returns:
        - pandas.DataFrame: A filtered DataFrame used to generate the .ins file.
        - str: The path to the created .ins file.

    Raises:
        ValueError: If required arguments are missing or if invalid values are encountered in the input data,
                    such as incorrect parameter formats, missing columns in the overview_observations DataFrame,
                    or invalid output paths.
        FileNotFoundError: If the specified CUL file (or other necessary file paths) does not exist or is incorrect.
        Exception: For any other unexpected errors that occur during the execution of the function, 
                   such as issues with file writing or data processing.
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