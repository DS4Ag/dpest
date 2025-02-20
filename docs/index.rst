.. dpest documentation master file, created by
   sphinx-quickstart on Tue Feb 18 15:19:42 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

dpest documentation
===================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.

What is dpest?
==============

`dpest` is a Python package designed to automate the creation of [PEST (Parameter Estimation and Uncertainty Analysis)](https://pesthomepage.org/) control files for calibrating [DSSAT (Decision Support System for Agrotechnology Transfer)](https://dssat.net/) crop models. Currently, `dpest` is capable of calibrating DSSAT wheat models only.  It generates template files for cultivar and ecotype parameters, instruction files for `OVERVIEW.OUT` and `PlantGro.OUT`, and the main PEST control file. A utility module is also included to extend `PlantGro.OUT` files for complete time series compatibility.

This documentation provides a complete reference for using `dpest`.

Table of Contents
===============

1.  `Installation <installation>`_
2.  `Prerequisites <prerequisites>`_
3.  `Basic Usage <basic_usage>`_
4.  `Module Reference <module_reference>`_
   *   `dpest.wheat.ceres.cul <dpest.wheat.ceres.cul>`_
   *   `dpest.wheat.ceres.eco <dpest.wheat.ceres.eco>`_
   *   `dpest.wheat.overview <dpest.wheat.overview>`_
   *   `dpest.wheat.plantgro <dpest.wheat.plantgro>`_
   *   `dpest.pst <dpest.pst>`_
   *   `dpest.wheat.utils.uplantgro <dpest.wheat.utils.uplantgro>`_
5.  `Example: Calibrating DSSAT for Wheat (CERES Model) <example>`_

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :hidden:

   installation
   prerequisites
   basic_usage
   module_reference
   example
   contributing
   package_structure

Indices and tables
==================

*   :ref:`genindex`
*   :ref:`modindex`
*   :ref:`search`