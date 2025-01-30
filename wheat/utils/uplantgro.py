from dpest.functions import *

def uplantgro(
        plantgro_file_path=None,
        treatment=None,
        variables=None,
):
    """
    Updates the PlantGro.OUT file with new rows if necessary.

    Parameters:
    plantgro_file_path (str): Path to the PlantGro.OUT file
    treatment (str): Treatment identifier
    variables (list): List of variables to consider
    nspaces_year_header (int): Number of spaces for year header (default 5)
    nspaces_doy_header (int): Number of spaces for day of year header (default 4)
    nspaces_columns_header (int): Number of spaces for other columns (default 6)

    Returns:
    None
    """
    # Define default variables:
    nspaces_year_header = 5
    nspaces_doy_header = 4
    nspaces_columns_header = 6

    rows_added = 0  # Initialize here

    try:
        # Validate plantgro_file_path
        validated_path = validate_file(plantgro_file_path, '.OUT')

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

        # Get treatment range
        treatment_range = simulations_lines(plantgro_file_path)[treatment]

        # Read growth file
        plantgro_file_df = read_growth_file(plantgro_file_path, treatment_range)

        # Get treatment number
        treatment_dict = simulations_lines(plantgro_file_path)
        treatment_number_name, treatment_experiment_name = extract_treatment_info_plantgrowth(plantgro_file_path, treatment_dict)

        # Make the path for the WHT file
        wht_file_path = os.path.join(os.path.dirname(plantgro_file_path), treatment_experiment_name.get(treatment) + '.WHT')

        # Get the dataframe from the WHT file data
        wht_df = wht_filedata_to_dataframe(wht_file_path)

        # Load and filter data for all variables and get the measured year
        dates_variable_values_dict = filter_dataframe(wht_df, treatment, treatment_number_name, variables)
        #year_measured_key = int(list(dates_variable_values_dict.keys())[-1])

        # Get the year and day of the year and join it as one unique number
        year_sim = int(str(plantgro_file_df['@YEAR'].iloc[-1]) + f"{plantgro_file_df['DOY'].iloc[-1]:03}")

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
            new_rows = new_rows_add(plantgro_file_df, number_rows_add)

            # Read the existing file and store its contents
            with open(plantgro_file_path, 'r') as file:
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
            with open(plantgro_file_path, 'w') as file:
                file.writelines(lines)

            # Add messages about rows added (now inside the try block)
        if rows_added > 0:
            print(f"PlantGro.OUT update: {rows_added} row{'s' if rows_added > 1 else ''} added successfully.")
        else:
            print("PlantGro.OUT status: No update required.")

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except FileNotFoundError as fe:
        print(f"FileNotFoundError: {fe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")