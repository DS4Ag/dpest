Example: Calibrating DSSAT for Wheat (CERES Model)
===================================================

This example demonstrates how to use `dpest` to create the necessary files for calibrating the CERES-Wheat model (DSSAT Version 4.8) using the `SWSW7501WH N RESPONSE` experiment.

1. Run DSSAT
------------

*   Follow these steps within the DSSAT software:

    1.  Launch DSSAT.
    2.  Click "Selector".
    3.  Expand "Crops" and select "Wheat".
    4.  Select the experiment "SWSW7501.WHX".
    5.  Click "Run".
    6.  Choose "CERES" as the crop model.
    7.  Click "OK" and wait for the simulation to finish.

.. raw:: html

    <iframe width="560" height="315" 
            src="https://www.youtube.com/embed/dzKpvJSEXZc?vq=hd1080" 
            frameborder="0" allowfullscreen>
    </iframe>

2. Create Template Files and Instruction Files
----------------------------------------------

.. code-block:: python

    import dpest

    # 1. Create CULTIVAR parameters TPL file
    cultivar_parameters, cultivar_tpl_path = dpest.wheat.ceres.cul(
        cultivar = 'MANITOU', #Cultivar name
        cul_file_path = 'C:/DSSAT48/Genotype/WHCER048.CUL' #Path to the CUL file
    )

    # 2. Create OVERVIEW observations INS file
    overview_observations, overview_ins_path = dpest.wheat.overview(
        treatment = '164.0 KG N/HA IRRIG', #Treatment Name
        overview_file_path = 'C:/DSSAT48/Wheat/OVERVIEW.OUT' #Path to the OVERVIEW.OUT file
    )
    # 3. Create PlantGro observations INS file
    plantgro_observations, plantgro_ins_path = dpest.wheat.plantgro(
        plantgro_file_path = 'C:/DSSAT48/Wheat/PlantGro.OUT', #Path to the PlantGro.OUT file
        treatment = '164.0 KG N/HA IRRIG', #Treatment Name
        variables = ['LAID', 'CWAD', 'T#AD'] #Variables to calibrate
    )
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

**Explanation:**

*   **File Paths:** Modify the file paths in the example code to match the actual locations of your DSSAT installation, experiment files, and desired output locations.
*   **Parameters and Variables:** Adjust the parameters and variables specified in the module calls to reflect the specific parameters you want to calibrate and the variables you want to use for comparison.
*   **Model Command Line:** The `model_command_line` argument in the `dpest.pst()` module specifies the command to run the DSSAT model. You will need to adapt this to your specific environment and how you run DSSAT. The example assumes you have a `run_dssat.py` script that handles the execution of DSSAT.
*   **Parameters groups:** In the `cul` module, the parameters should be passed inside the parameters groups.
*   **Variables:** In the `plantgro` module, the variables should be passed as list.

3. Run PEST
----------

After running the Python script, you will have a `.PST` file (the PEST control file) that you can use with PEST to perform model calibration. Follow the PEST documentation for instructions on running PEST with your control file.