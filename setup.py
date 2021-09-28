#!/usr/bin/env python

from setuptools import setup, find_packages

with open("requirements.txt", "r") as reqs_file:
    requirements = reqs_file.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = "0.0.4"

setup(name='repositories_collector',
      version=VERSION,
      description='A tool to query GraphQL for collecting repositories metadata.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Stefano Dalla Palma',
      maintainer='Stefano Dalla Palma',
      author_email='stefano.dallapalma0@gmail.com',
      url='https://github.com/radon-h2020/radon-repositories-collector',
      download_url=f'https://github.com/radon-h2020/radon-repositories-collector/archive/{VERSION}.tar.gz',
      packages=find_packages(exclude=('tests',)),
      entry_points={
          'console_scripts': ['repositories-collector=repocollector.cli:main'],
      },
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: Apache Software License",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Operating System :: OS Independent"
      ],
      install_requires=requirements
)
