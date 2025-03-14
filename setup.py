from setuptools import setup, find_packages
import setuptools_scm

setup(
    name="dpest",
    use_scm_version=True,  # This enables dynamic versioning
    setup_requires=["setuptools>=45", "setuptools_scm"],  # Ensure setuptools_scm is available during setup
    packages=find_packages(include=["dpest", "dpest.*"]),
    include_package_data=True,  # Ensures non-Python files are included
    package_data={
        "dpest": ["**/*.yml", "**/*.yaml"],  # Include all YAML files recursively
    },
    python_requires=">=3.7",
)
