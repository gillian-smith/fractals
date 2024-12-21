from setuptools import setup, find_packages
import os

setup(
    name='fractals',
    version='0.1.0',
    author='Gillian Smith',
    url="https://github.com/gillian-smith/fractals",
    license="gpl-3.0",
    entry_points={"console_scripts": ["render_fractal = fractals.render_fractal:main"]},
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pillow'
    ]
)