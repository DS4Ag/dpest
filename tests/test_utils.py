from pathlib import Path
from dpest.utils import *

# Setup path
repo_root = Path(__file__).parent.parent
pst_file_path = repo_root / "tests/dpest_out/PEST_CONTROL.pst"


# Set RSTFLE to “restart”
rstfle(pst_file_path, "restart")

# Set PESTMODE to “prediction”
pestmode(pst_file_path, "prediction")

# Set RLAMBDA1 to 5.0
rlambda1(pst_file_path, 5.0)

# Set RLAMFAC to 2.0:
rlamfac(pst_file_path, 2.0)

# Set PHIRATSUF to 0.3
phiratsuf(pst_file_path, 0.3)

# Set PHIREDLAM to 0.03
phiredlam(pst_file_path, 0.03)

# Set NUMLAM to 10
numlam(pst_file_path, 10)

# Set RELPARMAX to 0.2
relparmax(pst_file_path, 0.2)

# Set FACPARMAX to 2.0
facparmax(pst_file_path, 2.0)

# Set FACORIG to 01
facorig(pst_file_path, 0.1)

# Set PHIREDSWH to 0.1
phiredswh(pst_file_path, 0.1)

# Set NOPTMAX to 50 (iterative optimization)
noptmax(pst_file_path, new_value = 50)

# Set PHIREDSTP to 0.01
phiredstp(pst_file_path, 0.01)

# Set NPHISTP to 3
nphistp(pst_file_path, 3)

# Set NPHINORED to 5
nphinored(pst_file_path, 5)

# Set RELPARSTP to 0.01
relparstp(pst_file_path, 0.01)

# Set NRELPAR to 3
nrelpar(pst_file_path, 3)

# Updating Specific LSQR Parameters in an Existing PEST Control File
lsqr(
    pst_path = pst_file_path,
    lsqr_atol = 1e-6,
    lsqr_btol = 1e-6,
    lsqr_itnlim = 50
)

# Disabling LSQR Mode While Maintaining Other Settings
lsqr(
    pst_path = pst_file_path,
    lsqrmode = 0
)

# Adding an SVD Section to a PEST Control File with Default Parameters
svd(
    pst_path = pst_file_path
)

# Customizing SVD Parameters in an Existing PEST Control File
svd(
    pst_path = pst_file_path,
    maxsing = 500,
    eigthresh = 0.01,
    eigwrite = 1
)

# Removing the LSQR Section from a PEST Control File
rmv_splitcols(pst_file_path)