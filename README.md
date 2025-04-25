# dpest: Automating PEST Control File Creation for DSSAT Crop Model Calibration

[![Wang lab logo](https://static.wixstatic.com/media/c544bf_0e3064b159ae42238c83dca23bc352e8~mv2.png/v1/crop/x_0,y_0,w_1918,h_2080/fill/w_91,h_100,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/lab_icon_3.png)](https://www.dianewanglab.com/)

[![Python version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Documentation Status](https://readthedocs.org/projects/dpest/badge/?version=latest)](https://dpest.readthedocs.io/en/latest/?badge=latest)

## What is dpest?

`dpest` is a Python package designed to automate the creation of [PEST (Parameter Estimation and Uncertainty Analysis)](https://pesthomepage.org/) control files for calibrating [DSSAT (Decision Support System for Agrotechnology Transfer)](https://dssat.net/) crop models. Currently, `dpest` is capable of calibrating DSSAT wheat models only.  It generates template files for cultivar and ecotype parameters, instruction files for `OVERVIEW.OUT` and `PlantGro.OUT`, and the main PEST control file. A utility module is also included to extend `PlantGro.OUT` files for complete time series compatibility. 

### Documentation

For detailed usage instructions and module references, see the full documentation on: [dpest.readthedocs.io/en/latest](https://dpest.readthedocs.io/en/latest/).

## Key Features

*   Automated generation of `PEST control files (.PST)`.
*   Compatibility with DSSAT wheat models.
*   Creation of `PEST template files (.TPL)` for cultivar and ecotype parameters.
*   Generation of `PEST instruction files (.INS)` for key DSSAT output files.
*   Utility module to extend `PlantGro.OUT` files for complete time series.

## Installation

`dpest` can be installed via pip from [PyPI](https://pypi.org/project/dpest/).

```
pip install dpest
```

## Prerequisites

1.  **DSSAT Software:** [DSSAT (version 4.8)](https://dssat.net/) must be installed on your system.
2.  **DSSAT Experiment Data:** You'll need a DSSAT experiment to work with. The example below uses the `SWSW7501WH N RESPONSE` wheat experiment.
3.  **PEST Software:** You’ll need to have [PEST (version 18)](https://pesthomepage.org/) installed.

## Basic Usage


The following steps provide a brief overview of how to use `dpest`. For a **detailed, step-by-step example**, please refer to the official documentation:  
[Complete Example on Read the Docs](https://dpest.readthedocs.io/en/latest/example.html)  

1.  **Locate DSSAT Genotype Files:** The cultivar (`.CUL`) and ecotype (`.ECO`) files are typically included with the DSSAT installation. These are usually found in the `C:\DSSAT48\Genotype\` directory.
2.  **Run a DSSAT Simulation:** Execute a DSSAT simulation for your chosen wheat experiment using the CERES model. This will generate the necessary output files (`OVERVIEW.OUT` and `PlantGro.OUT`), typically found in the `C:\DSSAT48\Wheat\` directory.

        2.1. Launch DSSAT.
        2.2. Click "Selector".
        2.3. Expand "Crops" and select "Wheat".
        2.4. In the "Data" panel select the "SWSW7501.WHX" experiment.
        2.5. Click "Run" button in the toolbar.
        2.6. In the "Simulation" popup window, choose "CERES" as the crop model.
        2.7. Click "Run Model" and wait for the simulation to finish.


3.  **Import the `dpest` Package:**

    *   To import the entire `dpest` package:

    ```
    import dpest
    ```

    *   To import specific modules:

    ```
    from dpest.wheat.ceres import cul, eco
    from dpest.wheat import overview, plantgro
    from dpest import pst
    from dpest.wheat.utils import uplantgro

    # Now you can use the functions directly:
    cul(...)
    eco(...)
    overview(...)
    plantgro(...)
    pst(...)
    uplantgro(...)
    ```

4.  **Use the Modules**

    *   **`cul()`**: This module creates `PEST template files (.TPL)` for CERES-Wheat cultivar parameters. Use it to generate template files for cultivar calibration.
    *   **`eco()`**: This module creates `PEST template files (.TPL)` for CERES-Wheat ecotype parameters. Use it to generate template files for ecotype calibration.
    *   **`overview()`**: This module creates `PEST instruction files (.INS)` for reading observed (*measured*) values of key end-of-season crop performance metrics and key phenological observations from the `OVERVIEW.OUT` file. The instruction file tells PEST how to extract model-generated observations from the `OVERVIEW.OUT` file, compare them with the observations from the DSSAT `A file`, and adjust model parameters accordingly.
    *   **`plantgro()`**: This module creates `PEST instruction files (.INS)` for reading observed (*measured*) values of plant growth dynamics from the `PlantGro.OUT` file. The instruction file tells PEST how to extract time-series data from the `PlantGro.OUT file`, compare that data with the time-series data provided in the DSSAT `T file`, and adjust model parameters accordingly.
    *   **`pst()`**: enerates the main `PEST control file (.PST)` to guide the entire calibration process. It integrates the  `PEST template files (.TPL)` and `PEST instruction files (.INS)`, defines calibration parameters, observation groups, weights, PEST control variables and model run command.
    *   **`uplantgro()`**: modifies the DSSAT output file (`PlantGro.OUT`) to prevent PEST errors when simulated crop maturity occurs before the final measured observation. This ensures PEST can compare all available time-series data, even when the model predicts maturity earlier than observed in the field.

5.  **Create Template Files and Instruction Files:** Use the `dpest` modules to generate `PEST template files (.TPL)` for cultivar and ecotype parameters, and `PEST instruction files (.INS)` for the `OVERVIEW.OUT` and `PlantGro.OUT` files.

```
import dpest

# 1. Create CULTIVAR parameters TPL file
cultivar_parameters, cultivar_tpl_path = dpest.wheat.ceres.cul(
    P = 'P1D, P5', # How the user should enter the parameters
    G = 'G1, G2, G3', 
    PHINT = 'PHINT',
    cultivar = 'MANITOU',
    cul_file_path = 'C:/DSSAT48/Genotype/WHCER048.CUL'
)

# 2. Create OVERVIEW observations INS file
overview_observations,  overview_ins_path = dpest.wheat.overview(
    treatment = '164.0 KG N/HA IRRIG', #Treatment Name
    overview_file_path = 'C:/DSSAT48/Wheat/OVERVIEW.OUT' #Path to the OVERVIEW.OUT file
)
# 3. Create PlantGro observations INS file
plantgro_observations, plantgro_ins_path = dpest.wheat.plantgro(
    treatment = '164.0 KG N/HA IRRIG', #Treatment Name
    variables = ['LAID', 'CWAD', 'T#AD'] #Variables to calibrate
    plantgro_file_path = 'C:/DSSAT48/Wheat/PlantGro.OUT', #Path to the PlantGro.OUT file
)

```
6.  **Create the PEST Control File:** Use the `dpest.pst()` module to generate the main `PEST control file (.PST)`.

```

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
```

7.  **Run PEST:** Calibrate the model using PEST.

---
## Utilities for Editing PEST Control Files

In addition to automating the creation of PEST control and template files for DSSAT CERES-Wheat model calibration, `dpest` includes a growing set of utility functions under `dpest.utils` for directly modifying existing `.pst` (PEST control) files.


#### Why use `dpest.utils`?

Unlike libraries such as [`pyEMU`](https://pyemu.readthedocs.io/en/develop/pyemu.pst.html), which parse `.pst` files into Python objects and rewrite the entire file when saving any change, `dpest.utils` performs lightweight, line-by-line edits to preserve the original structure and untouched content.

These utilities:

- Edit existing `.pst` files in place, without reconstructing or redefining unrelated fields.
-  Are model-agnostic: they work with any `.pst` file, not just DSSAT-related ones.
- Only modify model-independent control parameters (e.g., optimization settings), leaving parameter and data blocks untouched.

This makes them ideal for **quickly tuning optimization settings** or **cleaning up `.pst` files** generated by `dpest` or other tools.

#### Example Usage

```python
# Load the dpest.utils
from dpest.utils import noptmax, rmv_splitcols

# Path to the .pst file
pst_file_path = './ENTRY1/PEST_CONTROL.pst'

# Increase the number of optimization iterations (NOPTMAX) in a .pst file
noptmax(pst_file_path, new_value=50)

# Remove SPLITTHRESH/SPLITRELDIFF/SPLITACTION columns from a .pst file parameter groups section
rmv_splitcols(“PEST_CONTROL.pst”)

```

**Full List of Utility Functions:**  
For the complete reference of available utility functions and their descriptions, see the [dpest ReadTheDocs Utils page](https://dpest.readthedocs.io/en/latest/utils.html).

### Contributing

Contributions to `dpest` are welcome! Please submit bug reports, feature requests, and pull requests through the project's GitHub repository or by email to: Luis Vargas Rojas - [lvargasr@purdue.edu](lvargasr@purdue.edu).

Purdue University, Wang Lab [dianewanglab.com](https://www.dianewanglab.com/)

### License

`dpest` is released under the [GNU General Public License v3.0 only](https://www.gnu.org/licenses/gpl-3.0.html).