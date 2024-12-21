from setuptools import setup, find_packages
import os

setup(
    name='fractals',
    version='0.1.0',
    author='Gillian Smith',
    url="https://github.com/gillian-smith/fractals",
    license="gpl-3.0",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pillow'
    ]
)