import yaml
import pyemu
import tempfile
from dpest.functions import *

def pst(
        cultivar_parameters=None,
        ecotype_parameters=None,
        species_parameters=None,
        dataframe_observations=None,
        output_path=None,
        model_comand_line=None,
        noptmax=1000,
        pst_filename='PEST_CONTROL.pst',
        input_output_file_pairs=None
):

    """
    Creates a ``PEST control file (.PST)`` for calibration of DSSAT crop models.

    The generated control file defines adjustable model parameters, parameter
    bounds and groups, observations and their weights, PEST template and
    instruction files, and the command used to execute DSSAT. It can incorporate
    parameters from cultivar (``.CUL``), ecotype (``.ECO``), and species
    (``.SPE``) files in a single calibration.

    **Conditionally Required Arguments:**
    =======

    At least one parameter dictionary must be supplied through
    ``cultivar_parameters``, ``ecotype_parameters``, or ``species_parameters``.
    Multiple parameter dictionaries may be supplied together.

        * **cultivar_parameters** (*dict*, *optional*):
          Dictionary containing cultivar-level parameter values, lower bounds,
          upper bounds, and parameter-group definitions. This dictionary is
          returned by the ``cul`` module.

          It is required only when no ``ecotype_parameters`` or
          ``species_parameters`` dictionary is supplied.

        * **ecotype_parameters** (*dict*, *optional*):
          Dictionary containing ecotype-level parameter values, lower bounds,
          upper bounds, and parameter-group definitions. This dictionary is
          returned by the ``eco`` module.

          It is required only when no ``cultivar_parameters`` or
          ``species_parameters`` dictionary is supplied.

        * **species_parameters** (*dict*, *optional*):
          Dictionary containing species-level parameter values, lower bounds,
          upper bounds, and parameter-group definitions. This dictionary is
          returned by the ``spe`` module.

          Species parameters can represent values stored in DSSAT species files
          such as ``SBGRO048.SPE`` or ``WHCER048.SPE``. It is required only when
          no ``cultivar_parameters`` or ``ecotype_parameters`` dictionary is
          supplied.

    **Required Arguments:**
    =======

        * **dataframe_observations** (``pd.DataFrame`` or ``list``):
          A DataFrame or list of DataFrames containing observations to be used in
          calibration and written to the ``* observation data`` section of the
          PEST control file.

          A single DataFrame may be supplied as:

          ``dataframe_observations = dataframe``

          Multiple DataFrames may be supplied as:

          ``dataframe_observations = [dataframe1, dataframe2]``

          Each DataFrame must contain the following columns:

          * ``'variable_name'``: Unique PEST observation identifier.
          * ``'value_measured'``: Measured value used as the PEST observation.
          * ``'group'``: PEST observation-group name.

          Observation DataFrames can be created using modules such as
          ``overview`` and ``plantgro``.

        * **model_comand_line** (*str*):
          Command line used by PEST to execute the DSSAT model. The command must
          generate all model output files referenced by the instruction-file
          entries in ``input_output_file_pairs``.

        * **input_output_file_pairs** (``list``):
          List of tuples defining PEST template/instruction files and their
          associated DSSAT input/output files. Each tuple follows the form:

          ``(pest_file, model_file)``

          where ``pest_file`` is a PEST template file (``.TPL``) or instruction
          file (``.INS``), and ``model_file`` is the corresponding DSSAT input or
          model-output file.

          The required template-file pairs depend on the parameter dictionaries
          supplied:

          * If ``cultivar_parameters`` is specified, the list must include a
            ``.TPL`` file paired with its corresponding DSSAT cultivar file
            (``.CUL``).

          * If ``ecotype_parameters`` is specified, the list must include a
            ``.TPL`` file paired with its corresponding DSSAT ecotype file
            (``.ECO``).

          * If ``species_parameters`` is specified, the list must include a
            ``.TPL`` file paired with its corresponding DSSAT species file
            (``.SPE``).

          * For each DataFrame in ``dataframe_observations``, the list must
            include an ``.INS`` file paired with the associated DSSAT output file,
            such as ``OVERVIEW.OUT`` or ``PlantGro.OUT``.

          Example structure:

          ``[(input_file1, output_file1), (input_file2, output_file2)]``

    **Optional Arguments:**
    =======

        * **output_path** (*str*, *default: current working directory*):
          Directory in which the ``.PST`` file is written.

        * **noptmax** (*int*, *default: 1000*):
          Maximum number of PEST optimization iterations.

          Set ``noptmax=-1`` to perform a Jacobian-based sensitivity run without
          conducting iterative parameter optimization.

        * **pst_filename** (*str*, *default: ``"PEST_CONTROL.pst"``*):
          File name assigned to the generated PEST control file.

    **Returns:**
    =======

        * ``None``:
          Creates the PEST control file at ``output_path`` using
          ``pst_filename``. The function validates supplied parameter
          dictionaries, observations, and template/instruction file pairs; merges
          parameter data from the supplied DSSAT file levels; sets parameter
          bounds and groups; and writes the completed ``.PST`` file.

    **Examples:**
    =======

    1. **Creating a PEST Control File with Cultivar and Ecotype Parameters**

       .. code-block:: python

          from dpest import pst

          pst(
              cultivar_parameters=cultivar_parameters,
              ecotype_parameters=ecotype_parameters,
              dataframe_observations=[
                  overview_observations,
                  plantgro_observations,
              ],
              model_comand_line=r'py "C:/pest18/run-dssat.py"',
              input_output_file_pairs=[
                  (cultivar_tpl_path, r'C:/DSSAT48/Genotype/WHCER048.CUL'),
                  (ecotype_tpl_path, r'C:/DSSAT48/Genotype/WHCER048.ECO'),
                  (overview_ins_path, r'C:/DSSAT48/Wheat/OVERVIEW.OUT'),
                  (plantgro_ins_path, r'C:/DSSAT48/Wheat/PlantGro.OUT'),
              ],
          )

       This example calibrates cultivar and ecotype parameters using end-of-season
       crop-performance observations and plant-growth observations.

    2. **Creating a PEST Control File with Cultivar Parameters Only**

       .. code-block:: python

          from dpest import pst

          pst(
              cultivar_parameters=cultivar_parameters,
              dataframe_observations=[
                  overview_observations,
                  plantgro_observations,
              ],
              model_comand_line=r'py "C:/pest18/run-dssat.py"',
              input_output_file_pairs=[
                  (cultivar_tpl_path, r'C:/DSSAT48/Genotype/WHCER048.CUL'),
                  (overview_ins_path, r'C:/DSSAT48/Wheat/OVERVIEW.OUT'),
                  (plantgro_ins_path, r'C:/DSSAT48/Wheat/PlantGro.OUT'),
              ],
          )

       This example calibrates cultivar parameters using both end-of-season and
       time-series plant-growth observations.

    3. **Creating a PEST Control File with Species Parameters Only**

       .. code-block:: python

          from dpest import pst

          pst(
              species_parameters=species_parameters,
              dataframe_observations=[
                  overview_observations,
                  plantgro_observations,
              ],
              model_comand_line=r'py "C:/pest18/run-dssat.py"',
              input_output_file_pairs=[
                  (species_tpl_path, r'C:/DSSAT48/Genotype/SBGRO048.SPE'),
                  (overview_ins_path, r'C:/DSSAT48/Soybean/OVERVIEW.OUT'),
                  (plantgro_ins_path, r'C:/DSSAT48/Soybean/PlantGro.OUT'),
              ],
          )

       This example calibrates species-level soybean parameters defined in
       ``SBGRO048.SPE``, such as photosynthesis, nitrogen fixation, temperature
       response, root-growth, or other CROPGRO species coefficients.

    4. **Creating a Combined Cultivar, Ecotype, and Species Calibration**

       .. code-block:: python

          from dpest import pst

          pst(
              cultivar_parameters=cultivar_parameters,
              ecotype_parameters=ecotype_parameters,
              species_parameters=species_parameters,
              dataframe_observations=[
                  overview_observations,
                  plantgro_observations,
              ],
              model_comand_line=r'py "C:/pest18/run-dssat.py"',
              input_output_file_pairs=[
                  (cultivar_tpl_path, r'C:/DSSAT48/Genotype/SBGRO048.CUL'),
                  (ecotype_tpl_path, r'C:/DSSAT48/Genotype/SBGRO048.ECO'),
                  (species_tpl_path, r'C:/DSSAT48/Genotype/SBGRO048.SPE'),
                  (overview_ins_path, r'C:/DSSAT48/Soybean/OVERVIEW.OUT'),
                  (plantgro_ins_path, r'C:/DSSAT48/Soybean/PlantGro.OUT'),
              ],
              noptmax=-1,
              pst_filename='SBGRO_NFIX_SENSITIVITY.pst',
          )

       This example creates a Jacobian-only sensitivity-analysis control file for
       a combined calibration involving cultivar, ecotype, and species
       parameters. The ``noptmax=-1`` setting calculates parameter sensitivities
       without performing iterative optimization.
    """


    # Define default variables
    yml_pst_file_block = 'PST_FILE'
    yml_file_observation_groups = 'OBSERVATION_GROUPS_SPECIFICATIONS'

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
        if not (cultivar_parameters or ecotype_parameters):
            raise ValueError(
                "At least one of `cultivar_parameters` or `ecotype_parameters` must be provided and non-empty.")

        if cultivar_parameters and not isinstance(cultivar_parameters, dict):
            raise ValueError("`cultivar_parameters`, if provided, must be a dictionary.")

        if ecotype_parameters and not isinstance(ecotype_parameters, dict):
            raise ValueError("`ecotype_parameters`, if provided, must be a dictionary.")

        # Additional validation for file extensions based on parameters
        if cultivar_parameters:
            if not any(pair[1].lower().endswith('.cul') for pair in input_output_file_pairs):
                raise ValueError(
                    "If `cultivar_parameters` is provided, at least one file in `input_output_file_pairs` must have a '.CUL' extension.")
        if ecotype_parameters:
            if not any(pair[1].lower().endswith('.eco') for pair in input_output_file_pairs):
                raise ValueError(
                    "If `ecotype_parameters` is provided, at least one file in `input_output_file_pairs` must have a '.ECO' extension.")

        # Validate that at least one file has a '.OUT' extension
        if not any(pair[1].lower().endswith('.out') for pair in input_output_file_pairs):
            raise ValueError("At least one file in `input_output_file_pairs` must have a '.OUT' extension.")

        if dataframe_observations is None:
            raise ValueError("`dataframe_observations` must be provided.")

        # Convert single dataframe to list for consistent processing
        if isinstance(dataframe_observations, pd.DataFrame):
            dataframe_observations = [dataframe_observations]

        if not isinstance(dataframe_observations, list) or not all(
                isinstance(df, pd.DataFrame) for df in dataframe_observations):
            raise ValueError("`dataframe_observations` must be a DataFrame or a list of DataFrames.")

        required_columns = {'variable_name', 'value_measured', 'group'}
        for df in dataframe_observations:
            if not required_columns.issubset(df.columns):
                raise ValueError(
                    "Each DataFrame in `dataframe_observations` must contain 'variable_name', 'value_measured', and 'group' columns.")

        # Get Parameter Group Variables
        observation_groups = yaml_data[yml_pst_file_block][yml_file_observation_groups]

        # ~~~~~~~~~~~~~~~~~~~~~~~ Old version
        # # Merge dictionaries if both are provided, or use the one that exists
        # parameters = {
        #     'parameters': {**(cultivar_parameters.get('parameters', {}) if cultivar_parameters else {}),
        #                    **(ecotype_parameters.get('parameters', {}) if ecotype_parameters else {})},
        #     'minima_parameters': {**(cultivar_parameters.get('minima_parameters', {}) if cultivar_parameters else {}),
        #                           **(ecotype_parameters.get('minima_parameters', {}) if ecotype_parameters else {})},
        #     'maxima_parameters': {**(cultivar_parameters.get('maxima_parameters', {}) if cultivar_parameters else {}),
        #                           **(ecotype_parameters.get('maxima_parameters', {}) if ecotype_parameters else {})},
        #     'parameters_grouped': {**(cultivar_parameters.get('parameters_grouped', {}) if cultivar_parameters else {}),
        #                            **(ecotype_parameters.get('parameters_grouped', {}) if ecotype_parameters else {})}
        # }
        # ~~~~~~~~~~~~~~~~~~~~~~~ / Old version

        # ~~~~~~~~~~~~~~~~~~~~~~~ New version
        # Merge parameter values (parameter names are unique, safe to merge directly)
        parameters = {
            'parameters': {
                **(cultivar_parameters.get('parameters', {}) if cultivar_parameters else {}),
                **(ecotype_parameters.get('parameters', {}) if ecotype_parameters else {}),
                **(species_parameters.get('parameters', {}) if species_parameters else {}),
            },
            'minima_parameters': {
                **(cultivar_parameters.get('minima_parameters', {}) if cultivar_parameters else {}),
                **(ecotype_parameters.get('minima_parameters', {}) if ecotype_parameters else {}),
                **(species_parameters.get('minima_parameters', {}) if species_parameters else {}),
            },
            'maxima_parameters': {
                **(cultivar_parameters.get('maxima_parameters', {}) if cultivar_parameters else {}),
                **(ecotype_parameters.get('maxima_parameters', {}) if ecotype_parameters else {}),
                **(species_parameters.get('maxima_parameters', {}) if species_parameters else {}),
            },
            'parameters_grouped': {
                **(cultivar_parameters.get('parameters_grouped', {}) if cultivar_parameters else {}),
                **(ecotype_parameters.get('parameters_grouped', {}) if ecotype_parameters else {}),
                **(species_parameters.get('parameters_grouped', {}) if species_parameters else {}),
            }
        }

        # Merge parameter groups without overwriting shared group names
        combined_parameters_grouped = {}

        # Loop through cultivar, ecotype, and species group definitions
        for source in [
            cultivar_parameters.get('parameters_grouped', {}) if cultivar_parameters else {},
            ecotype_parameters.get('parameters_grouped', {}) if ecotype_parameters else {},
            species_parameters.get('parameters_grouped', {}) if species_parameters else {}
        ]:
            for group_name, group_params in source.items():

                # Split group string into individual parameters
                new_params = [p.strip() for p in group_params.split(',') if p.strip()]

                if group_name not in combined_parameters_grouped:
                    # Initialize group
                    combined_parameters_grouped[group_name] = new_params
                else:
                    # Add parameters not already included
                    for p in new_params:
                        if p not in combined_parameters_grouped[group_name]:
                            combined_parameters_grouped[group_name].append(p)


        # Convert lists back to comma-separated strings
        parameters['parameters_grouped'] = {
            group_name: ', '.join(param_list)
            for group_name, param_list in combined_parameters_grouped.items()
        }
        # ~~~~~~~~~~~~~~~~~~~~~~~ / New version

        # Extract cultivar_parameters
        all_params = [
            param for group in parameters['parameters_grouped'].values()
            for param in group.replace(' ', '').split(',')
        ]

        # Create a minimal PST object
        pst = pyemu.pst_utils.generic_pst(all_params)

        # Populate parameters
        for param in all_params:
            pst.parameter_data.loc[param, 'parval1'] = float(parameters['parameters'][param])
            pst.parameter_data.loc[param, "parlbnd"] = float(parameters['minima_parameters'][param])
            pst.parameter_data.loc[param, "parubnd"] = float(parameters['maxima_parameters'][param])
            pst.parameter_data.loc[param, "pargp"] = next(
                (group for group, params in parameters['parameters_grouped'].items() if param in params.split(', ')),
                None)

            # Add PARTRANS and PARCHGLIM
            pst.parameter_data.loc[param, "partrans"] = "none"  # Set PARTRANS to none
            pst.parameter_data.loc[param, "parchglim"] = "relative"  # Set PARCHGLIM to relative

        # Create parameter groups using values from observation_groups
        pargp_data = []
        for group in parameters['parameters_grouped'].keys():
            pargp_entry = {"pargpnme": group}  # Start with the group name
            pargp_entry.update(observation_groups)  # Update with values from observation_groups
            pargp_data.append(pargp_entry)

        # Convert parameter groups list to DataFrame
        pst.parameter_groups = pd.DataFrame(pargp_data)

        # Clear existing observation data
        pst.observation_data = pst.observation_data.iloc[0:0]

        # Process all dataframes
        for df in dataframe_observations:
            # Validate and clean observation data
            df['value_measured'] = pd.to_numeric(df['value_measured'], errors='coerce')
            df = df.dropna(subset=['value_measured'])

            for index, row in df.iterrows():
                obsnme = row['variable_name']
                obsval = row['value_measured']
                obgnme = row['group']
                pst.observation_data.loc[obsnme, 'obsnme'] = obsnme
                pst.observation_data.loc[obsnme, 'obsval'] = obsval
                pst.observation_data.loc[obsnme, 'obgnme'] = obgnme
                pst.observation_data.loc[obsnme, 'weight'] = 1.0  # Default weight

        # ~~~~~~~~ Handle input and output files

        if input_output_file_pairs:
            # Validate file pairs
            if not all(len(pair) == 2 for pair in input_output_file_pairs):
                raise ValueError("Each input_output_file_pair must contain exactly two elements")
            if not all(pair[0].lower().endswith(('.tpl', '.ins')) for pair in input_output_file_pairs):
                raise ValueError("The first element of each pair must be a .tpl or .ins file")

            # Validate file existence
            for pair in input_output_file_pairs:
                validate_file_path(pair[0])  # Validate PEST file (TPL or INS)
                validate_file_path(pair[1])  # Validate model file

            # Function to count TPL and INS files
            def count_file_types(file_pairs):
                tpl_count = sum(1 for pair in file_pairs if pair[0].lower().endswith('.tpl'))
                ins_count = sum(1 for pair in file_pairs if pair[0].lower().endswith('.ins'))
                return tpl_count, ins_count

            # Add quotes to escape spaces
            def escape_spaces(file_pairs):
                return [
                    (f'"{pair[0]}"' if ' ' in pair[0] else pair[0],
                     f'"{pair[1]}"' if ' ' in pair[1] else pair[1])
                    for pair in file_pairs
                ]

            # Escape spaces in paths
            input_output_file_pairs = escape_spaces(input_output_file_pairs)

            # Count TPL and INS files
            tpl_count, ins_count = count_file_types(input_output_file_pairs)

            # Set input files (TPL files)
            pst.model_input_data = pd.DataFrame({
                'pest_file': [pair[0] for pair in input_output_file_pairs if
                              pair[0].strip('"').lower().endswith('.tpl')],
                'model_file': [pair[1] for pair in input_output_file_pairs if
                               pair[0].strip('"').lower().endswith('.tpl')]
            })

            # Set output files (INS files)
            pst.model_output_data = pd.DataFrame({
                'pest_file': [pair[0] for pair in input_output_file_pairs if
                              pair[0].strip('"').lower().endswith('.ins')],
                'model_file': [pair[1] for pair in input_output_file_pairs if
                               pair[0].strip('"').lower().endswith('.ins')]
            })

            # Set NTPLFLE and NINSFLE
            pst.control_data.ntplfle = tpl_count
            pst.control_data.ninsfle = ins_count

        # ~~~~~~~~/ Handle input and output files

        # Set NUMCOM, JACFILE, and MESSFILE
        pst.control_data.numcom = 1
        pst.control_data.jacfile = 0
        pst.control_data.messfile = 0

        # Set mode of operation to use
        pst.pestmode = "estimation"


        # ~~~~~~~~ Customize SVD section as a custom attribute

        # Store the original write method
        original_write = pst.write

        # Define a new write method that updates the SVD section
        def custom_write(self, filename):
            # First, write to a temporary file
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
                original_write(temp_file.name)
                temp_filename = temp_file.name

            # Read the content of the temporary file
            with open(temp_filename, 'r') as f:
                content = f.read()

            # Compute SVD defaults based on number of parameters
            npar = self.npar
            svdmode = 1  # enable SVD
            maxsing = npar  # allow up to number of parameters
            eigthresh = 5e-7  # recommended in PEST manual for most cases
            eigwrite = 0  # only singular values, smaller .svd file

            # Build SVD section text (matches PEST format)
            svd_section = (
                "* singular value decomposition\n"
                f"  {svdmode}\n"
                f"  {maxsing}  {eigthresh:.6E}\n"
                f"  {eigwrite}\n"
            )

            # Replace existing SVD section, or insert a new one after * control data
            if re.search(r'\* singular value decomposition.*?(?=\*|$)',
                         content, flags=re.DOTALL | re.IGNORECASE):
                # Replace existing SVD block
                content = re.sub(
                    r'\* singular value decomposition.*?(?=\*|$)',
                    svd_section,
                    content,
                    flags=re.DOTALL | re.IGNORECASE
                )
            else:
                # Insert SVD block immediately after the * control data section
                content = re.sub(
                    r'(\* control data.*?(?=\*|$))',
                    r'\1\n' + svd_section,
                    content,
                    flags=re.DOTALL | re.IGNORECASE
                )

            # Write modified content to the final file
            with open(filename, 'w') as f:
                f.write(content)

            # Remove the temporary file
            os.unlink(temp_filename)

        # Replace the write method
        pst.write = custom_write.__get__(pst)

        # ~~~~~~~~/ Customize SVD section as a custom attribute

        # # ~~~~~~~~ Add LSQR section as a custom attribute
        #
        # pst.lsqr_data = {
        #     "lsqrmode": 1,
        #     "lsqr_atol": 1e-4,
        #     "lsqr_btol": 1e-4,
        #     "lsqr_conlim": 28.0,
        #     "lsqr_itnlim": 28,
        #     "lsqrwrite": 0
        # }
        #
        # # Store the original write method
        # original_write = pst.write
        #
        # # Define a new write method that replaces SVD with LSQR
        # def custom_write(self, filename):
        #     # First, write to a temporary file
        #     with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        #         original_write(temp_file.name)
        #         temp_filename = temp_file.name
        #
        #     # Read the content of the temporary file
        #     with open(temp_filename, 'r') as f:
        #         content = f.read()
        #
        #     # Replace SVD section with LSQR
        #     lsqr_section = f"* lsqr\n  {self.lsqr_data['lsqrmode']}\n  {self.lsqr_data['lsqr_atol']}  {self.lsqr_data['lsqr_btol']}  {self.lsqr_data['lsqr_conlim']}  {self.lsqr_data['lsqr_itnlim']}\n  {self.lsqr_data['lsqrwrite']}\n"
        #     content = re.sub(r'\* singular value decomposition.*?(?=\*|$)', lsqr_section, content, flags=re.DOTALL)
        #
        #     # Write modified content to the final file
        #     with open(filename, 'w') as f:
        #         f.write(content)
        #
        #     # Remove the temporary file
        #     os.unlink(temp_filename)
        #
        # # Replace the write method
        # pst.write = custom_write.__get__(pst)
        #
        # # ~~~~~~~~/ Add LSQR section as a custom attribute

        # Set additional control data parameters
        pst.control_data.rlambda1 = 10.0
        pst.control_data.numlam = 10
        pst.control_data.icov = 1
        pst.control_data.icor = 1
        pst.control_data.ieig = 1

        # Add the the command used to run the model executable
        pst.model_command = [model_comand_line]

        # Add number of iteractions
        pst.control_data.noptmax = noptmax

        # Validate output_path
        output_path = validate_output_path(output_path)

        # Create the path and name for the file ouput
        pst_file_path = os.path.join(output_path, pst_filename)

        # Write the PST file
        pst.write(pst_file_path)

        print(f"PST file successfully created: {pst_file_path}")

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except FileNotFoundError as fe:
        print(f"FileNotFoundError: {fe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")