Example: Calibrating a Cultivar Using Multiple Treatments
==============================================================

This example demonstrates how to use `dpest` to create calibration files for the CERES-Wheat model using **three different treatments** from the ``SWSW7501WH N RESPONSE`` experiment. The objective is to calibrate the `MANITOU` cultivar using observations from the following treatments:

- `82.0 KG N/HA IRRIG`
- `123.0 KG N/HA IRRIG`
- `164.0 KG N/HA IRRIG`


1. Run DSSAT
------------

Follow these steps within the DSSAT software to generate the necessary output files (`OVERVIEW.OUT` and `PlantGro.OUT`) for all treatments:

1. Launch DSSAT.
2. Click "Selector."
3. Expand "Crops" and select "Wheat."
4. In the "Data" panel, select the `SWSW7501.WHX` experiment.
5. Click the "Run" button in the toolbar.
6. In the "Simulation" popup window, choose "CERES" as the crop model.
7. Click "Run Model" and wait for the simulation to complete.

.. raw:: html

    <iframe 
            width="700" 
            height="400"
            src="https://www.youtube.com/embed/dzKpvJSEXZc?vq=hd1080" 
            frameborder="0" allowfullscreen>
    </iframe>  


2. Create PEST Input Files for Multi-Treatment Calibration
----------------------------------------------------------

This section explains how to use `dpest` to create input files required for PEST calibration based on observations from multiple treatments.

**2.1 Import dpest Functions**

Import the required modules from the `dpest` package:

.. code-block:: python

    from dpest.wheat.ceres.cul import cul
    from dpest.wheat.overview import overview
    from dpest.wheat.plantgro import plantgro
    from dpest.pst import pst

After running this code, you will have access to all necessary functions for creating template files, instruction files, and the PEST control file.



**2.2 Create Cultivar Template File**

The first step is to create a template file (`.TPL`) for the `MANITOU` cultivar, which is planted across all treatments in this experiment using the `cul()` function:

.. code-block:: python

    cultivar_parameters, cultivar_tpl_path = cul(
        P='P1V, P1D, P5',
        G='G1, G2, G3',
        PHINT='PHINT',
        cultivar='MANITOU',
        cul_file_path='C:/DSSAT48/Genotype/WHCER048.CUL'
    )

After running this function:
- The `cultivar_parameters` variable stores a dictionary containing parameter groups and sections needed to generate the `.PST` file.
- The `cultivar_tpl_path` variable stores the file path of the generated `.TPL` file, which will be used in creating the `.PST` file.

Note that the cultivar template file named `WHCER048_CUL.TPL` will be created in the current working directory.



**2.3 Create Instruction Files**

Now, we need to create instruction files for each treatment and the instruction files (`.INS`) for both `OVERVIEW.OUT` and `PlantGro.OUT`.Since we're using multiple treatments, we'll add a `suffix` to differentiate the files. 

**OVERVIEW.OUT Instruction Files:**

Use the `overview()` function to generate instruction files for each treatment to compare the model simulations from the ``C:/DSSAT48/Wheat/OVERVIEW.OUT`` file with the measured data from the ``A File``.

.. code-block:: python

    overview_observations_trt1, overview_ins_path_trt1 = overview(
        treatment='82.0 KG N/HA IRRIG',
        overview_file_path='C:/DSSAT48/Wheat/OVERVIEW.OUT',
        suffix='TRT1'
    )

    overview_observations_trt2, overview_ins_path_trt2 = overview(
        treatment='123.0 KG N/HA IRRIG',
        overview_file_path='C:/DSSAT48/Wheat/OVERVIEW.OUT',
        suffix='TRT2'
    )

    overview_observations_trt3, overview_ins_path_trt3 = overview(
        treatment='164.0 KG N/HA IRRIG',
        overview_file_path='C:/DSSAT48/Wheat/OVERVIEW.OUT',
        suffix='TRT3'
    )

