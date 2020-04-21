#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:19:59 2020

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

import argparse
from frettchen.source.fileNames import FileNames
from frettchen.source.fretPair import FretPair

def getParser():
     parser = argparse.ArgumentParser(prog = 'frettchen',
                                 description = "A tool to model FRET Pairs \n\n"\
                                     "frettchen Copyright (C) 2020  Sebastian Malkusch\n"\
                                     "malkusch@med.uni-frankfurt.de\n"\
                                     "This program comes with ABSOLUTELY NO WARRANTY;\n"\
                                     "This is free software, and you are welcome to redistribute it under certain conditions;\n"\
                                     "<https://www.gnu.org/licenses/gpl-3.0.txt>",
                                 epilog="go frettchen!",
                                 formatter_class=argparse.RawTextHelpFormatter)
     parser.add_argument("-f", type = str, help = "Excel file comprising spectra information in sheet 'spectra'.")
     parser.add_argument("-q", type=float, help="Qantum yield of donor.")
     parser.add_argument("-k", type=float, help="Factor for relative dipole-dipole orientation (default is kappa^2=2/3.0).", default=2/3.0)
     parser.add_argument("-n", type=float, help="Refractive index of solvent (default is 1.33).", default=1.33)
     parser.add_argument("-e", type=float, help="Extinction coefficient of acceptor in [1/(M*cm)]")
     parser.add_argument("-l", type=float, help="Wavelength at which extinction coefficient is measured  in [nm]")
     return(parser)

def checkParser(args):
    parserValid = True
    errIndex = 0
    if not args.f:
        errIndex += 1
        print ("error %i: fret spectra need to be defined" %(errIndex))
    if not args.q:
        errIndex += 1
        print ("error %i: quantum yield of donor needs to be defined" %(errIndex))
    if not args.e:
        errIndex += 1
        print("error %i: molar extinction coefficient of acceptor needs to be defined" %(errIndex))
    if not args.l:
        errIndex += 1
        print("error %i: molar extinction coefficient wavelength needs to be defined" %(errIndex))
    if errIndex>0:
        print("Program exits with %i error messages." %(errIndex))
        parserValid = False
    return(parserValid)

def main(args = None):
    parser = getParser()
    args = parser.parse_args(args)
    if(checkParser(args)):
        fn = FileNames()
        fn.fileName = args.f
        fn.splitFileName()
        fn.updateDateString()
        fn.supplementalInformation = "FRET-Model"
        fn.suffix = "xlsx"
        fn.mergeFileName()

        fp = FretPair()
        fp.donorQuantumYield = args.q
        fp.kappaSquare = args.k
        fp.opticalDensity = args.n
        fp.molarExtinctionCoefficientAcceptor = args.e
        fp.acceptorExtinctionWavelength = args.l
        fp.loadSprectra(args.f)
        fp.fit()
        print(fp)
        fp.save(fn.outFileName)
    else:
        exit()


if __name__ == '__main__':
    main()