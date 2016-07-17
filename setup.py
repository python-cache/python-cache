import codecs
import os
import sys

from distutils.util import convert_path
from fnmatch import fnmatchcase
from setuptools import setup, find_packages


def readme():
    return open(os.path.join(os.path.dirname(__file__), 'README.md'), "r").read()

setup(
    name='python-cache',
    packages = find_packages(exclude=["tests.*", "tests"]),
    version='0.0.9',
    description='Pythonic way of Caching',
    long_description=readme(),
    author='python-cache',
    author_email='kevin830222@gmail.com, alan4chen@kimo.com',
    url='https://github.com/python-cache/python-cache',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Intended Audience :: Developers'
    ],
    install_requires=[],
    include_package_data=True,
    license='MIT License',
)


