#!/usr/bin/env python

from setuptools import setup,find_packages
from m3project_creator.pkg_creator import __version__

setup(name='m3project-creator',
      install_requires=['distribute'],
      version=__version__,
      description='M3 CMake project generator',
      author='Antoine Hoarau',
      author_email='hoarau.robotics@gmail.com',
      url='https://github.com/ahoarau/m3-cmake-project-creator',
      requires=['gtk'],
      license="GPL",
      scripts=["m3project_creator.py"],
      packages=find_packages(),
      include_package_data=True,
     )
