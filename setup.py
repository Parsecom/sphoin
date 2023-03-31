#!/usr/bin/env python

__author__ = "pom11"
__copyright__ = "Copyright 2023, Parsec Original Mastercraft S.R.L."
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "pom11"
__email__ = "office@parsecom.ro"

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
	readme = readme_file.read()

requirements = ["requests==2.28.1","pyyaml==6.0","textual==0.15.1","rich==13.3.3","python-dateutil==2.8.2","linkify-it-py==2.0.0"]

setup_requirements = [ ]


setup(
	author="P.O.M.",
	author_email='office@parsecom.ro',
	python_requires='>=3.6',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: 3.10',
		'Programming Language :: Python :: 3.11',
	],
	description="Connect to sphoin.app Pro Slots",
	entry_points={
		'console_scripts': [
			'sphoin=sphoin.cli:main',
			'sphoin.plot=sphoin.plot:test'
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
	version='2.0.0',
	zip_safe=True,
)