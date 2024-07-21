"""Setup script."""

import os
import pathlib

from setuptools import find_packages
from setuptools import setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
VERSION = get_version("multimodal/src/version.py")

setup(
    name="multimodal",
    description="Multimodal SDK.",
    long_description_content_type="text/markdown",
    long_description=README,
    version=VERSION,
    url="https://github.com/donigian/multimodal-sdk",
    author="armen donigian",
    author_email="donigian@gmail.com",
    license="Apache License 2.0",
    install_requires=[
        "absl-py",
        "numpy",
        "rich",
        "namex",
        "h5py",
        "optree",
        "ml-dtypes",
        "packaging",
    ],
    # Supported Python versions
    python_requires=">=3.9",
    classifiers=[
    ],
    packages=find_packages(
        include=("multimodal_sdk", "multimodal_sdk.*"),
        exclude=("*_test.py", "benchmarks"),
    ),
)
