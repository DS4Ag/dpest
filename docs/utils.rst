.. currentmodule:: dpest.utils

Control File Update Utilities
=============================

The ``dpest.utils`` subpackage provides functions for modifying variables
and sections of an existing PEST control (PST) file. Utilities are organized
below according to the PEST control-file section in which the corresponding
variables occur.


PEST Control File Section: Control Data
---------------------------------------

The ``* control data`` section defines the main settings that control PEST's
operation, optimization process, parameter changes, and termination criteria.


General control settings
~~~~~~~~~~~~~~~~~~~~~~~~

.. toctree::
   :maxdepth: 1

   RSTFLE — Restart-file behavior <dpest.utils.rstfle>
   PESTMODE — PEST mode of operation <dpest.utils.pestmode>


Lambda and objective-function control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These variables control the Marquardt lambda search and the objective-function
criteria used during optimization.

.. toctree::
   :maxdepth: 1

   RLAMBDA1 — Initial Marquardt lambda <dpest.utils.rlambda1>
   RLAMFAC — Marquardt lambda adjustment <dpest.utils.rlamfac>
   PHIRATSUF — Objective-function criterion for ending the current iteration <dpest.utils.phiratsuf>
   PHIREDLAM — Termination criterion for the Marquardt lambda search <dpest.utils.phiredlam>
   NUMLAM — Maximum number of Marquardt lambdas to test <dpest.utils.numlam>
   JACUPDATE — Broyden Jacobian update procedure <dpest.utils.jacupdate>


Parameter change limits
~~~~~~~~~~~~~~~~~~~~~~~

These variables constrain the magnitude of parameter changes during
optimization.

.. toctree::
   :maxdepth: 1

   RELPARMAX — Relative parameter change limit <dpest.utils.relparmax>
   FACPARMAX — Factor parameter change limit <dpest.utils.facparmax>
   FACORIG — Minimum fraction of the original parameter value <dpest.utils.facorig>


Optimization switching
~~~~~~~~~~~~~~~~~~~~~~

These variables control when PEST changes aspects of the derivative
calculation during optimization.

.. toctree::
   :maxdepth: 1

   PHIREDSWH — Objective-function change for introducing central derivatives <dpest.utils.phiredswh>
   NOPTSWITCH — Earliest iteration for switching to central derivatives <dpest.utils.noptswitch>


Optimization termination criteria
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These variables determine when the PEST optimization process terminates.

.. toctree::
   :maxdepth: 1

   NOPTMAX — Number of optimization iterations <dpest.utils.noptmax>
   PHIREDSTP — Objective-function reduction threshold <dpest.utils.phiredstp>
   NPHISTP — Number of iterations over which PHIREDSTP applies <dpest.utils.nphistp>
   NPHINORED — Number of iterations without objective-function reduction <dpest.utils.nphinored>
   RELPARSTP — Relative parameter change threshold <dpest.utils.relparstp>
   NRELPAR — Number of iterations over which RELPARSTP applies <dpest.utils.nrelpar>


PEST Control File Section: Parameter Groups
-------------------------------------------

The ``* parameter groups`` section defines how parameter derivatives are
calculated for each parameter group.

.. toctree::
   :maxdepth: 1

   INCTYP — Method used to calculate parameter increments <dpest.utils.parg_inctyp>
   DERINC — Parameter increment used for derivative calculation <dpest.utils.parg_derinc>
   Split-slope settings — Remove split-slope derivative settings <dpest.utils.rmv_splitcols>


PEST Control File Section: Singular Value Decomposition
-------------------------------------------------------

The ``* singular value decomposition`` section controls truncated singular
value decomposition (SVD) for solution of the inverse problem.

.. toctree::
   :maxdepth: 1

   SVD — Configure singular value decomposition <dpest.utils.svd>
   Remove SVD — Remove singular value decomposition settings <dpest.utils.rmv_svd>


PEST Control File Section: LSQR
-------------------------------

The ``* lsqr`` section controls use of the LSQR algorithm for solution of
the inverse problem.

.. toctree::
   :maxdepth: 1

   LSQR — Configure LSQR <dpest.utils.lsqr>
   Remove LSQR — Remove LSQR settings <dpest.utils.rmv_lsqr>


PEST Control File Section: Regularisation
-----------------------------------------

The ``* regularisation`` section controls regularisation and adjustment of
the regularisation weight factor.

.. toctree::
   :maxdepth: 1

   Regularisation — Configure regularisation settings <dpest.utils.regularisation>