After running these functions:
- The `overview_observations_trtX` variables store DataFrames with observations needed for creating the `.PST` file.
- The `overview_ins_path_trtX` variables store paths to instruction files created by the `overview()` function.
- The instruction files will be used in matching original DSSAT output files (`OVERVIEW.OUT`) with observations during calibration.

**PlantGro.OUT Instruction Files:**

Use the `plantgro()` function to generate instruction files for each treatment to compare the time-series model simulations from the ``'C:/DSSAT48/Wheat/PlantGro.OUT'`` file with the time-series measured data from the ``T File``.

.. code-block:: python

    plantgro_observations_trt1, plantgro_ins_path_trt1 = plantgro(
        treatment='82.0 KG N/HA IRRIG',
        plantgro_file_path='C:/DSSAT48/Wheat/PlantGro.OUT',
        variables=['LAID', 'CWAD', 'T#AD'],
        suffix='TRT1'
    )

    plantgro_observations_trt2, plantgro_ins_path_trt2 = plantgro(
        treatment='123.0 KG N/HA IRRIG',
        plantgro_file_path='C:/DSSAT48/Wheat/PlantGro.OUT',
        variables=['LAID', 'CWAD', 'T#AD'],
        suffix='TRT2'
    )

    plantgro_observations_trt3, plantgro_ins_path_trt3 = plantgro(
        treatment='164.0 KG N/HA IRRIG',
        plantgro_file_path='C:/DSSAT48/Wheat/PlantGro.OUT',
        variables=['LAID', 'CWAD', 'T#AD'],
        suffix='TRT3'
    )

After running these functions:
- The `plantgro_observations_trtX` variables store DataFrames with time-series observations needed for creating the `.PST` file.
- The `plantgro_ins_path_trtX` variables store paths to instruction files created by the `plantgro()` function.
- These instruction files will be used in matching original DSSAT output files (`PlantGro.OUT`) with time-series observations during calibration.

Note that both instruction files (`OVERVIEW.INS` and `PlantGro.INS`) will be created in the current working directory.


**2.4 Create the PEST Control File**

After creating the ``template file`` and ``instruction files`` for calibrating the ``MANITOU`` wheat cultivar across multiple treatments, the next step is to generate the ``PEST control file (.PST)``. This file integrates all necessary components and guides the calibration process.

The `.PST` file is created using the variables obtained in **2.2** and **2.3**. Additionally, you need to specify the `command-line instruction` to execute the DSSAT model for all treatments. For more information on running DSSAT from the command line, visit the the `DSSAT web documentation <https://dssat.net/tools/tools-for-power-users/>`_.

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

    # Use uplantgro from dpest.wheat.utils to extract and update data from PlantGro.OUT for each treatment if needed
    
    uplantgro(
        plantgro_file_path='C:/DSSAT48/Wheat/PlantGro.OUT',
        treatment='82.0 KG N/HA IRRIG',
        variables=['LAID', 'CWAD', 'T#AD']
    )

    uplantgro(
        plantgro_file_path='C:/DSSAT48/Wheat/PlantGro.OUT',
        treatment='123.0 KG N/HA IRRIG',
        variables=['LAID', 'CWAD', 'T#AD']
    )

    uplantgro(
        plantgro_file_path='C:/DSSAT48/Wheat/PlantGro.OUT',
        treatment='164.0 KG N/HA IRRIG',
        variables=['LAID', 'CWAD', 'T#AD']
    )


This script should be ``saved in the PEST installation directory`` (e.g., ``C:\pest18``). The command to execute it (e.g., ``py "C:\pest18\script_name.py"``) must match the actual filename and will be included in the ``.PST`` file.

**Generate the PEST Control File (.PST)**

Once you have saved your script for running DSSAT, you can generate the ``PEST control file`` using the following function:

