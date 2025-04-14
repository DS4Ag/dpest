import os
import pandas as pd
import re

from datetime import datetime, timedelta

def read_dssat_file(file_path):
    '''
    Function to read and print the file content
    '''
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except IOError:
        print(f"An error occurred while reading the file at {file_path}.")    

def extract_element_positions(line):
    """
    Extracts the first and last character positions of each element in a single line,
    including spaces between elements.

    Args:
        line (str): The text line to process.

    Returns:
        list of tuples: A list where each tuple contains the start and end positions of an element.
    """
    positions = []
    in_element = False
    start = None

    for i, char in enumerate(line):
        if char != " " and not in_element:  # Start of a new element
            in_element = True
            start = i
        elif char == " " and in_element:  # End of the current element
            in_element = False
            positions.append((start, i - 1))
    
    if in_element:  # Handle the last element if the line ends with a non-space character
        positions.append((start, len(line) - 1))
    
    # Include spaces as part of the range between consecutive elements
    adjusted_positions = []
    for idx, (start, end) in enumerate(positions):
        next_start = positions[idx + 1][0] if idx + 1 < len(positions) else len(line)
        adjusted_positions.append((start, next_start - 1))

    return adjusted_positions


def find_cultivar(file_content, head_line, cultivar, cultivar_cul_file):
    """
    Find the line containing the specified cultivar in the DSSAT cultivar file.
    
    Args:
    file_content (str): The content of the DSSAT cultivar file.
    cultivar (str): The cultivar to search for (VAR# or VAR-NAME).
    
    Returns:
    int: The line number containing the cultivar if found, or a message if not found.
    """
    lines = file_content.split('\n')

    # Find the index where the head parameters table starts to count the number of characters 
    for idx, line in enumerate(lines):
        if line.startswith(head_line):
            head = idx
    # Extract the number of characters that the head of the parameters table contain 
    num_characters = len(lines[head])
    
        # Get the character positions of each element on the head of the parameters table
    positions = extract_element_positions(lines[head])
    
    # Extract the line number that contains the cultivar number or name  
    for idx, line in enumerate(lines):
        if len(line) == len(lines[head]) and not line.strip().startswith('!'):
            var_num = lines[idx][positions[0][0]:positions[0][1]]
            var_name = lines[idx][positions[1][0]:positions[1][1]]
    
            # Get the position line of the cultivar 
            if cultivar == var_num.strip() or cultivar == var_name.strip():
                   return idx
    
    return f"The cultivar {cultivar} wasn't founded on file {cultivar_cul_file}"


def find_ecotype(file_content, head_line, ecotype, ecotype_file):
    """
    Find the line containing the specified ecotype in the DSSAT ecotype file.
    
    Args:
    file_content (str): The content of the DSSAT ecotype file.
    head_line (str): The line that starts the header of the ecotype table.
    ecotype (str): The ecotype to search for (ECO#).
    ecotype_file (str): The name of the ecotype file.
    
    Returns:
    int: The line number containing the ecotype if found, or a message if not found.
    """
    lines = file_content.split('\n')

    # Find the index where the head parameters table starts
    for idx, line in enumerate(lines):
        if line.startswith(head_line):
            head = idx
            break
    else:
        return f"Header line '{head_line}' not found in file {ecotype_file}"

    # Extract the number of characters that the head of the parameters table contains
    num_characters = len(lines[head])
    
    # Get the character positions of each element on the head of the parameters table
    positions = extract_element_positions(lines[head])
    
    # Extract the line number that contains the ecotype
    for idx, line in enumerate(lines[head+1:], start=head+1):
        if len(line) == num_characters and not line.strip().startswith('!'):
            # Extract the ecotype name and remove any trailing numbers or spaces
            eco_name = line[positions[0][0]:positions[0][1]].strip().split()[0]
            
            if ecotype == eco_name:
                return idx
    
    return f"The ecotype {ecotype} wasn't found in file {ecotype_file}"
    

