Example: Calibrating DSSAT for Wheat (CERES Model)
===================================================

This example demonstrates how to use `dpest` to create the necessary files for calibrating the CERES-Wheat model (DSSAT Version 4.8) using the `SWSW7501WH N RESPONSE` experiment.

1. Run DSSAT
------------

*   Follow these steps within the DSSAT software:

    1.  Launch DSSAT.
    2.  Click "Selector".
    3.  Expand "Crops" and select "Wheat".
    4.  In the "Data" panel select the "SWSW7501.WHX" experiment.
    5.  Click "Run" botton in the toolbar.
    6.  In the "Simulation" popup window, choose "CERES" as the crop model.
    7.  Click "Run Model" and wait for the simulation to finish.

.. raw:: html

    <iframe width="560" height="315" 
            src="https://www.youtube.com/embed/dzKpvJSEXZc?vq=hd1080" 
            frameborder="0" allowfullscreen>
    </iframe>

2. Using `dpest` create the PEST input files to perform the calibration
----------------------------------------------
For this example, we are going to calibrate the `MANITOU` wheat cultivar (Cultivar ID: `IB1500`) using the field-collected data from the `164.0 KG N/HA IRRIG` treatment of the `SWSW7501.WHX` experiment. The experiment information is found in the `C:\DSSAT48\Wheat\SWSW7501.WHX` file.  

    **2.1. Import the `dpest` Package**

    .. code-block:: python

                  import dpest

    
    **2.2. Create the Cultivar Template File**  

    The first step is to create the cultivar Template File (`.TPL`) for the `MANITOU` cultivar, which is the cultivar planted in the `164.0 KG N/HA IRRIG` treatment of the `SWSW7501.WHX` experiment. To achieve this, we use the `dpest.wheat.ceres.cul()` function, as shown below:  

    .. code-block:: python  

        import dpest  
  
        cultivar_parameters, cultivar_tpl_path = dpest.wheat.ceres.cul(  
            cultivar='MANITOU',  # Cultivar name  
            cul_file_path='C:/DSSAT48/Genotype/WHCER048.CUL'  # Path to the DSSAT wheat CUL file  
        )  

    After running this function:  

    - The `cultivar_parameters` variable stores a dictionary containing the parameter groups and sections needed to generate the `.PST` file.  
    - The `cultivar_tpl_path` variable stores the file path of the generated `.TPL` file, which will be used in creating the `.PST` file.

    Note that the cultivar template file named `WHCER048_CUL.TPL` will be created in the current working directory. 

    **2.3. Create Instructions Files**

    For this experiment, key end-of-season crop performance metrics and phenological observations were collected and recorded in the `C:\DSSAT48\Wheat\SWSW7501.WHA` file (referred to as the `A File`). Additionally, time-series data were collected and recorded in the `C:\DSSAT48\Wheat\SWSW7501.WHT` file (referred to as the `T File`). To create the PEST instruction files, we will use the `overview()` and `plantgro()` modules. The `overview()` module will create the instruction file to compare the model simulations from the `'C:/DSSAT48/Wheat/OVERVIEW.OUT'` file with the measured data from the `A File`, while the `plantgro()` module will create the instruction file to compare the time-series model simulations from the `'C:/DSSAT48/Wheat/PlantGro.OUT'` file with the time-series measured data from the `T File`.

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

    - The `overview_observations` variable stores the DataFrame with the observations needed for the `.PST` file's observations and observation group sections.
    - The `overview_ins_path` variable stores the path to the instruction file created by the `overview()` module, which will be used in the `input_output_file_pairs` argument of the `pst` module to match the original `OVERVIEW.OUT` file to the instruction file.
    - The `plantgro_observations` variable stores the DataFrame with the time-series observations needed for the `.PST` file's observations and observation group sections.
    - The `plantgro_ins_path` variable stores the path to the instruction file created by the `plantgro()` module, which will be used in the `input_output_file_pairs` argument of the `pst` module to match the original `PlantGro.OUT` file to the instruction file.

    Note that the `OVERVIEW.INS` and `PlantGro.INS` instruction files will be created in the current working directory.

    **2.4. Create the PEST Control File**

    After creating the **template file** and **instruction files** for calibrating the `MANITOU` wheat cultivar, the next step is to generate the **PEST control file (`.PST`)**. This file integrates all necessary components and guides the **calibration process**.

    The `.PST` file is created using the **variables** obtained in **2.2** and **2.3**. Additionally, we need to specify the **command-line instruction** to execute the DSSAT model.  

    The following Python script provides an example of how to run the **DSSAT CERES-Wheat model** using Python:

    .. code-block:: python

        import os
        import subprocess
        from datetime import datetime
        import pandas as pd
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

    This script should be **saved in the PEST directory** as **``run_dssat.py``**. The command to execute it will be included in the `.PST` file.

    **Generate the PEST Control File (`.PST`)**  

    Once the script is saved, we can generate the **PEST control file** using the following function:

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

    - The `.PST` file will be created in the working directory.
    - The **template file** and **instruction files** will be linked to their corresponding model input and output files.
    - The **command-line instruction** to run DSSAT is stored in the `.PST` file.
    
    The `.PST` file serves as the **main configuration file** for running PEST and calibrating the DSSAT model.


3. Validate the Created PEST Input Files  
----------------------------------------

After generating the **PEST input files**, it is important to validate that they were created correctly. This is done using PEST’s built-in validation tools.

### 3.1. Navigate to the Working Directory  

Open the **Command Prompt** and move to the directory where the **PEST input files** were created:

.. code-block:: console

    C:\Users\luizv> cd \wht_manitou_cal

### 3.2. Validate the PEST Control File (`.PST`)  

Run the following command to check the **PEST control file**:

.. code-block:: console

    C:\wht_manitou_cal> pestchek.exe PEST_CONTROL.pst

If the file is correctly formatted, the output will indicate **"No errors encountered."**  

### 3.3. Validate the Instruction Files (`.INS`)  

Next, verify that the **instruction files (`.INS`)** were correctly generated.

Check the **`OVERVIEW.INS`** file:

.. code-block:: console

    C:\wht_manitou_cal> inschek.exe OVERVIEW.ins C://DSSAT48/Wheat/OVERVIEW.OUT  

Then check the **`PlantGro.INS`** file:

.. code-block:: console

    C:\wht_manitou_cal> inschek.exe PlantGro.ins C://DSSAT48/Wheat/PlantGro.OUT  

If the instruction files are correct, the validation output will confirm that **no errors were found** and that the expected observations were identified.

### 3.4. Perform a Final Check of the PEST Control File  

Run `pestchek.exe` again to ensure that no issues were introduced after validating the instruction files:

.. code-block:: console

    C:\wht_manitou_cal> pestchek.exe PEST_CONTROL.pst

A properly formatted file will again display **"No errors encountered."**

### 3.5. Validate the Template File (`.TPL`)  

Finally, check the **template file (`.TPL`)**, which defines the parameters for calibration:

.. code-block:: console

    C:\wht_manitou_cal> tempchek.exe WHCER048_CUL.TPL

If the template file was created correctly, the validation output will confirm that all parameters were successfully identified.

---

4. Run the Calibration  
----------------------

After successfully validating the **PEST input files**, the final step is to run the calibration process.

### 4.1. Execute the PEST Calibration  

Run the following command to start **PEST** in parameter estimation mode:

.. code-block:: console

    C:\wht_manitou_cal> PEST.exe PEST_CONTROL.pst

