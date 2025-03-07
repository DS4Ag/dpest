from setuptools import setup, find_packages

setup(
    name="dpest",
    version="1.1.3",
    packages=find_packages(include=["dpest", "dpest.*"]),
    include_package_data=True,  # Ensures non-Python files are included
    package_data={
        "dpest": ["**/*.yml", "**/*.yaml"],  # Include all YAML files recursively
    },
    python_requires=">=3.7",
)