def find_parameter_position(line, parameter=None):
    """
    Extracts the first and last character positions of each element in a single line,
    including spaces between elements. If a specific parameter is provided, returns
    its start and end positions.

    Args:
        line (str): The text line to process.
        parameter (str, optional): The element to search for. Defaults to None.

    Returns:
        list of tuples or list: A list of start and end positions for all elements,
                                or the start and end positions of the specific parameter if provided.
    """
    positions = []
    in_element = False
    start = None

    # Identify the positions of all elements
    for i, char in enumerate(line):
        if char != " " and not in_element:  # Start of a new element
            in_element = True
            start = i
        elif char == " " and in_element:  # End of the current element
            in_element = False
            positions.append((start, i - 1))

    if in_element:  # Handle the last element if the line ends with a non-space character
        positions.append((start, len(line) - 1))

    # Adjust positions to include spaces as part of the range between consecutive elements
    adjusted_positions = []
    for idx, (start, end) in enumerate(positions):
        previous_end = positions[idx - 1][1] if idx > 0 else -1
        adjusted_positions.append((previous_end + 1, end))

    # If a parameter is provided, find and return its position
    if parameter is not None:
        for (start, end) in adjusted_positions:
            if line[start:end + 1].strip() == parameter:
                return [start, end]

    return adjusted_positions


def simulations_lines(file_path):
    """
    Identifies and extracts the line ranges associated with specific treatments in the OVERVIEW output file.

    Parameters:
    file_path (str): The path to the text file containing tOVERVIEW output file.

    Returns:
    dict: A dictionary where the keys are TREATMENT names and the values are
          tuples containing the start and end line numbers.
    """

    # Initialize dictionaries and lists to store relevant data
    result_dict = {}
    dssat_lines = []
    run_lines = []

    # Open the file and read all lines into a list
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Iterate through each line to identify lines starting with '*DSSAT' and '*RUN'
    for i, line in enumerate(lines):
        if '*DSSAT' in line:
            # Store the line number of each '*DSSAT' occurrence
            dssat_lines.append(i)
        if line.strip().startswith('TREATMENT'):
            # Store the line number and the content of each 'TREATMENT' line
            run_lines.append((i, line.strip()))

    # Process the stored lines to populate the result dictionary
    for i, start_line in enumerate(dssat_lines):
        if i < len(dssat_lines) - 1:
            # Determine the end line for the current '*DSSAT' section
            end_line = dssat_lines[i + 1] - 1
        else:
            # If it's the last '*DSSAT' section, set the end line as the last line of the file
            end_line = len(lines) - 1
            end_line = len(lines)
        
        # Find the appropriate '*RUN' line within the current '*DSSAT' section
        run_info = None
        for run_start, run_line in run_lines:
            if run_start >= start_line and run_start <= end_line:
                # Extract only the 'treatment' name from the 'TREATMENT -n' line
                run_info = run_line.split(':')[1].strip().rsplit(maxsplit=1)[0]

                break
        
        # If the treatment information was found, store it in the result dictionary
        if run_info:
            result_dict[run_info] = (start_line, end_line)

    # Return the entire dictionary with all treatment information
    return result_dict


