#!/usr/bin/env python

__author__ = "pom11"
__copyright__ = "Copyright 2022, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "1.1.0"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
	readme = readme_file.read()

requirements = ["requests","pyyaml","textual"]

setup_requirements = [ ]


setup(
	author="P.O.M.",
	author_email='office@parsecom.ro',
	python_requires='>=3.6',
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: 3.10',
	],
	description="Connect to sphoin.app Pro Slots",
	entry_points={
		'console_scripts': [
			'sphoin=sphoin.cli:main',
		],
	},
	install_requires=requirements,
	license="MIT license",
	long_description=readme,
	long_description_content_type="text/markdown",
	include_package_data=True,
	keywords='sphoin',
	name='sphoin',
	packages=find_packages(include=['sphoin', 'sphoin.*']),
	setup_requires=setup_requirements,
	url='https://github.com/Parsecom/sphoin',
	version='1.1.0',
	zip_safe=True,
)