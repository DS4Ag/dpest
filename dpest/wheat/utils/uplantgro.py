from dpest.functions import *

def uplantgro(
        plantgro_file_path=None,
        treatment=None,
        variables=None,
        nspaces_year_header=None,
        nspaces_doy_header = None,
        nspaces_columns_header = None,
):
    """
    Extends the ``PlantGro.OUT`` file by adding rows to ensure that simulated values exist for all measured observation dates. This situation arises during the calibration process when PEST attempts to compare a measured value from the DSSAT "T file" to a corresponding simulated value in the ``PlantGro.OUT`` file. If the simulation ends *before* the date of a measured observation, PEST will terminate the calibration process due to a missing observation error. This often occurs when measurements, such as remote sensing data, are taken close to the plant's maturity phase.

    This module addresses this issue by adding rows to the ``PlantGro.OUT`` file with default values (0), extending the simulation period to cover all measured observation dates.

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

    In this case, PEST  will throw an error and terminate the calibration because the ``PlantGro.OUT`` file does not contain information for the last ``DOY`` variable. The ``dpest.wheat.utils.uplantgro`` module adds the time series for the days that do not have an observation. The last row added with some values are simmilar with:

    .. code-block:: none

       2022  103   224     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0

    **Required Arguments:**
    =======

        * **plantgro_file_path** (*str*): Path to the ``PlantGro.OUT`` file.
        * **treatment** (*str*): The name of the treatment for which the cultivar is being calibrated. This should match exactly the treatment name as shown in the DSSAT application interface when an experiment is selected. For example, "164.0 KG N/HA IRRIG" is a treatment of the ``SWSW7501WH.WHX`` experiment.
        * **variables** (*list* or *str*): Variable(s) from the DSSAT "T file" (and thus present in the ``PlantGro.OUT file``) that PEST will extract. The PEST instruction file will use these to read the model output. You may specify a single variable as a string (e.g., ``'LAID'``) or multiple variables as a list (e.g., ``['LAID', 'CWAD', 'T#AD']``).

    **Optional Arguments:**
    =======

        * **nspaces_year_header** (*int*, *default: 5*): Number of spaces reserved for the year header in the ``PlantGro.OUT`` file. It is unlikely that the format of the ``PlantGro.OUT`` file changes in a way that necessitates modifying this value.
        * **nspaces_doy_header** (*int*, *default: 4*): Number of spaces reserved for the day-of-year header in the ``PlantGro.OUT`` file. It is unlikely that the format of the ``PlantGro.OUT`` file changes in a way that necessitates modifying this value.
        * **nspaces_columns_header** (*int*, *default: 6*): Number of spaces reserved for other columns in the ``PlantGro.OUT`` file. It is unlikely that the format of the ``PlantGro.OUT`` file changes in a way that necessitates modifying this value.

    **Returns:**
    =======

        * ``None``

    **Examples:**
    =======

    1. **Basic Usage (List of variables):**

       .. code-block:: python

          from dpest.wheat.utils import uplantgro

          uplantgro(
              plantgro_file_path='C:/DSSAT48/Wheat/PlantGro.OUT',
              treatment='164.0 KG N/HA IRRIG',
              variables=['LAID', 'CWAD', 'T#AD']
          )

       This example demonstrates the basic usage of the module with a list of variables (``LAID``, ``CWAD``, and ``T#AD``). If the simulation end date in the existing ``PlantGro.OUT`` file is earlier than the latest measurement date in the DSSAT "T file", then the ``PlantGro.OUT`` file will be extended by adding new rows. The values of all variables present in the ``PlantGro.OUT`` file will be set to ``0`` in the added rows.

    2. **Basic Usage (Single variable):**

       .. code-block:: python

          from dpest.wheat.utils import uplantgro

          uplantgro(
              plantgro_file_path='C:/DSSAT48/Wheat/PlantGro.OUT',
              treatment='164.0 KG N/HA IRRIG',
              variables='LAID'
          )

       This example demonstrates the basic usage of the module when only one variable (``LAID``) is specified. If the simulation end date in the existing ``PlantGro.OUT`` file is earlier than the latest measurement date in the DSSAT "T file", then the ``PlantGro.OUT`` file will be extended by adding new rows. The values of all variables present in the ``PlantGro.OUT`` file will be set to 0 in the added rows.
    """
    rows_added = 0  # Initialize

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