from setuptools import setup, find_packages

requiredPackages = [#should only contain third party pakages
    "coloredlogs",
    "xmltodict"
],

setup(
    name="ZES Zimmer zlr decoder",
    version="0.1",
    author="Manuel Pitz (RWTH Aachen University)",
    author_email="manuel.pitz@eonerc.rwth-aachen.de",
    install_requires = requiredPackages,
    packages= []
)