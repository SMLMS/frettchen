#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 08:58:39 2020

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
import pandas as pd
import numpy as np

class FretPair:
    def __init__(self):
        self._spectra = pd.DataFrame()
        self._donorQuantumYield = 1.0
        self._kappaSquare = 2.0/3.0
        self._opticalDensity = 1.0
        self._molarExtinctionCoefficientAcceptor = 0.0
        self._acceptorExtinctionWavelength = 0.0
        self._overlapIntegral = 0.0
        self._foersterRadius = 0.0
        
    @property
    def spectra(self):
        return(self._spectra)
    
    @property
    def donorQuantumYield(self):
        return(self._donorQuantumYield)
    
    @donorQuantumYield.setter
    def donorQuantumYield(self, value: float):
        self._donorQuantumYield = value
        
    @property
    def kappaSquare(self):
        return(self._kappaSquare)
    
    @kappaSquare.setter
    def kappaSquare(self, value: float):
        self._kappaSquare = value
        
    @property
    def opticalDensity(self):
        return(self._opticalDensity)
    
    @opticalDensity.setter
    def opticalDensity(self, value: float):
        self._opticalDensity = value
        
    @property
    def molarExtinctionCoefficientAcceptor(self):
        return(self._molarExtinctionCoefficientAcceptor)
        
    @molarExtinctionCoefficientAcceptor.setter
    def molarExtinctionCoefficientAcceptor(self, value: float):
        self._molarExtinctionCoefficientAcceptor = value
        
    @property
    def acceptorExtinctionWavelength(self):
        return(self._acceptorExtinctionWavelength)
    
    @acceptorExtinctionWavelength.setter
    def acceptorExtinctionWavelength(self, value: float):
        self._acceptorExtinctionWavelength = value
        
    @property
    def overlapIntegral(self):
        return(self._overlapIntegral)
    
    @property
    def foersterRadius(self):
        return(self._foersterRadius)
    
    def loadSprectra(self, fileName: str):
        self._spectra = pd.read_excel(io = fileName, sheet_name = "spectra", header = 0)
        
    def normalizeEmissionSpectrum(self):
        area = abs(np.trapz(self.spectra["donor_emission"], self.spectra["wavelength_[nm]"]))
        self._spectra["donor_emission_normalized"] = self.spectra["donor_emission"]/area
        
    def normalizeAbsorptionSpectrum(self):
        index = np.searchsorted(self.spectra["wavelength_[nm]"], self.acceptorExtinctionWavelength)
        
        self._spectra["acceptor_absorption_[1/(M*cm)]"] = np.dot(np.divide(self.spectra["acceptor_absorption"],
                                                                           self.spectra["acceptor_absorption"][index]),
                                                                 self.molarExtinctionCoefficientAcceptor)
        
    def calcOverlap(self):
        self._spectra["overlap"]=(self.spectra["acceptor_absorption_[1/(M*cm)]"])*(self.spectra["donor_emission_normalized"])* (self.spectra["wavelength_[nm]"]**4)

    def calcOverlapIntegral(self):
        self._overlapIntegral = abs(np.trapz(self.spectra["overlap"], self.spectra["wavelength_[nm]"]))

    def calcFoersterRadius(self):
        self._foersterRadius=0.211*(((self.opticalDensity**-4)*self.kappaSquare*self.donorQuantumYield*self.overlapIntegral)**(1.0/6.0))
        
    def fit(self):
        self.normalizeEmissionSpectrum()
        self.normalizeAbsorptionSpectrum()
        self.calcOverlap()
        self.calcOverlapIntegral()
        self.calcFoersterRadius()
        
    def saveSpectra(self, writer: pd.ExcelWriter):
        self.spectra.to_excel(excel_writer = writer,
                              sheet_name = "spectra",
                              header = True,
                              index = False)
        
    def saveModel(self, writer: pd.ExcelWriter):
        data = {"parameter":["donor quantum yield", "K^2", "optical density", "molar extinction coefficient acceptor [M^-1 cm^-1]", "extinction coefficient wavelength [nm]", "overlap integral", "Foerster Radius [A]"],
              "values": [self.donorQuantumYield, self.kappaSquare, self.opticalDensity, self.molarExtinctionCoefficientAcceptor, self.acceptorExtinctionWavelength, self.overlapIntegral, self.foersterRadius]
              }
        df = pd.DataFrame.from_dict(data)
        df.to_excel(excel_writer = writer,
                    sheet_name = "FRET",
                    header = True,
                    index = False)
        
    def save(self, fileName: str):
        with pd.ExcelWriter(fileName) as writer:
            self.saveSpectra(writer)
            self.saveModel(writer)
        
    def __str__(self):
        string = str("FretPair\ndonor quantum yield: %.3e\nK^2: %.3e\noptical density: %.3f\nmolar extinction coefficient acceptor [M^-1 * cm^-1]: %.3e\nextinction coefficient wavelength [nm]: %.3f\noverlap integral: %.3e\nFoerster Radius [A]: %.3f\n "
                     %(self.donorQuantumYield,
                       self.kappaSquare,
                       self.opticalDensity,
                       self.molarExtinctionCoefficientAcceptor,
                       self.acceptorExtinctionWavelength,
                       self.overlapIntegral,
                       self.foersterRadius)
                     )
        return string
    
    def __del__(self):
        message  = str("removed instance of FretPairs from heap.")
        print(message)

def main():
    fileName = "../../cy3-cy5.xlsx"
    fp = FretPair()
    fp.donorQuantumYield = 0.15
    fp.kappaSquare = 2.0/3.0
    fp.opticalDensity = 1.33
    fp.molarExtinctionCoefficientAcceptor = 250e3
    fp.acceptorExtinctionWavelength = 646
    fp.loadSprectra(fileName)
    fp.fit()
    fp.save("../../result.xlsx")
    print(fp)
    
    
if __name__ == '__main__':
    main()    