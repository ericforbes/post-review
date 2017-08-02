#!/usr/bin/env python

from setuptools import setup, find_packages
import re
import codecs
import os.path
import sys

requires = ['requests==2.18.1',
            'future==0.16.0',
            'coloredlogs==7.1',
            'configparser==3.5.0'
            ]


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


#Unable to use just Manifest because config.ini exists in a package
#Must use both package_data and Manifest

setup_options = dict(
    name='post-review',
    version=find_version("postreview", "__init__.py"),
    description='unified command line interface for posting code reviews and merge requests',
    long_description=open('README.rst').read(),
    url='https://github.com/ericforbes/post-review',
    author='Eric Forbes',
    author_email='ericforbes91@gmail.com',
    license='MIT',
    keywords='git devops review',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    package_data={
        'postreview': ['config.ini']
    },
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,<4',
    entry_points={
        'console_scripts': [
            'post-review=postreview.__main__:main'
        ]
    },
    install_requires=[
        'requests>=2.18',
        'coloredlogs>=7.1',
        'configparser>=3.5.0',
        'future>=0.16.0'
        ],
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Version Control :: Git',
        )
    )

setup(**setup_options)