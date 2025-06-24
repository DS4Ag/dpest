Example: Calibrating DSSAT for Wheat (CERES Model)
===================================================

This example demonstrates how to use ``dpest`` to create the necessary files for calibrating the CERES-Wheat model (DSSAT Version 4.8) using the ``SWSW7501WH N RESPONSE`` experiment.

1. Run DSSAT
------------

*   Follow these steps within the DSSAT software:

    1.  Launch DSSAT.
    2.  Click "Selector".
    3.  Expand "Crops" and select "Wheat".
    4.  In the "Data" panel select the "SWSW7501.WHX" experiment.
    5.  Click "Run" button in the toolbar.
    6.  In the "Simulation" popup window, choose "CERES" as the crop model.
    7.  Click "Run Model" and wait for the simulation to finish.

.. raw:: html

    <iframe 
            width="700"
            height="400"
            src="https://www.youtube.com/embed/dzKpvJSEXZc?vq=hd1080"
            frameborder="0" allowfullscreen>
    </iframe>

2. Using ``dpest`` create the PEST input files to perform the calibration
----------------------------------------------
For this example, we are going to calibrate the ``MANITOU`` wheat cultivar (Cultivar ID: ``IB1500``) using the field-collected data from the ``164.0 KG N/HA IRRIG`` treatment of the ``SWSW7501.WHX`` experiment. The experiment information is found in the ``C:/DSSAT48/Wheat/SWSW7501.WHX`` file.  

**2.1. Import the dpest Package**

.. code-block:: python

              import dpest


**2.2. Create the Cultivar Template File**  

The first step is to create the cultivar Template File (``.TPL``) for the ``MANITOU`` cultivar, which is the cultivar planted in the ``164.0 KG N/HA IRRIG`` treatment of the ``SWSW7501.WHX`` experiment. To achieve this, we use the ``dpest.wheat.ceres.cul()`` function, as shown below:  

.. code-block:: python  

    import dpest  

    cultivar_parameters, cultivar_tpl_path = dpest.wheat.ceres.cul(
        P = 'P1D, P5', 
        G = 'G1, G2, G3', 
        PHINT = 'PHINT',
        cultivar = 'MANITOU',
        cul_file_path = './DSSAT48/Genotype/WHCER048.CUL'
    )  

After running this function:  

- The ``cultivar_parameters`` variable stores a dictionary containing the parameter groups and sections needed to generate the ``.PST`` file.  
- The ``cultivar_tpl_path`` variable stores the file path of the generated ``.TPL`` file, which will be used in creating the ``.PST`` file.

Note that the cultivar template file named ``WHCER048_CUL.TPL`` will be created in the current working directory. 

**2.3. Create Instructions Files**

For this experiment, key end-of-season crop performance metrics and phenological observations were collected and recorded in the ``C:/DSSAT48/Wheat/SWSW7501.WHA`` file (referred to as the ``A File``). Additionally, time-series data were collected and recorded in the ``C:/DSSAT48/Wheat/SWSW7501.WHT`` file (referred to as the ``T File``). To create the PEST instruction files, we will use the ``overview()`` and ``plantgro()`` modules. The ``overview()`` module will create the instruction file to compare the model simulations from the ``'C:/DSSAT48/Wheat/OVERVIEW.OUT'`` file with the measured data from the ``A File``, while the ``plantgro()`` module will create the instruction file to compare the time-series model simulations from the ``'C:/DSSAT48/Wheat/PlantGro.OUT'`` file with the time-series measured data from the ``T File``.

.. code-block:: python

    # Create OVERVIEW observations INS file
    overview_observations, overview_ins_path = dpest.wheat.overview(
        treatment = '164.0 KG N/HA IRRIG',  # Treatment Name
        overview_file_path = './DSSAT48/Wheat/OVERVIEW.OUT'  # Path to the OVERVIEW.OUT file
    )

    # Create PlantGro observations INS file
    plantgro_observations, plantgro_ins_path = dpest.wheat.plantgro(
        treatment = '164.0 KG N/HA IRRIG',  # Treatment Name
        variables = ['LAID', 'CWAD', 'T#AD'],  # Variables to calibrate
        plantgro_file_path = './DSSAT48/Wheat/PlantGro.OUT'  # Path to the PlantGro.OUT file
    )

After running these functions:

- The ``overview_observations`` variable stores the DataFrame with the observations needed for the ``.PST`` file's observations and observation group sections.
- The ``overview_ins_path`` variable stores the path to the instruction file created by the ``overview()`` module, which will be used in the ``input_output_file_pairs`` argument of the ``pst`` module to match the original ``OVERVIEW.OUT`` file to the instruction file.
- The ``plantgro_observations`` variable stores the DataFrame with the time-series observations needed for the ``.PST`` file's observations and observation group sections.
- The ``plantgro_ins_path`` variable stores the path to the instruction file created by the ``plantgro()`` module, which will be used in the ``input_output_file_pairs`` argument of the ``pst`` module to match the original ``PlantGro.OUT`` file to the instruction file.

Note that the ``OVERVIEW.INS`` and ``PlantGro.INS`` instruction files will be created in the current working directory.

**2.4. Create the PEST Control File**

After creating the ``template file`` and ``instruction files`` for calibrating the ``MANITOU`` wheat cultivar, the next step is to generate the ``PEST control file (.PST``). This file integrates all necessary components and guides the ``calibration process``.

The ``.PST`` file is created using the ``variables`` obtained in ``2.2`` and ``2.3``. Additionally, we need to specify the ``command-line instruction`` to execute the DSSAT model. For more information on how to run DSSAT from the command line, visit the `DSSAT Power Users Guide <https://dssat.net/tools/tools-for-power-users/>`_.

