dpest
=======================

A Python package for automating PEST (Parameter Estimation) file creation for DSSAT crop model calibration using time series data.

What is dpest?
==============

``dpest`` is a Python package designed to automate the creation of `PEST (Parameter Estimation and Uncertainty Analysis) <https://pesthomepage.org/>`_ control files for calibrating `DSSAT (Decision Support System for Agrotechnology Transfer) <https://dssat.net/>`_ crop models. Currently, ``dpest`` is capable of calibrating DSSAT wheat models only. It generates template files for cultivar and ecotype parameters, instruction files for ``OVERVIEW.OUT`` and ``PlantGro.OUT``, and the main PEST control file. A utility module is also included to extend ``PlantGro.OUT`` files for complete time series compatibility.

Key Features
============

- Automated generation of ``PEST control files (.PST)``.
- Compatibility with DSSAT wheat models.
- Creation of ``PEST template files (.TPL)`` for cultivar and ecotype parameters.
- Generation of ``PEST instruction files (.INS)`` for key DSSAT output files.
- Utility module to extend ``PlantGro.OUT`` files for complete time series.

Installation
============

``dpest`` can be installed via pip from `PyPI <https://pypi.org/project/dpest/>`_.

::

    pip install dpest

Prerequisites
=============

1. **DSSAT Software:** `DSSAT (version 4.8) <https://dssat.net/>`_ must be installed on your system.
2. **DSSAT Experiment Data:** You'll need a DSSAT experiment to work with. The example below uses the ``SWSW7501WH N RESPONSE`` wheat experiment.
3. **PEST Software:** You’ll need to have `PEST (version 18) <https://pesthomepage.org/>`_ installed.

How to Use dpest?
=================

Jupyter notebook example
------------------------

We provide a Jupyter notebook example (`usage_example.ipynb <https://github.com/DS4Ag/dpest/blob/main/examples/wheat/ceres/usage_example.ipynb>`_) that demonstrates all package functions in a practical workflow and includes steps for using PEST’s “check” functions to validate the generated input files.

Read the Docs
-------------

For a **detailed, step-by-step example**, please refer to the official documentation:
`Complete Example on Read the Docs <https://dpest.readthedocs.io/en/latest/example.html>`_

Basic Usage
-----------

The following steps provide a brief overview of how to use ``dpest``.

1. **Locate DSSAT Genotype Files:** The cultivar (``.CUL``) and ecotype (``.ECO``) files are typically included with the DSSAT installation. These are usually found in the ``C:\DSSAT48\Genotype\`` directory.
2. **Run a DSSAT Simulation:** Execute a DSSAT simulation for your chosen wheat experiment using the CERES model. This will generate the necessary output files (``OVERVIEW.OUT`` and ``PlantGro.OUT``), typically found in the ``C:\DSSAT48\Wheat\`` directory.

   2.1. Launch DSSAT.
   2.2. Click "Selector".
   2.3. Expand "Crops" and select "Wheat".
   2.4. In the "Data" panel select the "SWSW7501.WHX" experiment.
   2.5. Click "Run" button in the toolbar.
   2.6. In the "Simulation" popup window, choose "CERES" as the crop model.
   2.7. Click "Run Model" and wait for the simulation to finish.

3. **Import the ``dpest`` Package:**

   To import the entire ``dpest`` package:

   .. code-block:: python

      import dpest

   To import specific modules:

   .. code-block:: python

      from dpest import cul, eco, overview, ts, pst, uts

      # Now you can use the functions directly:
      cul(...)
      eco(...)
      overview(...)
      ts(...)
      pst(...)
      uts(...)

4. **Use the Modules**

   - ``cul()``: This module creates `PEST template files (.TPL)` for CERES-Wheat cultivar parameters. Use it to generate template files for cultivar calibration.
   - ``eco()``: This module creates `PEST template files (.TPL)` for CERES-Wheat ecotype parameters. Use it to generate template files for ecotype calibration.
   - ``overview()``: This module creates `PEST instruction files (.INS)` for reading observed (*measured*) values of key end-of-season crop performance metrics and key phenological observations from the `OVERVIEW.OUT` file. The instruction file tells PEST how to extract model-generated observations from the `OVERVIEW.OUT` file, compare them with the observations from the DSSAT `A file`, and adjust model parameters accordingly.
   - ``plantgro()``: This module creates `PEST instruction files (.INS)` for reading observed (*measured*) values of plant growth dynamics from the time-series output `.OUT` files . The instruction file tells PEST how to extract time-series data from the `.OUT` file, compare that data with the time-series data provided in the DSSAT `T file`, and adjust model parameters accordingly.
   - ``pst()``: This module creates the main `PEST control file (.PST)`.
   - ``uplantgro()``: This module extends time-series output `.OUT` files by adding rows when the plant maturity simulation date occurs before a measured observation date.

