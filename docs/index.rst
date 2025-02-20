What is dpest?
=============

`dpest` is a Python package designed to automate the creation of `PEST (Parameter Estimation and Uncertainty Analysis)`_ control files for calibrating `DSSAT (Decision Support System for Agrotechnology Transfer)`_ crop models. Currently, `dpest` is capable of calibrating DSSAT wheat models only. It generates template files for cultivar and ecotype parameters, instruction files for `OVERVIEW.OUT` and `PlantGro.OUT`, and the main PEST control file. A utility module is also included to extend `PlantGro.OUT` files for complete time series compatibility.

.. _PEST (Parameter Estimation and Uncertainty Analysis): https://pesthomepage.org/
.. _DSSAT (Decision Support System for Agrotechnology Transfer): https://dssat.net/

This documentation provides a complete reference for using `dpest`.

Table of Contents
=================

1.  `Installation <#installation>`_
2.  `Prerequisites <#prerequisites>`_
3.  `Basic Usage <basic_usage>`_
4.  Module Reference
    *   `dpest.wheat.ceres.cul <dpestwheatcerescul>`_
    *   `dpest.wheat.ceres.eco <dpestwheatcereseco>`_
    *   `dpest.wheat.overview <dpestwheatoverview>`_
    *   `dpest.wheat.plantgro <dpestwheatplantgro>`_
    *   `dpest.pst <dpestpst>`_
    *   `dpest.wheat.utils.uplantgro <dpestwheatutilsuplantgro>`_
5.  `Example: Calibrating DSSAT for Wheat (CERES Model) <example>`_

.. toctree::
   :maxdepth: 2

   dpest.wheat.ceres.cul
   dpest.wheat.ceres.eco
   dpest.wheat.overview
   dpest.wheat.plantgro
   dpest.pst
   dpest.wheat.utils.uplantgro
   basic_usage
   example