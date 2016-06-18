from setuptools import setup

import os


def readme():
    return open(os.path.join(os.path.dirname(__file__), 'README.md'), "r").read()

setup(
    name='pycache-adaptor',
    packages=['PycacheAdaptor'],
    version='0.0.1',
    description='Pythonic way of Caching',
    long_description=readme(),
    author='pycache-adaptor',
    author_email='kevin830222@gmail.com, alan4chen@kimo.com',
    url='https://github.com/pycache-adaptor/pycache-adaptor.git',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Intended Audience :: Developers'
    ],
    install_requires=[],
    include_package_data=True,
    license='MIT License',
)
