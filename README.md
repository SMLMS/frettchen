# frettchen
A package to model fret pairs

## Generate distribution archive
python -m pip install --user --upgrade setuptools wheel
python setup.py sdist bdist_wheel

## Installation
python -m pip install ~/path/to/wheel

## Usage
### for help
python frettchen.py -h
### test data set
python frettchen.py -f data/cy3-cy5.xlsx  -q 0.15 -e 250000.0 -l 646
