#!/usr/bin/env python

# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: Czech Technical University in Prague

from setuptools import setup
from catkin_pkg.python_setup import generate_distutils_setup

setup_kwargs = generate_distutils_setup()
setup_kwargs['packages'] = ['zyxel_gs1200_api']
setup_kwargs['package_dir'] = {'': 'src'}

setup(**setup_kwargs)
