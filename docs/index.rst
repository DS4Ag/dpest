dpest
=======================

What is dpest?
=============

`dpest` is a Python package designed to automate the creation of `PEST (Parameter Estimation and Uncertainty Analysis)`_ control files for calibrating `DSSAT (Decision Support System for Agrotechnology Transfer)`_ crop models. Currently, `dpest` is capable of calibrating DSSAT wheat models only. It generates template files for cultivar and ecotype parameters, instruction files for `OVERVIEW.OUT` and `PlantGro.OUT`, and the main PEST control file. A utility module is also included to extend `PlantGro.OUT` files for complete time series compatibility.

.. _PEST (Parameter Estimation and Uncertainty Analysis): https://pesthomepage.org/
.. _DSSAT (Decision Support System for Agrotechnology Transfer): https://dssat.net/

This documentation provides a complete reference for using `dpest`.


Installation
=================
`dpest` can be installed via pip from `PyPI <https://pypi.org/project/dpest/>`_.

.. code-block:: bash

   pip install dpest


Table of Contents
=================

.. toctree::
   :maxdepth: 2
   :hidden:

   basic_usage
   dpest.wheat.ceres.cul
   dpest.wheat.ceres.eco
   dpest.wheat.overview
   dpest.wheat.plantgro
   dpest.pst
   dpest.wheat.utils.uplantgro
   example
   example_multiple_trts

*  `Basic Usage <basic_usage.html>`_
*  Module Reference
    *  `dpest.wheat.ceres.cul <dpest.wheat.ceres.cul.html>`_
    *  `dpest.wheat.ceres.eco <dpest.wheat.ceres.eco.html>`_
    *  `dpest.wheat.overview <dpest.wheat.overview.html>`_
    *  `dpest.wheat.plantgro <dpest.wheat.plantgro.html>`_
    *  `dpest.pst <dpest.pst.html>`_
    *  `dpest.wheat.utils.uplantgro <dpest.wheat.utils.uplantgro.html>`_
*  `Example: Calibrating DSSAT for Wheat (CERES Model) <example.html>`_
*  `Example: Calibrating a Cultivar Using Multiple Treatments <example_multiple_trts.html>`_