.. code-block:: python

    pst(
        cultivar_parameters=cultivar_parameters,
        dataframe_observations=[
            overview_observations_trt1, overview_observations_trt2, overview_observations_trt3,
            plantgro_observations_trt1, plantgro_observations_trt2, plantgro_observations_trt3
        ],
        model_comand_line=r'py "C:\pest18\run_dssat.py"',  # Command to run DSSAT
        input_output_file_pairs=[
            # Template file → Cultivar parameter file
            (cultivar_tpl_path, 'C://DSSAT48/Genotype/WHCER048.CUL'),
            
            # Instruction files for OVERVIEW.OUT (3 treatments)
            (overview_ins_path_trt1, 'C://DSSAT48/Wheat/OVERVIEW.OUT'),
            (overview_ins_path_trt2, 'C://DSSAT48/Wheat/OVERVIEW.OUT'),
            (overview_ins_path_trt3, 'C://DSSAT48/Wheat/OVERVIEW.OUT'),

            # Instruction files for PlantGro.OUT (3 treatments)
            (plantgro_ins_path_trt1, 'C:/DSSAT48/Wheat/PlantGro.OUT'),
            (plantgro_ins_path_trt2, 'C:/DSSAT48/Wheat/PlantGro.OUT'),
            (plantgro_ins_path_trt3, 'C:/DSSAT48/Wheat/PlantGro.OUT')
        ]
    )

After running this function:
- A `.PST` control file is created that combines all observation data and links them to their corresponding template and instruction files.
- This `.PST` file is ready for use in PEST calibration.


**Key Notes for Multi-Treatment Calibration:**
- The `dataframe_observations` argument includes observations from all treatments (`TRT1`, `TRT2`, `TRT3`) for both `OVERVIEW.OUT` and `PlantGro.OUT`.
- The `input_output_file_pairs` argument specifies how each instruction file corresponds to its respective DSSAT output file.


3. Validate Input Files
-----------------------

After generating the ``PEST input files``, it is important to validate that they were created correctly. To ensure that all input files are correctly formatted before running PEST, use TEMPCHEK, INSCHEK and PESTCHEK utilities provided by PEST:

**3.1. Open the Command Prompt**

To begin the validation process, open the Command Prompt (or terminal, if using a different operating system)

**3.2. Navigate to the Working Directory**

Once the Command Prompt (or terminal) is open, navigate to the directory where the ``PEST input files`` were created. Use the following command to change to the working directory (replace with your actual path):

.. code-block::

    cd path_to_your_directory

**3.3. Validate PEST Files**

Run the following commands to validate the different PEST input files. Each validation command checks a specific file. The instructions are provided as comments next to each command:

.. code-block:: bash

    # Validate the Template File (.TPL)
    tempchek.exe WHCER048_CUL.TPL

    # Validate the Overview Instruction FileS (.INS) 
    inschek.exe OVERVIEW_TRT1.ins C://DSSAT48/Wheat/OVERVIEW.OUT
    inschek.exe OVERVIEW_TRT2.ins C://DSSAT48/Wheat/OVERVIEW.OUT
    inschek.exe OVERVIEW_TRT3.ins C://DSSAT48/Wheat/OVERVIEW.OUT

    # Validate the PlantGro Instruction File (.INS)
    inschek.exe PlantGro_TRT1.ins C://DSSAT48/Wheat/PlantGro.OUT
    inschek.exe PlantGro_TRT2.ins C://DSSAT48/Wheat/PlantGro.OUT
    inschek.exe PlantGro_TRT3.ins C://DSSAT48/Wheat/PlantGro.OUT

    # Validate PEST Control File
    pestchek.exe PEST_CONTROL.pst

If the files are correctly formatted and no errors are found, the output will confirm this (e.g., "No errors encountered").



4. Run the Calibration  
----------------------

After successfully validating the ``PEST input files``, the final step is to run the calibration process.

Run the following command to start ``PEST`` in parameter estimation mode:

.. code-block:: console

    C:\wht_manitou_cal> PEST.exe PEST_CONTROL.pst 