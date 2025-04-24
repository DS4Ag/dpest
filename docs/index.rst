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
   :maxdepth: 1
   :caption: Basic usage

   self
   Basic_usage

.. toctree::
   :maxdepth: 2
   :caption: PEST control file

   dpest.pst
   utils

.. toctree::
   :maxdepth: 2
   :caption: Wheat (PEST input files)

   dpest.wheat.ceres.cul
   dpest.wheat.ceres.eco
   dpest.wheat.overview
   dpest.wheat.plantgro
   dpest.wheat.utils.uplantgro

.. toctree::
   :maxdepth: 2
   :caption: Examples

   example
   example_multiple_trts