
import sys
import os
from setuptools import setup, find_packages

sys.path.insert(0, '.')

CURRENT_DIR = os.path.dirname(__file__)

setup(
    name='SonyAPI',
    version='0.0.1',
    description=open(os.path.join(CURRENT_DIR, 'README.md')).read(),
    install_requires=['requests'],
    maintainer='Kevin Schlosser',
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/kdschlosser/SonyAPI'
)
