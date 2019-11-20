# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import versioneer

requires = open('requirements.txt').read().strip().split('\n')

setup(
    name='intake_iris',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Iris plugins for Intake',
    url='https://github.com/informatics-lab/intake-iris',
    maintainer='Peter Killick',
    maintainer_email='peter.killick@informaticslab.co.uk',
    license='BSD',
    py_modules=['intake_iris'],
    packages=find_packages(),
    entry_points={
        'intake.drivers': [
            'netcdf = intake_iris.netcdf:NetCDFSource',
            'grib = intake_iris.grib:GRIBSource',
        ]
    },
    package_data={'': ['*.csv', '*.yml', '*.html']},
    include_package_data=True,
    install_requires=requires,
    long_description=open('README.md').read(),
    zip_safe=False, )
