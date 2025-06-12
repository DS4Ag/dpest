import os
import subprocess
from dpest.wheat.utils import uplantgro

# User-editable section for system DSSAT installation
dssat_install_dir = r'C:\DSSAT48'  # System DSSAT installation folder
dssat_exe = os.path.join(dssat_install_dir, 'DSCSM048.EXE')
control_file = os.path.join(dssat_install_dir, 'Wheat', 'DSSBatch.v48')

# Project data directory (relative to script location)
project_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(project_dir, 'DSSAT48')
output_dir = os.path.join(data_dir, 'Wheat')

# Change working directory to the output directory
os.chdir(output_dir)

# Build and run DSSAT command
module = 'CSCER048'
switch = 'B'
command_line = f'"{dssat_exe}" {module} {switch} "{control_file}"'
result = subprocess.run(command_line, shell=True, check=True, capture_output=True, text=True)
print(result.stdout)

# Use uplantgro from dpest.wheat.utils to extract and update data from PlantGro.OUT if needed
uplantgro(
    plantgro_file_path=os.path.join(output_dir, 'PlantGro.OUT'),
    treatment='164.0 KG N/HA IRRIG',
    variables=['LAID', 'CWAD', 'T#AD']
)
