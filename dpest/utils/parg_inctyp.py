def parg_inctyp(pst_path, updates):
    """
    Updates INCTYP values for one or more parameter groups in a PEST control (.pst) file.

    The ``INCTYP`` field specifies the increment type used by PEST for derivative
    calculations in the ``* parameter groups`` section. Typical values are
    ``relative`` and ``absolute``. This function modifies the ``* parameter groups``
    section of an existing ``.pst`` file in place.

    **Required Arguments:**
    =======

        * **pst_path** (*str*):
            Path to the ``.pst`` PEST control file to modify.

        * **updates** (*dict*):
            Dictionary mapping parameter group names to new ``INCTYP`` values.

            Example::

                {
                    "PART_SEED": "relative",
                    "SEED_COMP": "absolute"
                }

    **Returns:**
    =======

        * ``None``

        The function updates the ``* parameter groups`` section in place.

    **Examples:**
    =======

    1. **Update INCTYP for two parameter groups:**

       .. code-block:: python

          from dpest.utils import parg_inctyp

          parg_inctyp(
              pst_path = "A-1_input/PEST_CONTROL.pst",
              updates = {
                  "PART_SEED": "relative",
                  "SEED_COMP": "relative"
              }
          )

    2. **Set one parameter group to absolute increments:**

       .. code-block:: python

          from dpest.utils import parg_inctyp

          parg_inctyp(
              pst_path = "PEST_CONTROL.pst",
              updates = {
                  "SEED_COMP": "absolute"
              }
          )
    """
    try:
        import os

        # Validate pst_path
        if not os.path.isfile(pst_path):
            raise FileNotFoundError(f"File not found: {pst_path}")

        # Validate updates
        if not isinstance(updates, dict) or len(updates) == 0:
            raise ValueError("`updates` must be a non-empty dictionary.")

        allowed_values = {"absolute", "relative"}

        validated_updates = {}
        for group_name, new_value in updates.items():
            if not isinstance(group_name, str) or not group_name.strip():
                raise ValueError(f"Invalid parameter group name: {group_name}")

            if not isinstance(new_value, str):
                raise ValueError(
                    f"INCTYP value for group '{group_name}' must be a string."
                )

            clean_value = new_value.strip().lower()
            if clean_value not in allowed_values:
                raise ValueError(
                    f"INCTYP for group '{group_name}' must be one of: {sorted(allowed_values)}"
                )

            validated_updates[group_name.strip()] = clean_value

        # Read PST file
        with open(pst_path, 'r') as f:
            lines = f.readlines()

        # Find * parameter groups section
        section_start_idx = None
        section_end_idx = None

        for i, line in enumerate(lines):
            if line.strip().lower().startswith('* parameter groups'):
                section_start_idx = i
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith('*'):
                    j += 1
                section_end_idx = j
                break

        if section_start_idx is None:
            raise ValueError(
                "This file does not contain a '* parameter groups' section and is not a valid PEST control file."
            )

        # Process lines in the section
        found_groups = set()

        for i in range(section_start_idx + 1, section_end_idx):
            current_line = lines[i]

            # Skip empty lines
            if not current_line.strip():
                continue

            values = current_line.split()
            if len(values) < 2:
                continue

            group_name = values[0]

            if group_name in validated_updates:
                values[1] = validated_updates[group_name]  # INCTYP is 2nd value
                current_padding = len(current_line) - len(current_line.lstrip())
                new_line = " " * current_padding + "   ".join(values) + "\n"
                lines[i] = new_line
                found_groups.add(group_name)

        # Check that all requested groups were found
        missing_groups = set(validated_updates.keys()) - found_groups
        if missing_groups:
            raise ValueError(
                "The following parameter groups were not found in the '* parameter groups' section: "
                + ", ".join(sorted(missing_groups))
            )

        # Write updated file
        with open(pst_path, 'w') as f:
            f.writelines(lines)

        print(
            f"INCTYP updated successfully for parameter groups: {', '.join(sorted(found_groups))}"
        )

    except FileNotFoundError as fe:
        print(f"Error: {str(fe)}")
    except ValueError as ve:
        print(f"ValueError: {str(ve)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")