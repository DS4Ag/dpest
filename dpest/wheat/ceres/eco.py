import yaml
from dpest.functions import *

def eco(
    ecotype = None,
    eco_file_path = None,
    output_path = None,
    new_template_file_extension = None,
    header_start = None,
    tpl_first_line = None,
    minima = None,
    maxima = None,
    mrk = '~',
    **parameters_grouped
):
    """
    Creates a ``PEST template file (.TPL)`` for CERES-Wheat ecotype parameters based on a ``DSSAT ecotype file (.ECO)``. This module is specific to the CERES-Wheat model and uses default values tailored for this model.

    **Required Arguments:**
    =======

        * **ecotype** (*str*): Ecotype ID to modify. This should match the ``ECO#`` (ecotype ID) column in the ``DSSAT ecotype file (.ECO)``
        * **eco_file_path** (*str*): Full path to the ``DSSAT ecotype (.ECO)`` file. Typically, this is the path to the ``WHCER048.ECO`` file, usually located at ``C:\DSSAT48\Genotype\WHCER048.ECO``.

    **Optional Arguments:**
    =======

        * **output_path** (*str*, *default: current working directory*): Directory to save the generated ``PEST template file (.TPL)``.
        * **new_template_file_extension** (*str*, *default: ".TPL"*): Extension for the generated ``PEST template file (.TPL)``. This is the PEST default value and should not be changed without good reason.
        * **header_start** (*str*, *default: "@ECO#"*): Identifier for the header row in the ``DSSAT ecotype file (.ECO)``.
        * **tpl_first_line** (*str*, *default: "ptf"*): First line to include in the  ``PEST template file (.TPL)``. This is the PEST default value and should not be changed without good reason.
        * **minima** (*str*, *default: "999991"*): Row identifier for the minima ecotype parameter values.
        * **maxima** (*str*, *default: "999992"*): Row identifier for the maxima ecotype parameter values.
        * **mrk** (*str*, *default: "~"*) Primary marker delimiter character for the template file. Must be a single character and cannot be A-Z, a-z, 0-9, !, [, ], (, ), :, space, tab, or &.
        * **parameters_grouped** (*dict*, *optional*): Parameters to calibrate, grouped and comma-separated. If not provided, all ecotype parameters are calibrated. For example: ``PHEN='P1, P2FR1', VERN='VEFF'``. 'PHEN' and 'VERN' are ecotype parameter group names, and the values are the specific ecotype parameters to calibrate, using the same names as in the ``DSSAT ecotype file (.ECO)``. Parameter group names should be less than 12 characters.

    **Returns:**
    =======

    * *tuple*: A tuple containing:
        * *dict*: A dictionary containing:
            * ``'parameters'``: Current ecotype parameter values for the specified ecotype.
            * ``'minima_parameters'``: Minima values for all ecotype parameters.
            * ``'maxima_parameters'``: Maxima values for all ecotype parameters.
            * ``'parameters_grouped'``: The grouped ecotype parameters used for template generation.
        * *str*: The full path to the generated .TPL file.

    **Examples:**
    =======

    1. **Basic Usage (Required Arguments Only):**

       .. code-block:: python

          from dpestool.wheat.ceres import eco

          # Call the module with only the required arguments
          ecotype_parameters, ecotype_tpl_path = eco(
              ecotype = 'CAWH01',
              eco_file_path = 'C:/DSSAT48/Genotype/WHCER048.ECO'
          )

          # The returned tuple and path are saved in the variables, can be used with any name that the user prefer, to call them later

       This example creates a template file using only the required arguments. Note that the returned tuple ``(ecotype_parameters, ecotype_tpl_path)`` is captured. The ``ecotype_parameters`` dictionary will be used later to make the control file's parameter groups and parameters sections using the ``pst`` module. The ``ecotype_tpl_path`` path will be used in the ``input_output_file_pairs`` argument of the ``pst`` module to match the original ``DSSAT ecotype file (.ECO)`` to the template file.

    2. **Specifying Parameter Groups (Tuple Not Saved):**

       .. code-block:: python

          from dpestool.wheat.ceres import eco

          # Call the module specifying parameter groups, but not saving the returned tuple
          eco(
              ecotype = 'CAWH01',
              eco_file_path = 'C:/DSSAT48/Genotype/WHCER048.ECO',
              PHEN = 'P1, P2FR1',
              VERN = 'VEFF'
          )

       This example demonstrates how to specify the ``parameters_grouped`` argument to calibrate only specific ecotype parameters. In this case, the returned tuple is not saved, but the ``PEST template file (.TPL)`` is still created at the specified location. If you want to use the ecotype parameters and path for the ``pst`` module, the returned tuple should be saved with the names that the user prefer.
    """

    # Defaul variable values
    yml_ecotype_block = 'ECOTYPE_TPL_FILE'
    yaml_file_variables = 'FILE_VARIABLES'
    yaml_parameters = 'PARAMETERS'

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

        # Validate inputs
        if ecotype is None:
            raise ValueError("The 'ecotype' argument is required and must be specified by the user.")

        # Validate eco_file_path
        validated_path = validate_file(eco_file_path, '.ECO')

        # Get the ecotype template file variables
        function_arguments = yaml_data[yml_ecotype_block][yaml_file_variables]

        # Validate marker delimiters using the validate_marker() function
        mrk = validate_marker(mrk, "mrk")

        if new_template_file_extension is None:
            new_template_file_extension = function_arguments['new_template_file_extension']

        if header_start is None:
            header_start = function_arguments['header_start']

        if tpl_first_line is None:
            tpl_first_line = function_arguments['tpl_first_line']

        if minima is None:
            minima = str(function_arguments['minima'])

        if maxima is None:
            maxima = str(function_arguments['maxima'])
            
        if parameters_grouped == {}:
            parameters_grouped = yaml_data[yml_ecotype_block][yaml_parameters]
            parameters_grouped = {key: ', '.join(value) for key, value in parameters_grouped.items()}

        # Combine all the groups of parameters into a list
        parameters = []
        for key, value in parameters_grouped.items():
            group_parameters = [param.strip() for param in value.split(',')]  # Strip spaces from each parameter
            parameters.extend(group_parameters)  # Add the group parameters to the main list

        # Read the ECO file
        file_content = read_dssat_file(eco_file_path)
        lines = file_content.split('\n')

        # Locate header and target lines
        header_line_number = next(idx for idx, line in enumerate(lines) if line.startswith(header_start))
        header_line = lines[header_line_number]

        # Get the number of the line that contains the parameters of the specified ecotype
        ecotype_line_number = find_ecotype(file_content, header_start, ecotype, eco_file_path)
        if isinstance(ecotype_line_number, str):  # Error message returned
            raise ValueError(ecotype_line_number)
        minima_line_number = find_ecotype(file_content, header_start, minima, eco_file_path)
        if isinstance(minima_line_number, str):  # Error message returned
            raise ValueError(minima_line_number)
        maxima_line_number = find_ecotype(file_content, header_start, maxima, eco_file_path)
        if isinstance( maxima_line_number, str):  # Error message returned
            raise ValueError( maxima_line_number)

        # Extract parameter values for ecotype, minima, and maxima
        def extract_parameter_values(line_number):
            parameter_values = {}
            for parameter in parameters:
                try:
                    par_position = find_parameter_position(header_line, parameter)
                    parameter_value = lines[line_number][par_position[0]:par_position[1] + 1].strip()
                    parameter_values[parameter] = parameter_value
                except Exception:
                    raise ValueError(f"Parameter '{parameter}' does not exist in the header line of {eco_file_path}.")
            return parameter_values


        # Delete extra spaces on the parameter values
        def clean_parameter_values(parameter_dict):
            cleaned_dict = {}
            for key, value in parameter_dict.items():
                if isinstance(value, str) and '   ' in value:
                    cleaned_dict[key] = value.split()[1]
                else:
                    cleaned_dict[key] = value
            return cleaned_dict

        minima_parameter_values = clean_parameter_values(extract_parameter_values(minima_line_number))
        maxima_parameter_values = clean_parameter_values(extract_parameter_values(maxima_line_number)) 

        # Dictionary to store current parameter values
        current_parameter_values = {}
    
        # Iterate each parameter in the list to generate the template
        parameter_par_truncated = {}

        count = 0
        for parameter in parameters:

            # Get the parameter position on the line 
            par_position = find_parameter_position(header_line, parameter)

                # Validate and adjust the starting position if necessary
            if par_position[0] < len(ecotype):
                par_position[0] = len(ecotype)

            # Extract the current value of the parameter from the line
            parameter_value = lines[ecotype_line_number][par_position[0]:par_position[1]+1].strip()

            # Extract the second element when two numbers where obtained instead of one
            if len(str(parameter_value).split()) > 1:

                parameter_value = str(parameter_value).split()[-1]

            # Store the current value in the dictionary
            current_parameter_values[parameter] = parameter_value
        
            # Get the length of a parameter including empty spaces 
            char_compl = header_line[par_position[0]+1:par_position[1]+1]
            
            # Get the length of the parameter without empty characters 
            char = char_compl.strip()
        
            # Calculate the number of available characters for the parameter
            available_space = len(char_compl) - 2
            
            # Truncate or pad the parameter to fit within the available space
            if len(parameter) > available_space:

                truncated_parameter = parameter[:available_space]  # Truncate the parameter

                # Change the last character when the truncated parameter already exist in the dictionary 
                counter = 1
                while any(truncated_parameter.strip() == existing.strip() for existing in parameter_par_truncated.values()):
                    suffix = str(counter)
                    truncated_parameter = truncated_parameter[:-len(suffix)] + suffix
                    
                    counter += 1

                # Save the parameter compleate name and truncated name into a dictionary
                parameter_par_truncated[parameter] = truncated_parameter.strip()

            else:
                truncated_parameter = parameter.ljust(available_space)  # Add spaces to the parameter

                # Save the parameter compleate name and truncated name into a dictionary
                parameter_par_truncated[parameter] = truncated_parameter.strip()            

            # Construct the variable template
            variable_template = f" ~{truncated_parameter}~"

            # Extract the ecotype line to modify parameters
            ecotype_line = lines[ecotype_line_number]
        
            if count == 0:
                # Replace the content at the specified position with adjusted_template
                modified_line = (
                    ecotype_line[:par_position[0]]  # Part of the line before the parameter
                    + variable_template  # Insert the adjusted template
                    + ecotype_line[par_position[1] + 1:]  # Part of the line after the parameter
                )
            else: 
                # Replace the content at the specified position with adjusted_template
                modified_line = (
                    modified_line[:par_position[0]]  # Part of the line before the parameter
                    + variable_template  # Insert the adjusted template
                    + modified_line[par_position[1] + 1:]  # Part of the line after the parameter
                )
            count += 1

        #     # Save the parameter compleate name and truncated name into a dictionary     
        #     parameter_par_truncated[parameter] = truncated_parameter.strip()
        
        # Insert the modified line back into the text
        lines[ecotype_line_number] = modified_line
        
        # Insert 'ptf' and marker at the beginning of the file content
        lines.insert(0, f"{tpl_first_line} {mrk}")
        
        # Output the updated text
        updated_text = "\n".join(lines)
    
        # Validate output_path
        output_path = validate_output_path(output_path)

        # Add the file name and extension to the path for the new file
        output_new_file_path = os.path.join(output_path, os.path.splitext(os.path.basename(eco_file_path))[0] + '_ECO' + '.' + new_template_file_extension)
        
        # Save the updated text to a new .TPL file
        with open(output_new_file_path, 'w') as file:
            file.write("\n".join(lines))
        
        # Replace keys in current_parameter_values 
        current_parameter_values = {parameter_par_truncated[key]: value for key, value in current_parameter_values.items() if key in parameter_par_truncated}
        minima_parameter_values = {parameter_par_truncated[key]: value for key, value in minima_parameter_values.items() if key in parameter_par_truncated}
        maxima_parameter_values = {parameter_par_truncated[key]: value for key, value in maxima_parameter_values.items() if key in parameter_par_truncated}

        # Update the values in parameters_grouped
        parameters_grouped = {
            key: ', '.join(parameter_par_truncated.get(param.strip(), param.strip()) for param in value.split(','))
            for key, value in parameters_grouped.items()
        }
        

        print(f"Template file successfully created at: {output_new_file_path}")
        
        return {'parameters': current_parameter_values, 
                'minima_parameters': minima_parameter_values, 
                'maxima_parameters': maxima_parameter_values, 
                'parameters_grouped': parameters_grouped}, output_new_file_path

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except FileNotFoundError as fe:
        print(f"FileNotFoundError: {fe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")