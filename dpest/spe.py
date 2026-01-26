import yaml
from dpest.functions import *


def spe(
    species_file_path = None,
    output_path = None,
    new_template_file_extension = None,
    tpl_first_line = None,
    mrk = '~',
    **parameters_grouped,
):
    """
    Creates a ``PEST template file (.TPL)`` for species-level parameters based on a
    ``DSSAT species file (.SPE)`` (e.g. ``SBGRO048.SPE``, ``WHCER048.SPE``).

    Unlike cultivar (``.CUL``) and ecotype (``.ECO``) files, species files do not follow
    a strictly tabular structure. Parameters are often arranged in blocks, tuples, or
    vectors, and may lack explicit column headers. This module therefore relies on
    user-specified parameter locations (line number and column position) to build the
    template.

    Each parameter to be calibrated is provided as a keyword argument, where the keyword
    is the user-defined parameter name, and the value describes the location and bounds
    of that parameter. Two input formats are supported:

    1) **Tuple / list syntax** (no explicit keys):

       .. code-block:: python

          PARMAX = (line, column, min_value, max_value, group_name)

       For example:

       .. code-block:: python

          PARMAX = (5, 1, 20.0, 60.0, 'PHOTOSYN')

       where:

       - ``line`` (*int*): 1-based line number in the ``.SPE`` file where the parameter
         value (to calibrate) is located.
       - ``column`` (*int*): 1-based column index of the parameter value (to calibrate) within that
         line, counting numeric entries from left to right.
       - ``min_value`` (*float*): Minimum value of the parameter search range to be used
         in the PEST calibration.
       - ``max_value`` (*float*): Maximum value of the parameter search range to be used
         in the PEST calibration.
       - ``group_name`` (*str*, *optional*): Name of the PEST parameter group to which
         this parameter belongs. If omitted, the group name defaults to the parameter
         name (e.g. ``PARMAX``).

    2) **Dictionary syntax** (explicit keys):

       .. code-block:: python

          PARMAX = {
              'line': 5,
              'column': 1,
              'min': 20.0,
              'max': 60.0,
              'group': 'PHOTOSYN',
          }

       If ``'group'`` is not provided, it defaults to the parameter name.

    The function replaces the original numeric values at the specified locations with
    PEST template markers, truncating or padding parameter identifiers as needed to fit
    within the available space, and ensuring that each truncated identifier is unique
    (e.g. ``~PM0~``, ``~PM1~``). The resulting template file is written alongside the
    original species file (or to ``output_path`` if provided).

    **Required Arguments:**
    =======

        * **species_file_path** (*str*):
            Full path to the ``DSSAT species file (.SPE)``. For example:

            - ``C:/DSSAT48/Genotype/WHCER048.SPE``
            - ``C:/DSSAT48/Genotype/SBGRO048.SPE``

    **Optional Arguments:**
    =======

        * **output_path** (*str*, *default: current working directory*):
            Directory to save the generated ``PEST template file (.TPL)``.

        * **new_template_file_extension** (*str*, *default: "TPL"*):
            Extension for the generated ``PEST template file (.TPL)``. This is the PEST
            default value and should not be changed without good reason.

        * **tpl_first_line** (*str*, *default: "ptf"*):
            First line to include in the ``PEST template file (.TPL)``. This is the PEST
            default value and should not be changed without good reason.

        * **mrk** (*str*, *default: "~"*):
            Primary marker delimiter character for the template file. Must be a single
            character and cannot be A–Z, a–z, 0–9, ``!``, ``[``, ``]``, ``(``, ``)``,
            ``:``, space, tab, or ``&``.

        * **parameters_grouped** (*dict*, *optional*):
            Species parameters to calibrate, passed as keyword arguments. Each keyword
            corresponds to a parameter name (used as the PEST parameter identifier before
            truncation), and its value is either:

            - A tuple/list: ``(line, column, min_value, max_value[, group_name])``
            - A dictionary with keys: ``'line'``, ``'column'``, ``'min'``, ``'max'``,
              and optional ``'group'``.

            For example:

            .. code-block:: python

               from dpest import spe

               species_parameters, species_tpl_path = spe(
                   species_file_path = 'C:/DSSAT48/Genotype/WHCER048.SPE',
                   PGERM = (15, 1, 0.0, 20.0, 'Phase_dur'),
                   P0    = (15, 3, -5.0, 5.0, 'Phase_dur'),
                   Fac   = (19, 1, 0.0, 2.0,  'Phase_dur'),
                   h     = (19, 2, 10.0, 30.0, 'Phase_dur'),
                   GrStg = (19, 3, 0.0, 4.0,  'Phase_dur'),
                   LWLOS = (30, 3, 0.0, 6.0,  'Phase_dur'),
               )

            In this case, several CERES-Wheat species parameters from different sections
            of the WHCER048.SPE file are selected for calibration in a single template.

    **Returns:**
    =======

    * *tuple*: A tuple containing:

        * *dict*: A dictionary containing:

            * ``'parameters'``:
                Current parameter values at the specified locations. Keys are the
                truncated parameter identifiers that are written into the template file.

            * ``'minima_parameters'``:
                User-specified minimum values for each parameter, keyed by the truncated
                parameter identifiers. These values define the lower limits of the
                parameter ranges explored by PEST.

            * ``'maxima_parameters'``:
                User-specified maximum values for each parameter, keyed by the truncated
                parameter identifiers. These values define the upper limits of the
                parameter ranges explored by PEST.

            * ``'parameters_grouped'``:
                Parameter group definitions, with each group containing a comma-separated
                list of the truncated parameter identifiers used in the template file.

        * *str*:
            The full path to the generated ``PEST template file (.TPL)``.

    **Notes:**
    =======

    * Line numbering convention:
        This function assumes that the user-provided ``line`` values are 1-based
        (i.e. the first line in the file is line 1). Internally, these values are
        converted to 0-based indices when accessing the file content.

    * Column indexing:
        The ``column`` argument is interpreted as a 1-based index of the numeric entry
        within the specified line, counting from left to right. Internally, the line is
        split into entries using default whitespace separation in order to locate the
        corresponding value.

    **Examples:**
    =======

    1. **CERES-Wheat species file (WHCER048.SPE):**

       .. code-block:: python

          from dpest import spe

          species_parameters, species_tpl_path = spe(
              species_file_path = 'C:/DSSAT48/Genotype/WHCER048.SPE',
              PGERM = (15, 1, 0.0, 20.0, 'Phase_dur'),
              P0    = (15, 3, -5.0, 5.0, 'Phase_dur'),
              Fac   = (19, 1, 0.0, 2.0,  'Phase_dur'),
              h     = (19, 2, 10.0, 30.0, 'Phase_dur'),
              GrStg = (19, 3, 0.0, 4.0,  'Phase_dur'),
              LWLOS = (30, 3, 0.0, 6.0,  'Phase_dur'),
          )

       The returned ``species_parameters`` dictionary can be used to define PEST
       parameter groups and parameter ranges in the PEST control file using the ``pst``
       module, and ``species_tpl_path`` is used in the ``input_output_file_pairs``
       argument of the ``pst`` module to match the original WHCER048.SPE file to the
       template file.

    2. **Soybean species file (SBGRO048.SPE) using dictionary syntax:**

       .. code-block:: python

          from dpest import spe

          species_parameters, species_tpl_path = spe(
              species_file_path = 'C:/DSSAT48/Genotype/SBGRO048.SPE',
              PARMAX = {
                  'line': 5,
                  'column': 1,
                  'min': 20.0,
                  'max': 60.0,
                  'group': 'PHOTOSYN',
              },
              PHTMAX = {
                  'line': 5,
                  'column': 2,
                  'min': 40.0,
                  'max': 80.0,
                  'group': 'PHOTOSYN',
              },
              XLMAXT_2 = {
                  'line': 11,
                  'column': 2,
                  'min': 0.0,
                  'max': 20.0,
                  'group': 'TEMP_RESP',
              },
              XPGSLW_3 = {
                  'line': 18,
                  'column': 3,
                  'min': 0.0,
                  'max': 0.01,
                  'group': 'SLW_SHAPE',
              },
              RTDEPI = {
                  'line': 40,
                  'column': 1,
                  'min': 10.0,
                  'max': 40.0,
                  'group': 'ROOTS',
              },
          )

       This example illustrates the dictionary syntax for specifying parameter locations
       and bounds in the soybean SBGRO048.SPE file, where several parameters are stored
       in tuple or vector‑like blocks rather than simple scalar entries.
    """

    # YAML configuration block for species template settings
    yml_species_block = 'SPECIES_TPL_FILE'
    yaml_file_variables = 'FILE_VARIABLES'

    try:
        # Locate YAML configuration in the same directory as this module
        current_dir = os.path.dirname(os.path.abspath(__file__))
        arguments_file = os.path.join(current_dir, 'arguments.yml')
        if not os.path.isfile(arguments_file):
            raise FileNotFoundError(f"YAML file not found: {arguments_file}")

        with open(arguments_file, 'r') as yml_file:
            yaml_data = yaml.safe_load(yml_file)

        # Validate species file path and extension
        if species_file_path is None:
            raise ValueError("The 'species_file_path' argument is required and must be specified by the user.")

        spe_extension = yaml_data[yml_species_block][yaml_file_variables].get('spe_file_extension', '.SPE')
        validated_spe_file_path = validate_file(species_file_path, spe_extension)

        # Read template-related defaults from YAML
        function_arguments = yaml_data[yml_species_block][yaml_file_variables]
        mrk = validate_marker(mrk, "mrk")

        if new_template_file_extension is None:
            new_template_file_extension = function_arguments['new_template_file_extension']
        if tpl_first_line is None:
            tpl_first_line = function_arguments['tpl_first_line']

        # Read the entire species file into a list of lines
        file_content = read_dssat_file(validated_spe_file_path)
        lines = file_content.split('\n')

        # Parameter value dicts (keyed initially by full parameter name)
        current_parameter_values = {}
        minima_parameter_values = {}
        maxima_parameter_values = {}

        # Mapping from full parameter name -> truncated PEST ID
        parameter_name_truncated = {}

        # Normalised parameter definitions: [{'name','line','column','min','max','group'}, ...]
        normalized_parameters = []

        # Normalise user-provided parameter specifications
        for param_name, spec in parameters_grouped.items():
            full_name = str(param_name).strip()

            # Tuple/list syntax: (line, column, min, max[, group])
            if isinstance(spec, (tuple, list)):
                if len(spec) < 4:
                    raise ValueError(
                        f"Parameter '{full_name}' must be specified as "
                        "(line, column, min, max[, group]) when using tuple/list syntax."
                    )
                line = spec[0]
                column = spec[1]
                p_min = spec[2]
                p_max = spec[3]
                group = spec[4] if len(spec) > 4 else full_name

            # Dict syntax with explicit keys
            elif isinstance(spec, dict):
                try:
                    line = spec['line']
                    column = spec['column']
                    p_min = spec['min']
                    p_max = spec['max']
                except KeyError as exc:
                    raise ValueError(
                        f"Parameter '{full_name}' dictionary must contain 'line', 'column', 'min', and 'max' keys."
                    ) from exc
                group = spec.get('group', full_name)

            else:
                raise ValueError(
                    f"Parameter '{full_name}' must be specified as a tuple/list "
                    "(line, column, min, max[, group]) or as a dictionary."
                )

            # Ensure integer indices for line and column
            try:
                line = int(line)
                column = int(column)
            except Exception as exc:
                raise ValueError(
                    f"'line' and 'column' for parameter '{full_name}' must be integers."
                ) from exc

            normalized_parameters.append(
                {
                    'name': full_name,
                    'line': line,
                    'column': column,
                    'min': p_min,
                    'max': p_max,
                    'group': str(group).strip(),
                }
            )

        # Helper: for a given line, compute token spans and field spans
        def compute_token_and_field_spans(line_text):
            """
            For a given line, compute:
              - token_spans: (start, end) positions of each non-space token,
                             in the same order as line_text.split().
              - field_spans: (start, end) positions of the column "fields"
                             that hold those tokens.

            Rules:
              * token_spans follow Python's split() order and find() positions.
              * Field 1 covers the first token plus all contiguous spaces
                immediately to its left, leaving exactly one space margin
                at the far left if possible.
              * For fields i>1, the left boundary is at most one column to
                the right of the previous field end, but never to the right
                of the token start.
            """

            # Find all tokens in split() order
            raw_tokens = line_text.split()
            token_spans = []
            search_pos = 0
            for tok in raw_tokens:
                idx = line_text.find(tok, search_pos)
                if idx == -1:
                    raise ValueError(f"Could not locate token '{tok}' in line: {line_text}")
                token_spans.append((idx, idx + len(tok)))
                search_pos = idx + len(tok)

            if not token_spans:
                return [], []

            field_spans = []
            prev_field_end = None

            for i, (tok_start, tok_end) in enumerate(token_spans):
                if i == 0:
                    # First field: extend as far left as possible over spaces,
                    # but always leave a one-column margin at the far left.
                    left = tok_start
                    while left > 1 and line_text[left - 1].isspace():
                        left -= 1
                    field_start = left
                else:
                    # Later fields: start at previous field_end + 1, but not
                    # beyond the token's own start
                    candidate_start = prev_field_end + 1
                    field_start = min(tok_start, candidate_start)

                field_end = tok_end
                field_spans.append((field_start, field_end))
                prev_field_end = field_end

            return token_spans, field_spans

        # First pass: assign truncated IDs based on field widths, enforce uniqueness
        used_truncated_ids = set()

        for param_def in normalized_parameters:
            full_name = param_def['name']
            line_number_user = param_def['line']
            column_index = param_def['column']

            # 1-based line index from user -> 0-based in list
            line_idx = line_number_user - 1
            if line_idx < 0 or line_idx >= len(lines):
                raise ValueError(
                    f"Line index {line_number_user} for parameter '{full_name}' is out of range "
                    f"in file {validated_spe_file_path}."
                )

            line_text = lines[line_idx]
            # Compute token spans and corresponding field spans once for this line
            token_spans, field_spans = compute_token_and_field_spans(line_text)

            # Validate column index relative to tokens
            if column_index < 1 or column_index > len(token_spans):
                raise ValueError(
                    f"Column index {column_index} for parameter '{full_name}' is out of range "
                    f"on line {line_number_user}."
                )

            # Field span for this column gives the width available for the marker
            field_start, field_end = field_spans[column_index - 1]
            field_width = field_end - field_start

            # Maximum length for the ID inside this field (two chars reserved for markers)
            max_id_len = max(1, field_width - 2)

            # Start base_id from a short code (first 3 characters of the name)
            base_id = full_name.strip()
            if len(base_id) > 3:
                base_id = base_id[:3]

            # Enforce maximum length inside the field
            if len(base_id) > max_id_len:
                base_id = base_id[:max_id_len]

            # If there is still room, pad on the right to use full width
            if len(base_id) < max_id_len:
                base_id = base_id.ljust(max_id_len)

            truncated = base_id
            counter = 0
            # Ensure unique IDs by altering the tail with numeric suffixes when needed
            while truncated in used_truncated_ids:
                suffix = str(counter)
                if len(base_id) > len(suffix):
                    truncated = base_id[:-len(suffix)] + suffix
                else:
                    truncated = base_id + suffix
                counter += 1

            used_truncated_ids.add(truncated)
            parameter_name_truncated[full_name] = truncated

        # Second pass: build markers and modify lines
        # Work on a copy of lines so multiple parameters on the same line compose correctly
        line_buffer = list(lines)

        for param_def in normalized_parameters:
            full_name = param_def['name']
            line_number_user = param_def['line']
            column_index = param_def['column']
            p_min = param_def['min']
            p_max = param_def['max']

            line_idx = line_number_user - 1
            line_text = line_buffer[line_idx]

            token_spans, field_spans = compute_token_and_field_spans(line_text)

            field_start, field_end = field_spans[column_index - 1]
            token_start, token_end = token_spans[column_index - 1]

            field_width = field_end - field_start
            token_str = line_text[token_start:token_end]

            # Store the original numeric value and bounds using the full parameter name
            current_value = token_str.strip()
            current_parameter_values[full_name] = current_value
            minima_parameter_values[full_name] = p_min
            maxima_parameter_values[full_name] = p_max

            # Build the marker using the precomputed truncated ID
            truncated_id = parameter_name_truncated[full_name]

            # Available characters inside the field for the ID (excluding markers)
            max_id_len = max(1, field_width - 2)

            # Start from the truncated ID, further limit to max_id_len and strip spaces
            base_core = truncated_id[:max_id_len].strip()

            # Now always pad with '-' to exactly max_id_len
            if len(base_core) > max_id_len:
                base_core = base_core[:max_id_len]
            if len(base_core) < max_id_len:
                base_core = base_core.ljust(max_id_len, '-')

            id_for_marker = base_core

            marker_core = f"{mrk}{id_for_marker}{mrk}"
            # If marker is still too wide for the field, trim the ID further
            while len(marker_core) > field_width and len(id_for_marker) > 1:
                id_for_marker = id_for_marker[:-1]
                marker_core = f"{mrk}{id_for_marker}{mrk}"

            # Right-align marker inside the field, using spaces to the left if available
            marker = marker_core.rjust(field_width)

            # Replace the field region in the line with the marker
            new_line = line_text[:field_start] + marker + line_text[field_end:]
            line_buffer[line_idx] = new_line

        # Insert PEST header, write TPL, and build return structures
        line_buffer.insert(0, f"{tpl_first_line} {mrk}")

        output_path = validate_output_path(output_path)
        output_new_file_path = os.path.join(
            output_path,
            os.path.splitext(os.path.basename(validated_spe_file_path))[0] + '_SPE' + '.' + new_template_file_extension
        )

        with open(output_new_file_path, 'w') as file:
            file.write("\n".join(line_buffer))

        # Translate dictionaries from full_name keys to truncated IDs
        current_parameter_values = {
            parameter_name_truncated[k]: v
            for k, v in current_parameter_values.items()
            if k in parameter_name_truncated
        }
        minima_parameter_values = {
            parameter_name_truncated[k]: v
            for k, v in minima_parameter_values.items()
            if k in parameter_name_truncated
        }
        maxima_parameter_values = {
            parameter_name_truncated[k]: v
            for k, v in maxima_parameter_values.items()
            if k in parameter_name_truncated
        }

        # Build group definitions (group -> comma-separated truncated IDs)
        grouped_truncated = {}
        for param_def in normalized_parameters:
            full_name = param_def['name']
            group_name = param_def['group']
            if full_name in parameter_name_truncated:
                tid = parameter_name_truncated[full_name]
                grouped_truncated.setdefault(group_name, []).append(tid)

        grouped_truncated = {g: ', '.join(v) for g, v in grouped_truncated.items()}

        print(f"Template file successfully created at: {output_new_file_path}")

        return {
            'parameters': current_parameter_values,
            'minima_parameters': minima_parameter_values,
            'maxima_parameters': maxima_parameter_values,
            'parameters_grouped': grouped_truncated,
        }, output_new_file_path

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except FileNotFoundError as fe:
        print(f"FileNotFoundError: {fe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
