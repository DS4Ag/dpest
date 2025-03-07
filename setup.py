from setuptools import setup, find_packages

setup(
    name="dpest",
    version="1.1.2",
    packages=find_packages(include=["dpest", "dpest.*"]),
    include_package_data=True,  # Ensures non-Python files are included
    package_data={
        "dpest": ["**/*.yml", "**/*.yaml"],  # Include all YAML files recursively
    },
    python_requires=">=3.7",
)

# setup(
#     name="dpest",
#     version="1.1.2",
#     packages=find_packages(include=["dpest", "dpest.*"]),
#     install_requires=[
#         "pyemu>=1.3.8",
#         "pyyaml>=6.0.2",
#         "pandas>=2.2.3",
#         "matplotlib>=3.10.1",
#         "flopy>=3.9.2"
#     ],
    
#     python_requires=">=3.7",
# )