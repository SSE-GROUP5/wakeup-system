""" Setup file for the zeromq package. """
from setuptools import setup, find_packages

setup(
    name='zeromq',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyzmq',
    ]
)