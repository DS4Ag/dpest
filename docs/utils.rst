.. currentmodule:: dpest.utils

Control File Update Utilities
=============================

This subpackage contains utility functions used to modify specific sections
and variables of PEST control files.

Control Data
------------

General control settings
~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   dpest.utils.rstfle
   dpest.utils.pestmode

Lambda and objective-function control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   dpest.utils.rlambda1
   dpest.utils.rlamfac
   dpest.utils.phiratsuf
   dpest.utils.phiredlam
   dpest.utils.numlam
   dpest.utils.jacupdate

Parameter change limits
~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   dpest.utils.relparmax
   dpest.utils.facparmax
   dpest.utils.facorig

Optimization switching
~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   dpest.utils.phiredswh
   dpest.utils.noptswitch

Optimization termination criteria
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   dpest.utils.noptmax
   dpest.utils.phiredstp
   dpest.utils.nphistp
   dpest.utils.nphinored
   dpest.utils.relparstp
   dpest.utils.nrelpar


Parameter Groups
----------------

Utilities associated with the ``* parameter groups`` section of the PEST
control file.

.. toctree::
   :maxdepth: 1

   dpest.utils.parg_inctyp
   dpest.utils.parg_derinc


Singular Value Decomposition
----------------------------

Utilities associated with the ``* singular value decomposition`` section.

.. toctree::
   :maxdepth: 1

   dpest.utils.svd
   dpest.utils.rmv_svd


LSQR
----

Utilities associated with the ``* lsqr`` section.

.. toctree::
   :maxdepth: 1

   dpest.utils.lsqr
   dpest.utils.rmv_lsqr


Regularisation
--------------

Utilities associated with the ``* regularisation`` section.

.. toctree::
   :maxdepth: 1

   dpest.utils.regularisation


Model Input/Output
------------------

Utilities used to modify model input/output-related entries in the PEST
control file.

.. toctree::
   :maxdepth: 1

   dpest.utils.rmv_splitcols


Jacobian
--------

Utilities related to Jacobian handling.

.. toctree::
   :maxdepth: 1

   dpest.utils.jacupdate