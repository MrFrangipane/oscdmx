from os import path
from codecs import open
from setuptools import setup, find_packages


NAME = 'oscdmx'
VERSION = '0.0.3'
DESCRIPTION = 'OSC and DMX'
AUTHOR = 'MrFrangipane'
AUTHOR_EMAIL = 'mr@frangipane.me'


_here = path.abspath(path.dirname(__file__))
_readme_filepath = path.join(_here, 'README.md')
_requirements_filepath = path.join(_here, 'requirements.txt')


if path.isfile(_readme_filepath):
    with open(_readme_filepath, encoding='utf-8') as readme_file:
        _long_description = readme_file.read()
else:
    _long_description = 'Unable to load README.md'


if path.isfile(_requirements_filepath):
    with open(_requirements_filepath) as requirements_file:
        _requirements = requirements_file.readlines()
else:
    _requirements = list()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=_long_description,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(exclude=['tests']),
    install_requires=_requirements,
    include_package_data=True
)
