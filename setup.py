# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in bep_customization/__init__.py
from bep_customization import __version__ as version

setup(
	name='bep_customization',
	version=version,
	description='customization',
	author='saw',
	author_email='saw',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