The following Python script provides an example of how to run the ``DSSAT CERES-Wheat model`` using Python:

.. code-block:: python

    import os
    import subprocess
    from dpest.wheat.utils import uplantgro

    # User-editable section for system DSSAT installation
    dssat_install_dir = r'C:\DSSAT48'  # System DSSAT installation folder
    dssat_exe = os.path.join(dssat_install_dir, 'DSCSM048.EXE')
    control_file = os.path.join(dssat_install_dir, 'Wheat', 'DSSBatch.v48')

    # Project data directory (relative to script location)
    project_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(project_dir, 'DSSAT48')
    output_dir = os.path.join(data_dir, 'Wheat')

    # Change working directory to the output directory
    os.chdir(output_dir)

    # Build and run DSSAT command
    module = 'CSCER048'
    switch = 'B'
    command_line = f'"{dssat_exe}" {module} {switch} "{control_file}"'
    result = subprocess.run(command_line, shell=True, check=True, capture_output=True, text=True)
    print(result.stdout)

    # Use uplantgro from dpest.wheat.utils to extract and update data from PlantGro.OUT if needed
    uplantgro(
        plantgro_file_path=os.path.join(output_dir, 'PlantGro.OUT'),
        treatment='164.0 KG N/HA IRRIG',
        variables=['LAID', 'CWAD', 'T#AD']
    )

**Download the example of a Python script to run DSSAT**

`run_dssat.py <https://raw.githubusercontent.com/DS4Ag/dpest/refs/heads/main/examples/wheat/ceres/run_dssat.py>`_ *(Click to download if not already in your directory)*

.. important::

   The provided run_dssat.py script is set up so that DSSAT writes its output files directly into the project’s data directory (e.g., DSSAT48/Wheat). This ensures PEST always reads the latest simulation results.

   If you use a different method to run DSSAT (such as your own script, a batch file, or a direct executable call), you must:

   - Ensure that DSSAT outputs are written to the correct directory referenced in your .pst file.
   - Update the * model command line in the .pst file to match your actual execution command.
   - Double-check that the output files are being updated with each run, so PEST uses the latest results.
   - For more on running DSSAT from the command line and managing outputs, see the `DSSAT Power Users Guide <https://dssat.net/tools/tools-for-power-users/>`_.

   The run_dssat.py script is provided as a reference. Adapt it as needed for your own DSSAT installation and workflow.


**Where to save and how to call the Python script for PEST**

The Python script ``run_dssat.py`` is configured to be saved in the root directory of your project (i.e., in the same folder as your main project files and the ``DSSAT48`` data directory).

When specifying the command to execute this script in the PEST control file (``.PST``), use a command that correctly references the script’s filename and its path relative to the directory where you run PEST.

For example, if the script is named ``run_dssat.py`` and is located in the project root, the command to execute it would be::

   py ./run_dssat.py

or equivalently::

   python ./run_dssat.py

This command should be included exactly as shown in the ``* model command line`` section of your ``.PST`` file.

    **Generate the PEST Control File (.PST)**

Once the script is saved, we can generate the ``PEST control file`` using the following function:

.. code-block:: python

    dpest.pst(
        cultivar_parameters = cultivar_parameters,
        dataframe_observations = [overview_observations, plantgro_observations],
        model_comand_line = r'py ./run_dssat.py',  # Command to run the model
        input_output_file_pairs = [
            (cultivar_tpl_path, './DSSAT48/Genotype/WHCER048.CUL'),  # Template file → Target file
            (overview_ins_path , './DSSAT48/Wheat/OVERVIEW.OUT'),  # Instruction file → Target file
            (plantgro_ins_path , './DSSAT48/Wheat/PlantGro.OUT')  # Instruction file → Target file
        ]
    )

After running this function:

- The ``.PST`` file will be created in the working directory.
- The ``template file`` and ``instruction files`` will be linked to their corresponding model input and output files.
- The ``command-line instruction`` to run DSSAT is stored in the ``.PST`` file.

The ``.PST`` file serves as the ``main configuration file`` for running PEST and calibrating the DSSAT model.


3. Validate the Created PEST Input Files
--------------------------------------------

After generating the ``PEST input files``, it is important to validate that they were created correctly. To ensure that all input files are correctly formatted before running PEST, use TEMPCHEK, INSCHEK and PESTCHEK utilities provided by PEST:

**3.1. Open the Command Prompt**

To begin the validation process, open the Command Prompt (or terminal, if using a different operating system)

**3.2. Navigate to the Working Directory**

Once the Command Prompt (or terminal) is open, navigate to the directory where the ``PEST input files`` were created. Use the following command to change to the working directory (replace with your actual path):

.. code-block::

    cd path_to_your_directory

**3.3. Validate PEST Files**

Run the following commands to validate the different PEST input files. Each validation command checks a specific file. The instructions are provided as comments next to each command:

.. code-block::

    # Validate the Template File (.TPL)
    tempchek.exe WHCER048_CUL.TPL 

    # Validate the Overview Instruction File (.INS)
    inschek.exe OVERVIEW.ins ./DSSAT48/Wheat/OVERVIEW.OUT

    # Validate the PlantGro Instruction File (.INS)
    inschek.exe PlantGro.ins ./DSSAT48/Wheat/PlantGro.OUT

    # Validate the PEST Control File (.PST)
    pestchek.exe PEST_CONTROL.pst  

If the files are correctly formatted and no errors are found, the output will confirm this (e.g., "No errors encountered").


4. Run the Calibration  
----------------------

After successfully validating the ``PEST input files``, the final step is to run the calibration process.

Run the following command in the Command Prompt (or terminal, if using a different operating system) to start ``PEST`` in parameter estimation mode:

.. code-block:: console

   PEST.exe PEST_CONTROL.pst