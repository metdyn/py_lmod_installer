# (C) Copyright 2021-2022 United States Government as represented by the Administrator of the
# National Aeronautics and Space Administration. All Rights Reserved.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.


# --------------------------------------------------------------------------------------------------


import os.path
import setuptools


# --------------------------------------------------------------------------------------------------


setuptools.setup(
    name='py-lmod-installer',
    author='NASA Global Modeling and Assimilation Office',
    description='Install Python packages to be compliant with Lmod',
    url='https://github.com/geos-esm/py-lmod-installer',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'py_installer = py_lmod_installer.py_installer:main'
        ],
    },
)


# --------------------------------------------------------------------------------------------------