5. **Create Template Files and Instruction Files:** Use the ``dpest`` modules to generate ``PEST template files (.TPL)`` for cultivar and ecotype parameters, and ``PEST instruction files (.INS)`` for the ``OVERVIEW.OUT`` and time-series output ``.OUT`` files.

   .. code-block:: python

      import dpest

      # 1. Create CULTIVAR parameters TPL file
      cultivar_parameters, cultivar_tpl_path = dpest.cul(
          P = 'P1D, P5', # How the user should enter the parameters
          G = 'G1, G2, G3',
          PHINT = 'PHINT',
          cultivar = 'MANITOU',
          cul_file_path = 'C:/DSSAT48/Genotype/WHCER048.CUL'
      )

      # 2. Create OVERVIEW observations INS file
      overview_observations,  overview_ins_path = dpest.overview(
          treatment = '164.0 KG N/HA IRRIG', #Treatment Name
          overview_file_path = 'C:/DSSAT48/Wheat/OVERVIEW.OUT' #Path to the OVERVIEW.OUT file
      )
      # 3. Create PlantGro observations INS file
      plantgro_observations, plantgro_ins_path = dpest.ts(
          treatment = '164.0 KG N/HA IRRIG', #Treatment Name
          variables = ['LAID', 'CWAD', 'T#AD'], #Variables to calibrate
          ts_file_path = 'C:/DSSAT48/Wheat/PlantGro.OUT', #Path to the PlantGro.OUT file
      )

6. **Create the PEST Control File:** Use the ``dpest.pst()`` module to generate the main ``PEST control file (.PST)``.

   .. code-block:: python

      # 4. Create the PST file
      dpest.pst(
          cultivar_parameters = cultivar_parameters,
          dataframe_observations = [overview_observations, plantgro_observations],
          model_comand_line = r'py "C:\pest18\run_dssat.py"', #Command line to run the model
          input_output_file_pairs = [
              (cultivar_tpl_path, 'C://DSSAT48/Genotype/WHCER048.CUL'), #Template file and the file to be modified
              (overview_ins_path , 'C://DSSAT48/Wheat/OVERVIEW.OUT'), #Instruction file and the file to be modified
              (plantgro_ins_path , 'C://DSSAT48/Wheat/PlantGro.OUT') #Instruction file and the file to be modified
          ]
      )

7. **Run PEST:** Calibrate the model using PEST.

Utilities for Editing PEST Control Files
========================================

In addition to automating the creation of PEST control and template files for DSSAT CERES-Wheat model calibration, ``dpest`` includes a growing set of utility functions under ``dpest.utils`` for directly modifying existing ``.pst`` (PEST control) files.

Why use ``dpest.utils``?
------------------------

Unlike libraries such as `pyEMU <https://pyemu.readthedocs.io/en/develop/pyemu.pst.html>`_, which parse ``.pst`` files into Python objects and rewrite the entire file when saving any change, ``dpest.utils`` performs lightweight, line-by-line edits to preserve the original structure and untouched content.

These utilities:

- Edit existing ``.pst`` files in place, without reconstructing or redefining unrelated fields.
- Are model-agnostic: they work with any ``.pst`` file, not just DSSAT-related ones.
- Only modify model-independent control parameters (e.g., optimization settings), leaving parameter and data blocks untouched.

This makes them ideal for **quickly tuning optimization settings** or **cleaning up ``.pst`` files** generated by ``dpest`` or other tools.

Example Usage
-------------

.. code-block:: python

    # Load the dpest.utils
    from dpest.utils import noptmax, rmv_splitcols

    # Path to the .pst file
    pst_file_path = './ENTRY1/PEST_CONTROL.pst'

    # Increase the number of optimization iterations (NOPTMAX) in a .pst file
    noptmax(pst_file_path, new_value=50)

    # Remove SPLITTHRESH/SPLITRELDIFF/SPLITACTION columns from a .pst file parameter groups section
    rmv_splitcols("PEST_CONTROL.pst")



.. toctree::
   :maxdepth: 1
   :caption: Home
   :hidden:

   Home <self>

.. toctree::
   :maxdepth: 2
   :caption: Create genotype parameters template file
   :hidden:

   dpest.cul
   dpest.eco
   dpest.spe

.. toctree::
   :maxdepth: 2
   :caption: Create measured and simulated observation instruction files
   :hidden:

   dpest.overview
   dpest.ts
   dpest.uts

.. toctree::
   :maxdepth: 2
   :caption: Create template file for the PEST calibration
   :hidden:

   dpest.pst

.. toctree::
   :maxdepth: 2
   :caption: Update the PEST template calibration file
   :hidden:

   dpest.utils

.. toctree::
   :maxdepth: 2
   :caption: Examples
   :hidden:

   example
   example_multiple_trts