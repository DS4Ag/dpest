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
        cul_file_path = 'C:/DSSAT48/Genotype/WHCER048.CUL'
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
        overview_file_path = 'C:/DSSAT48/Wheat/OVERVIEW.OUT'  # Path to the OVERVIEW.OUT file
    )

    # Create PlantGro observations INS file
    plantgro_observations, plantgro_ins_path = dpest.wheat.plantgro(
        treatment = '164.0 KG N/HA IRRIG',  # Treatment Name
        variables = ['LAID', 'CWAD', 'T#AD'],  # Variables to calibrate
        plantgro_file_path = 'C:/DSSAT48/Wheat/PlantGro.OUT'  # Path to the PlantGro.OUT file
    )

After running these functions:

- The ``overview_observations`` variable stores the DataFrame with the observations needed for the ``.PST`` file's observations and observation group sections.
- The ``overview_ins_path`` variable stores the path to the instruction file created by the ``overview()`` module, which will be used in the ``input_output_file_pairs`` argument of the ``pst`` module to match the original ``OVERVIEW.OUT`` file to the instruction file.
- The ``plantgro_observations`` variable stores the DataFrame with the time-series observations needed for the ``.PST`` file's observations and observation group sections.
- The ``plantgro_ins_path`` variable stores the path to the instruction file created by the ``plantgro()`` module, which will be used in the ``input_output_file_pairs`` argument of the ``pst`` module to match the original ``PlantGro.OUT`` file to the instruction file.

Note that the ``OVERVIEW.INS`` and ``PlantGro.INS`` instruction files will be created in the current working directory.

**2.4. Create the PEST Control File**

After creating the ``template file`` and ``instruction files`` for calibrating the ``MANITOU`` wheat cultivar, the next step is to generate the ``PEST control file (.PST``). This file integrates all necessary components and guides the ``calibration process``.

The ``.PST`` file is created using the ``variables`` obtained in ``2.2`` and ``2.3``. Additionally, we need to specify the ``command-line instruction`` to execute the DSSAT model. For more information on how to run DSSAT from the command line, visit the `DSSAT web documentation <https://dssat.net/tools/tools-for-power-users/>`_.

The following Python script provides an example of how to run the ``DSSAT CERES-Wheat model`` using Python:

.. code-block:: python

    import os
    import subprocess
    from dpest.wheat.utils import uplantgro

    def build_path(*args):
        """
        Construct a file path from multiple arguments.
        """
        return os.path.join(*args)

    # Define DSSAT root directory and output folder
    dssat_path = 'C://DSSAT48/'
    output_directory = 'C://DSSAT48/Wheat/'

    # Set the working directory to the output folder
    os.chdir(output_directory)

    # Build the command to run DSSAT
    main_executable = build_path(dssat_path, 'DSCSM048.EXE')
    module = 'CSCER048'
    switch = 'B'
    control_file = build_path(dssat_path, 'Wheat/DSSBatch.v48')

    # Create and execute the command 
    command_line = ' '.join([main_executable, module, switch, control_file])
    result = subprocess.run(command_line, shell=True, check=True, capture_output=True, text=True)

    # Print DSSAT execution output
    print(result.stdout)

    # Use uplantgro from dpest.wheat.utils to extract and update data from PlantGro.OUT if needed
    uplantgro(
        plantgro_file_path='C:/DSSAT48/Wheat/PlantGro.OUT',
        treatment='164.0 KG N/HA IRRIG',
        variables=['LAID', 'CWAD', 'T#AD']
    )

This script should be ``saved in the PEST installation directory`` (e.g., ``C:\pest18``). The command to execute it (``py "C:\pest18\script_name.py"``) must match the actual filename and will be included in the ``.PST`` file.

**Generate the PEST Control File (.PST)**  

Once the script is saved, we can generate the ``PEST control file`` using the following function:

.. code-block:: python

    dpest.pst(
        cultivar_parameters = cultivar_parameters,
        dataframe_observations = [overview_observations, plantgro_observations],
        model_comand_line = r'py "C:\pest18\run_dssat.py"',  # Command to run the model
        input_output_file_pairs = [
            (cultivar_tpl_path, 'C://DSSAT48/Genotype/WHCER048.CUL'),  # Template file → Target file
            (overview_ins_path , 'C://DSSAT48/Wheat/OVERVIEW.OUT'),  # Instruction file → Target file
            (plantgro_ins_path , 'C://DSSAT48/Wheat/PlantGro.OUT')  # Instruction file → Target file
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
    inschek.exe OVERVIEW.ins C://DSSAT48/Wheat/OVERVIEW.OUT  

    # Validate the PlantGro Instruction File (.INS)
    inschek.exe PlantGro.ins C://DSSAT48/Wheat/PlantGro.OUT 

    # Validate the PEST Control File (.PST)
    pestchek.exe PEST_CONTROL.pst  

If the files are correctly formatted and no errors are found, the output will confirm this (e.g., "No errors encountered").


4. Run the Calibration  
----------------------

After successfully validating the ``PEST input files``, the final step is to run the calibration process.

Run the following command to start ``PEST`` in parameter estimation mode:

.. code-block:: console

    C:\wht_manitou_cal> PEST.exe PEST_CONTROL.pst 