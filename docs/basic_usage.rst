Basic Usage
===========

The following steps outline the typical workflow for using `dpest`:

1. **Locate DSSAT Genotype Files:** The cultivar (`.CUL`) and ecotype (`.ECO`) files are typically included with the DSSAT installation. These are usually found in the "C:\DSSAT48\Genotype\" directory.
2. **Run a DSSAT Simulation:** Execute a DSSAT simulation for your chosen wheat experiment using either the CERES, NWHEAT, or CROPSIM model. This will generate the necessary output files (`OVERVIEW.OUT` and `PlantGro.OUT`), typically found in the "C:\DSSAT48\Wheat\" directory.
3. **Import the `dpest` Package:**

    There are two ways to import the `dpest` package:

        A. **Using Fully Qualified Names:**

           Import the entire package:

           .. code-block:: python

              import dpest

           Now you can use the modules with their fully qualified names:

           .. code-block:: python

              dpest.wheat.ceres.cul(...)
              dpest.wheat.ceres.eco(...)
              dpest.wheat.overview(...)
              dpest.wheat.plantgro(...)
              dpest.pst(...)
              dpest.wheat.utils.uplantgro(...)

        B. **Using Locally Bound Names:**

           Import specific modules into your current namespace:

           .. code-block:: python

              from dpest.wheat.ceres import cul, eco
              from dpest.wheat import overview, plantgro
              from dpest import pst
              from dpest.wheat.utils import uplantgro

           Now you can use the functions directly by their locally bound names:

           .. code-block:: python

              cul(...)
              eco(...)
              overview(...)
              plantgro(...)
              pst(...)
              uplantgro(...)

4. **Use the Modules**

    *   **cul()**: This module creates `PEST template files (.TPL)` for CERES-Wheat cultivar parameters. Use it to generate template files for cultivar calibration.
    *   **eco()**: This module creates `PEST template files (.TPL)` for CERES-Wheat ecotype parameters. Use it to generate template files for ecotype calibration.
    *   **overview()**: This module creates `PEST instruction files (.INS)` for reading observed (*measured*) values of key end-of-season crop performance metrics and key phenological observations from the `OVERVIEW.OUT` file. The instruction file tells PEST how to extract model-generated observations from the `OVERVIEW.OUT` file, compare them with the observations from the DSSAT `A file`, and adjust model parameters accordingly.
    *   **plantgro()**: This module creates `PEST instruction files (.INS)` for reading observed (*measured*) values of plant growth dynamics from the `PlantGro.OUT` file. The instruction file tells PEST how to extract time-series data from the `PlantGro.OUT file`, compare that data with the time-series data provided in the DSSAT `T file`, and adjust model parameters accordingly.
    *   **pst()**: This module creates the main `PEST control file (.PST)`.
    *   **uplantgro()**: This module extends `PlantGro.OUT` files by adding rows when the plant maturity simulation date occurs before a measured observation date.

5. **Create Template Files and Instruction Files:** Use the `dpest` modules to generate `PEST template files (.TPL)` for cultivar and ecotype parameters, and `PEST instruction files (.INS)` for the `OVERVIEW.OUT` and `PlantGro.OUT` files.
6. **Create the PEST Control File:** Use the `dpest.pst()` module to generate the main `PEST control file (.PST)`.
7. **Run PEST:** Calibrate the model using PEST.