def extract_simulation_data(file_path):
    """
    Extracts simulation data for each cultivar, including the experiment information, 
    and returns a DataFrame with all the data.

    Parameters:
    file_path (str): The path to the text file containing the growth aspects data.

    Returns:
    pd.DataFrame: A DataFrame containing the parsed data for all cultivars, including the experiment info.
    """
    # Get the dictionary with the line ranges for each cultivar
    treatment_dict = simulations_lines(file_path)

    # Initialize an empty DataFrame to store all the data
    all_data = pd.DataFrame(columns=['TREATMENT','cultivar', 'VARIABLE', 'VALUE_SIMULATED', 'VALUE_MEASURED', 'EXPERIMENT', 'POSITION'])

    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Iterate through each cultivar and extract data
        for treatment, (start_line, end_line) in treatment_dict.items():
            cultivar_data = []
            experiment_info = None

            # Iterate through the lines in the specified range to find the EXPERIMENT line
            for i in range(start_line, end_line):
                line = lines[i].strip()

                # Look for the line containing 'EXPERIMENT'
                if line.startswith('EXPERIMENT'):
                    # Extract the experiment description after the colon
                    experiment_info = line.split(':')[1].strip()

                if line.startswith('CROP') and 'CULTIVAR :' in line:
                    # Extract CULTIVAR information using split
                    parts = line.split('CULTIVAR :')
                    if len(parts) > 1:
                        cultivar = parts[1].split('ECOTYPE')[0].strip()  # Extract everything between 'CULTIVAR :' and 'ECOTYPE'
                
                # Look for the line with simulation results (lines after @)
                if line.startswith('@'):

                    # Store the header line to return it 
                    header_line = line

                    line_number = 0
                    for data_line in lines[i+1:]:

                        line_number += 1

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
                            'TREATMENT': treatment,
                            'cultivar': cultivar,
                            'VARIABLE': variable_name,
                            'VALUE_SIMULATED': simulated_value,
                            'VALUE_MEASURED': measured_value,
                            'EXPERIMENT': experiment_info,
                            'POSITION': line_number,
                        })

                    # Convert to DataFrame and append to all_data
                    cultivar_df = pd.DataFrame(cultivar_data)
                    all_data = pd.concat([all_data, cultivar_df], ignore_index=True)

    # Remove rows where any of the columns 'VARIABLE', 'VALUE_SIMULATED', or 'VALUE_MEASURED' contain '--------'
    all_data = all_data[~all_data[['VARIABLE', 'VALUE_SIMULATED', 'VALUE_MEASURED']].apply(lambda x: x.str.contains('--------')).any(axis=1)]

    # Convert the 'VALUE_SIMULATED' and 'VALUE_MEASURED' columns to numeric values
    all_data['VALUE_SIMULATED'] = pd.to_numeric(all_data['VALUE_SIMULATED'], errors='coerce')
    all_data['VALUE_MEASURED'] = pd.to_numeric(all_data['VALUE_MEASURED'], errors='coerce')

    # Split the 'Cultivar' column into 'treatment' and 'cultivar' columns
    #all_data[['treatment', 'cultivar']] = all_data['Cultivar'].str.split('_', expand=True)

    # Drop the original 'Cultivar' column as it's now split into two
    #all_data.drop(columns=['Cultivar'], inplace=True)

    # Convert all column names to lowercase
    all_data.columns = all_data.columns.str.lower()

    return all_data, header_line


