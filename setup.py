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
from setuptools import setup, find_packages
from SonyAPI.version import (
    __version__,
    __author__,
    __author_email__,
    __url__,
    __download_url__,
    __description__,
    __requirements__,
    __keywords__
)

sys.path.insert(0, '.')

setup(
    name='SonyAPI',
    version=__version__,
    description=__description__,
    install_requires=__requirements__,
    maintainer=__author__,
    author=__author__,
    author_email=__author_email__,
    zip_safe=True,
    packages=find_packages(),
    include_package_data=True,
    url=__url__,
    download_url=__download_url__,
    keywords=__keywords__,
    classifiers=[]
)
