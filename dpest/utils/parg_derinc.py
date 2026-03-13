def parg_derinc(pst_path, updates):
    """
    Updates DERINC values for one or more parameter groups in a PEST control (.pst) file.

    The ``DERINC`` value controls the initial derivative increment used by PEST for
    parameters belonging to a given parameter group. This function modifies the
    ``* parameter groups`` section of an existing ``.pst`` file in place.

    This is useful when some groups contain parameters with very narrow bounds and
    the default derivative increment written by ``dpest.pst()`` is too large, causing
    ``pestchek.exe`` to return errors such as:

    * ``Initial derivative increment for parameter ... greater than parameter range divided by 3.2``

    **Required Arguments:**
    =======

        * **pst_path** (*str*):
            Path to the ``.pst`` PEST control file to modify.

        * **updates** (*dict*):
            Dictionary mapping parameter group names to new ``DERINC`` values.

            Example::

                {
                    "PART_SEED": 1.0e-03,
                    "SEED_COMP": 1.0e-03
                }

    **Returns:**
    =======

        * ``None``

        The function updates the ``* parameter groups`` section in place.

    **Examples:**
    =======

    1. **Update DERINC for two parameter groups:**

       .. code-block:: python

          from dpest.utils import parg_derinc

          parg_derinc(
              pst_path = "A-1_input/PEST_CONTROL.pst",
              updates = {
                  "PART_SEED": 1.0e-03,
                  "SEED_COMP": 1.0e-03
              }
          )

    2. **Update DERINC for a single parameter group:**

       .. code-block:: python

          from dpest.utils import parg_derinc

          parg_derinc(
              pst_path = "PEST_CONTROL.pst",
              updates = {
                  "PHOTO": 5.0e-03
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

        validated_updates = {}
        for group_name, new_value in updates.items():
            if not isinstance(group_name, str) or not group_name.strip():
                raise ValueError(f"Invalid parameter group name: {group_name}")

            try:
                new_value = float(new_value)
            except Exception:
                raise ValueError(
                    f"DERINC value for group '{group_name}' must be numeric. Got: {new_value}"
                )

            if new_value <= 0:
                raise ValueError(
                    f"DERINC value for group '{group_name}' must be greater than zero."
                )

            validated_updates[group_name.strip()] = new_value

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
            if len(values) < 3:
                continue

            group_name = values[0]

            if group_name in validated_updates:
                values[2] = f"{validated_updates[group_name]:.6E}"  # DERINC is 3rd value
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
            f"DERINC updated successfully for parameter groups: {', '.join(sorted(found_groups))}"
        )

    except FileNotFoundError as fe:
        print(f"Error: {str(fe)}")
    except ValueError as ve:
        print(f"ValueError: {str(ve)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")