def process_treatment_file(file_path, treatment_mapping, season_mapping):
    """
    Reads the treatment file, extracts the treatment data, and adds 'treatment' and 'season' columns.

    Parameters:
    - file_path: Path to the treatment file.
    - treatment_mapping: A dictionary for mapping treatment codes (e.g., 'WW' to 'Well-watered').
    - season_mapping: A dictionary for mapping season codes (e.g., '22' to 'Winter 2021-2022').

    Returns:
    - DataFrame with 'N', 'TNAME', 'CU', 'treatment', and 'season' columns.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Initialize an empty list to store the data
    data = []
    in_treatments_section = False

    for line in lines:
        # Check if we are entering the TREATMENTS section
        if line.startswith('*TREATMENTS'):
            in_treatments_section = True
            continue
        
        # Check if we are leaving the TREATMENTS section
        if in_treatments_section and line.startswith('*'):
            break
        
        # Process lines in the TREATMENTS section
        if in_treatments_section:
            # Skip the header row
            if '@N' in line:
                continue
            
            # Split the line into columns using whitespace
            parts = list(filter(None, line.split()))
            if len(parts) >= 5:
                # Extract the required columns
                N = parts[0]
                TNAME = parts[4]
                CU = parts[5]
                data.append([N, TNAME, CU])
    
    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=['N', 'TNAME', 'entry'])
    
    # Extract treatment code and season code from TNAME and map them
    df['treatment'] = df['TNAME'].str[:2].map(treatment_mapping)
    df['season'] = df['TNAME'].str[2:4].map(season_mapping)
    
    return df

    
### Variables transformation functions
# Functions to transform the variable names from the OVERVIEW file fit the max 20 characters required by PEST

def clean_variable_name(variable_name):
    # Replace spaces with underscores
    cleaned_name = re.sub(r'\s+', '_', variable_name)
    # Remove all non-alphanumeric characters and underscores
    cleaned_name = re.sub(r'[\W]', '', cleaned_name)
    return cleaned_name

def adjust_variable_name(name, existing_names):
    # Ensure the name is no more than 20 characters
    if len(name) > 20:
        # Step 1: Remove underscores
        name = name.replace('_', '')
        # Step 2: Trim to 20 characters
        name = name[:20]

    # Check for duplicates and append suffix if necessary
    original_name = name
    suffix = 'A'
    while name in existing_names:
        name = f"{original_name[:18]}_{suffix}"
        suffix = chr(ord(suffix) + 1)  # Increment suffix (A -> B -> C, etc.)

    return name

def process_variable_names(df):
    # Clean variable names
    df['variable_name'] = df['variable'].apply(clean_variable_name)

    # Adjust names to ensure uniqueness and length constraints
    existing_names = set()
    adjusted_names = []

    for name in df['variable_name']:
        adjusted_name = adjust_variable_name(name, existing_names)
        adjusted_names.append(adjusted_name)
        existing_names.add(adjusted_name)

    df['variable_name'] = adjusted_names
    return df

### / Variables transformation functions


def extract_treatment_info_plantgrowth(file_path, treatment_dict):
    """
    Extracts treatment information and their corresponding codes from a file.

    Args:
        file_path (str): Path to the input file.
        treatment_dict (dict): A dictionary with treatment names as keys and their line ranges as values.

    Returns:
        dict: A dictionary where keys are treatment names and values are treatment codes.
    """
    treatment_number_name = {}
    treatment_experiment_name = {}

    # Read the file lines
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Iterate through each treatment range and extract data
        for treatment, (start_line, end_line) in treatment_dict.items():
            # Iterate through the lines in the specified range
            for i in range(start_line, end_line):
                line = lines[i].strip()

                # Look for the line containing 'EXPERIMENT'
                if line.startswith('EXPERIMENT'):
                    # Extract the code between 'EXPERIMENT' and ':'
                    experiment_info = line.split(':')[1].split()[0]

                # Look for the line containing 'TREATMENT'
                if line.startswith('TREATMENT'):
                    # Extract the code between 'TREATMENT' and ':'
                    treatment_code = line.split()[1].strip()

                    # Extract the treatment_info after the ':' and before trailing spaces
                    treatment_info = line.split(':')[1].strip().rsplit(maxsplit=1)[0]

                    # Store the values in the dictionary
                    treatment_number_name[treatment_info] = treatment_code

                    treatment_experiment_name[treatment_info] = experiment_info

    return treatment_number_name, treatment_experiment_name


def wht_filedata_to_dataframe(file_path):
    """
    Parses a DSSAT-style TXT file and returns a DataFrame.
    
    Parameters:
        file_path (str): The path to the TXT file.
    
    Returns:
        pd.DataFrame: A DataFrame containing the data from the TXT file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the line with column headers (starts with '@')
    header_line = None
    for line in lines:
        if line.startswith('@'):
            header_line = line.strip()
            break
    
    if header_line is None:
        raise ValueError("No header line starting with '@' found in the file.")
    
    # Extract column names from the header line
    columns = header_line[1:].split()

    # Find the data lines (non-comment and numeric)
    data_lines = [
        line.strip() for line in lines 
        if line.strip() and not line.startswith(('*', '!', '@'))
    ]

    # Parse data lines into a list of lists for the DataFrame
    data = []
    for line in data_lines:
        # Split on whitespace and ensure consistency with the number of columns
        values = line.split()
        if len(values) == len(columns):
            data.append(values)
        else:
            raise ValueError(f"Data row has inconsistent column count: {line}")

    # Create and return the DataFrame
    df = pd.DataFrame(data, columns=columns)
    return df


