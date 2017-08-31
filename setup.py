# -*- coding: utf-8 -*-
#
# SonyAPI
# External control of Sony Bravia Generation 3 TV's
# Copyright (C) 2017  Kevin G. Schlosser
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import sys
import os
from setuptools import setup, find_packages
from SonyAPI.version import __version__, __author__

sys.path.insert(0, '.')
CURRENT_DIR = os.path.dirname(__file__)

setup(
    name='SonyAPI',
    version=__version__,
    description=open(os.path.join(CURRENT_DIR, 'README.md')).read(),
    install_requires=['requests>=2.18.4', 'setuptools>=36.3.0'],
    maintainer=__author__,
    zip_safe=True,
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/kdschlosser/SonyAPI'
)
