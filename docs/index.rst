dpest 1.0 documentation
=======================

What is dpest?
==============

`dpest` is a Python package designed to automate the creation of `PEST (Parameter Estimation and Uncertainty Analysis)`_ control files for calibrating `DSSAT (Decision Support System for Agrotechnology Transfer)`_ crop models. Currently, `dpest` is capable of calibrating DSSAT wheat models only. It generates template files for cultivar and ecotype parameters, instruction files for `OVERVIEW.OUT` and `PlantGro.OUT`, and the main PEST control file. A utility module is also included to extend `PlantGro.OUT` files for complete time series compatibility.

.. _PEST (Parameter Estimation and Uncertainty Analysis): https://pesthomepage.org/
.. _DSSAT (Decision Support System for Agrotechnology Transfer): https://dssat.net/

This documentation provides a complete reference for using `dpest`.

.. toctree::
   :numbered:
   :maxdepth: 2
   :caption: Table of Contents:

   installation
   prerequisites
   basic_usage
   module_reference
   example

.. toctree::
   :numbered: 4
   :maxdepth: 1
   :caption: Module Reference:

   dpest.wheat.ceres.cul
   dpest.wheat.ceres.eco
   dpest.wheat.overview
   dpest.wheat.plantgro
   dpest.pst
   dpest.wheat.utils.uplantgro