def get_header_and_first_sim(file_path):
    """
    Reads the header line and the first simulation date from the PlantGro.OUT file.

    Parameters:
    file_path (str): The path to the PlantGro.OUT file.

    Returns:
    tuple: A header line and the first simulation date as a datetime object.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find header line containing '@YEAR'
    header_line = next(line for line in lines if '@YEAR' in line)

    # Find line immediately after header for first simulation date
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            if '@YEAR' in line:
                first_sim = lines[line_num]
                break

    # Create datetime object based on first simulation year and day of year (DOY)
    date_first_sim = datetime(int(first_sim[1:5]), 1, 1) + timedelta(days=int(first_sim[6:9]) - 1)
    return header_line, date_first_sim



def calculate_days_dict(dates_dict, date_first_sim):
    """
    Calculates a dictionary of days from the first simulation date to each date in the dictionary.

    Parameters:
    dates_dict (dict): Dictionary mapping DOY values to variable names.
    date_first_sim (datetime): The first simulation date.

    Returns:
    dict: A dictionary mapping each date to its adjusted day count.
    """

    days_dict = {}
    for date_str, variables in dates_dict.items():
        # Handle four-digit year format (e.g., 2023012)
        if len(date_str) == 7:
            year_var = int(date_str[:4])
            day_var = int(date_str[4:])

        # Handle two-digit year format (e.g., 75167)
        elif len(date_str) == 5:
            year_var = int(date_str[:2])
            day_var = int(date_str[2:])

            # Complex year determination logic
            if year_var < date_first_sim.year % 100:
                # If year is less, assume it's in the next century
                year_var += 2000
            elif year_var == date_first_sim.year % 100:
                # If year is same, check day of year
                if day_var < date_first_sim.timetuple().tm_yday:
                    year_var += 2000  # Earlier in the year, next century
                else:
                    year_var += 1900  # Later in the year, same century
            else:
                # If year is greater, assume previous century
                year_var += 1900

        else:
            raise ValueError(f"Invalid date format: {date_str}")

        # Convert to actual date
        date_var = datetime(year_var, 1, 1) + timedelta(days=day_var - 1)

        # Calculate days from first simulation date
        days_from_start = (date_var - date_first_sim).days
        # days_dict[date_str] = [(date_var - date_first_sim).days, variable[0]]

        # Store all variables along with the day count
        # Calculate days from first simulation date and use the first variable
        first_variable = next(iter(variables))
        days_dict[date_str] = [(date_var - date_first_sim).days, list(variables.keys())]

    return days_dict


def adjust_days_dict(days_dict):
    """
    Adjusts the days dictionary to calculate differences between consecutive days.

    Parameters:
    days_dict (dict): Dictionary mapping DOY to a list with days and variable names.

    Returns:
    dict: Adjusted days dictionary with differences calculated and variable names preserved.
    """
    adjusted_days_dict = {}
    previous_days = None

    for date, (days, variable) in days_dict.items():
        if previous_days is None:
            adjusted_days = days + 1  # Initial adjustment for the first value
        else:
            adjusted_days = days - previous_days  # Difference from previous value

        # Update previous_days for the next iteration
        previous_days = days
        # Store the adjusted days along with the variable name
        adjusted_days_dict[date] = [adjusted_days, variable]

    return adjusted_days_dict


def find_variable_position(header_line, variables):

    """
        Counts space groups until the specified variables.
        Count starts at 1.

        Arguments:
        header_line (str): The header line containing variable names.
        variables (list): A list of variable names to find.

        Returns:
        dict: A dictionary with variables as keys and their positions as values.
    """
    variables_file = header_line.lstrip('@').split()
    positions = {}
    space_count = 1  # Start at 1

    for variable_file in variables_file:
        if variable_file in variables:
            positions[variable_file] = space_count
        space_count += 1

    # Check if all variables were found
    for variable in variables:
        if variable not in positions:
            print(f"Variable '{variable}' not found.")

    return positions


def filter_dataframe(dataframe, treatment, treatment_number_name, variables):
    """
    Filters a DataFrame based on the treatment and returns a dictionary of DATE
    and variables where values are not -99.

    Parameters:
    dataframe (pd.DataFrame): Input DataFrame.
    treatment (str): Treatment name to filter by.
    treatment_number_name (dict): Mapping of treatments to their corresponding TRNO values.
    variables (list): List of variable names to check in the dataset.

    Returns:
    dict: A dictionary containing filtered data with DATE as keys and variables as values.
    """
    # Check critical columns (if-else for missing columns)
    critical_columns = {'TRNO', 'DATE'}
    missing_critical = critical_columns - set(dataframe.columns)

    if missing_critical:
        print(f"Error: Missing critical columns {missing_critical}. Exiting.")
        return {}

    # Check if the treatment exists
    elif treatment not in treatment_number_name:
        print(f"Error: Treatment '{treatment}' not found. Exiting.")
        return {}

    elif set(variables).issubset(dataframe.columns):

        # Get the TRNO value for the treatment
        trno_value = treatment_number_name[treatment]

        # Initialize date and variable and value result dictionary
        variable_value = {}

        # Filter data with if-else for missing variables
        for variable in variables:

            if variable not in dataframe.columns:
                print(f"Warning: Column '{variable}' is missing. Skipping.")
            else:
                # Filter DataFrame for valid rows
                filtered_df = dataframe[
                    (dataframe['TRNO'] == trno_value) &
                    (dataframe[variable] != '-99') &
                    (dataframe[variable] != -99) &
                    (dataframe[variable] != 0)
                ]

                # Populate results
                for _, row in filtered_df.iterrows():
                    date = row['DATE']
                    if date not in variable_value:
                        variable_value[date] = {}
                    variable_value[date][variable] = row[variable]

        # Return sorted results
        return dict(sorted(variable_value.items()))

    else:
        # Notify if required columns are missing
        print(f"One or more required columns are missing: {set(variables) - set(dataframe.columns)}")
        return {}

def validate_marker(marker, marker_name):
    '''
    Validate the marker delimiter for the INS files according to the specified rules.
    '''
    invalid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789[]():& \t')

    if len(marker) != 1:
        raise ValueError(f"Invalid {marker_name} character. It must be a single character.")
    
    if marker_name == 'mrk' and (marker in invalid_chars or marker == '!'):
        raise ValueError(f"Invalid {marker_name} character. It must not be one of A-Z, a-z, 0-9, !, [, ], (, ), :, space, tab, or &.")
    elif marker_name == 'smk' and marker in invalid_chars:
        raise ValueError(f"Invalid {marker_name} character. It must not be one of A-Z, a-z, 0-9, [, ], (, ), :, space, tab, or &.")
    
    return marker


def validate_output_path(output_path):
    """
    Validates that the output file path specified by the user exists.
    """
    if output_path is not None:
        if not isinstance(output_path, str):
            raise ValueError("The 'output_path' must be a string if specified.")
        if not os.path.isdir(output_path):
            raise FileNotFoundError(f"The specified output directory does not exist: {output_path}")
    else:
        output_path = os.getcwd()
    return output_path


def validate_file(file_path, file_extension):

    """
    Validates that the input file path exists and the file extension is correct.
    """

    if not file_path or not isinstance(file_path, str):
        raise ValueError(f"The file path must be a non-empty string.")
    if not file_path.upper().endswith(file_extension.upper()):
        raise ValueError(f"The file must have a {file_extension} extension.")
    if not os.path.isfile(file_path):
        file_name = os.path.basename(file_path)
        file_dir = os.path.dirname(file_path)
        raise FileNotFoundError(f"The file '{file_name}' does not exist at: {file_dir}")
    return file_path


def validate_file_path(file_path):
    """
    Validates that the input file path exists.
    """
    if not file_path or not isinstance(file_path, str):
        raise ValueError(f"The file path must be a non-empty string.")
    if not os.path.isfile(file_path):
        file_name = os.path.basename(file_path)
        file_dir = os.path.dirname(file_path)
        raise FileNotFoundError(f"The file '{file_name}' does not exist at: {file_dir}")
    return file_path


def extract_all_params(*parameter_dicts):
    """
    Extract all parameters from one or more dictionaries.
    """
    all_params = []
    for param_dict in parameter_dicts:
        grouped = param_dict.get('parameters_grouped', {})
        params = [
            param
            for group in grouped.values()
            for param in group.replace(' ', '').split(',')
        ]
        all_params.extend(params)
    return all_params


def read_growth_file(file_path, treatment_range):
    """
    Reads a growth aspects output file and converts it into a pandas DataFrame.
    
    Arguments:
    file_path (str): The path to the text file containing the growth aspects data.
    treatment_range (tuple): A tuple containing the start and end line numbers for the treatment data.
    
    Returns:
    pd.DataFrame: A DataFrame containing the parsed data.
    """
    # Initialize an empty list to store the data
    data = []

    start_line, end_line = treatment_range

    # Open and read the file
    with open(file_path, "r") as text_file:
        lines = text_file.readlines()
        
        # Filter lines for the specified treatment
        treatment_lines = lines[start_line-1:end_line]  # -1 to account for 0-based indexing
            
        # Find the line starting with '@' which contains the column headers
        for i, line in enumerate(treatment_lines):
            if line.startswith('@'):
                header_line = line
                break
        
        # Extract the column headers by splitting the line at whitespace
        headers = header_line.strip().split()
        
        # Extract the data starting from the next line after the headers
        for line in treatment_lines[i+1:]:
            # Split the line into individual values based on whitespace
            row = line.strip().split()
            # Append the row to the data list
            data.append(row)

    # Create a DataFrame from the data with the extracted headers
    df = pd.DataFrame(data, columns=headers)

    # Convert appropriate columns to numeric data types
    df = df.apply(pd.to_numeric)

    return df


def new_rows_add(PlantGro, rows_add):
    # Get the last values from the relevant columns
    last_row = PlantGro.iloc[-1]
    last_das = int(last_row['DAS'])
    last_dap = int(last_row['DAP'])
    last_doy = int(last_row['DOY'])
    start_year = int(last_row['@YEAR'])

    new_rows = []

    for i in range(1, rows_add + 1):
        # Calculate the new values
        new_das = last_das + i
        new_dap = last_dap + i
        new_doy = last_doy + i

        def is_leap_year(year):
            """Check if a year is a leap year."""
            return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

        # Determine the number of days in the current year
        days_in_year = 366 if is_leap_year(start_year) else 365

        # If DOY exceeds the number of days in the year, increment the year and reset DOY
        if new_doy > days_in_year:
            new_doy = 1
            start_year += 1

        # Create the new row with 0 for all other columns
        new_row = {
            '@YEAR': start_year,
            'DOY': new_doy,
            'DAS': new_das,
            'DAP': new_dap,
        }

        # Add 0 for all other columns
        for col in PlantGro.columns.difference(['@YEAR', 'DOY', 'DAS', 'DAP']):
            new_row[col] = 0

        # Ensure new values are integers
        new_row['@YEAR'] = int(new_row['@YEAR'])
        new_row['DOY'] = int(new_row['DOY'])
        new_row['DAS'] = int(new_row['DAS'])
        new_row['DAP'] = int(new_row['DAP'])

        new_rows.append(new_row)

    return new_rows

def add_suffix_to_variables(variable_names, suffix, max_length):
    """
    Append a suffix to each variable name, ensuring the final name does not exceed max_length.

    Parameters:
        variable_names (iterable): List or Series of original variable names.
        suffix (str): Suffix to append (assumed already validated).
        max_length (int): Maximum allowed length of the final variable name.

    Returns:
        dict: Mapping from original variable name to suffixed (and possibly truncated) name.
    """
    updated_names = {}
    for var_name in variable_names:
        new_name = var_name + suffix
        if len(new_name) > max_length:
            new_name = var_name[:max_length - len(suffix)] + suffix
        updated_names[var_name] = new_name
    return updated_names