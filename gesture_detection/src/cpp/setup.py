from setuptools import setup, Extension
import pybind11
import numpy as np
import os

# Use absolute path for the cpp file
current_dir = os.path.dirname(os.path.abspath(__file__))
cpp_file = os.path.join(current_dir, 'custom_distance.cpp')

ext_modules = [
    Extension(
        'custom_distance',
        [cpp_file],  
        include_dirs=[
            pybind11.get_include(),
            np.get_include()
        ],
        language='c++'
    ),
]

setup(
    name='custom_distance',
    version='0.0.1',
    author='User',
    author_email='user@example.com',
    description='Provides a custom distance for gesture detection',
    ext_modules=ext_modules,
    python_requires='>=3.6',
    install_requires=[
        'pybind11>=2.6.0',
        'numpy'
    ],
)
