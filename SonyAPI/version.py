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

__author__ = 'Kevin G. Schlosser'
__author_email__ = 'Kevin.G.Schlosser@gmail.com'
__version__ = '0.1.1b2'
__version_info__ = (0, 1, 1, 'b2')
__description__ = 'Sony Bravia TV interface (generation 3)'
__url__ = 'https://github.com/kdschlosser/SonyAPI'
__requirements__ = ['requests >= 2.18.4', 'setuptools >= 36.3.0']
__keywords__ = 'Sony SonyAPI Bravia BraviaAPI SonyTV BraviaTV'
__license__ = 'GPL-2.0'
__download_url__ = (
    'https://github.com/kdschlosser/SonyAPI/archive/%s.tar.gz' % __version__
)

status = dict(
    a='3 - Alpha',
    b='4 - Beta',
    pre='2 - Pre-Alpha'
)

dev_status = status.get(__version__[-1][:-1], '5 - Production/Stable')

__classifiers__ = [
    'Development Status :: ' + dev_status,
    'Operating System :: MacOS',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: Unix',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Other Audience',
    'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Topic :: Multimedia',
    'Topic :: Other/Nonlisted Topic',
    'Topic :: Home Automation'
]

del dev_status
del status
