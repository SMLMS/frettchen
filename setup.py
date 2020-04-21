#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 16:45:05 2020

@author: malkusch

Frettchen a tool to model FRET pairs

    Copyright (C) 2020  Sebastian Malkusch

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="frettchen",
    version="20.4",
    author="Sebastian Malkusch",
    author_email="malkusch@med.uni-frankfurt.com",
    description="a package for modeling fret pairs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SMLMS/frettchen",
    packages=setuptools.find_packages(),
	install_requires=['numpy',
                   'pandas'],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
        ],
)