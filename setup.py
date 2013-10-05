#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages

with open('README.rst') as file:
    long_description = file.read()

setup(name='XAIL',
      version='0.0.1',
      description='eXtensible AI Language for Python',
      long_description=long_description,
      author='Xiaomao Chen',
      author_email='xiaomao5@live.com',
      url='http://dev.ivybits.tk/projects/pyxail',
      packages=find_packages(),
      install_requires=['stemming'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Communications :: Chat',
          'Topic :: Education',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          ],
     )