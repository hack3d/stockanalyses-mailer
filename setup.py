# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='stockanalyses-mailer',
	version='0.1.0',
	description='Send mails from a queue.',
	url='http://stockdashboard.de',
	author='Raphael Lekies',
	author_email='raphael.lekies@stockdashboard.de',
	maintainer='Raphael Lekies',
	maintainer_email='raphael.lekies@stockdashboard.de',
	license='Commercial',
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
	entry_points={
		'console_scripts': [
			'stockanalyses-mailer = mailer:main'
]
	}
)