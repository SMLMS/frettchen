#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 15:18:40 2020

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

import os
from datetime import datetime


class FileNames:
    def __init__(self):
        self._fileName = str()
        self._folderName = str()
        self._baseName = str()
        self._supplementalInformation = str()
        self._dateString = str()
        self._suffix = str()
        self._outFileName = str()
    
    @property
    def fileName(self):
        return self._fileName
    
    @fileName.setter
    def fileName(self, name: str):
        if(type(name) != str):
            errorMessage = str('FileNames instance variable fileName should be of type str, was of type %s.' % (type(name)))
            raise Exception(errorMessage)
        else:
            self._fileName = name
    
    @property
    def folderName(self):
        return self._folderName
    
    @folderName.setter
    def folderName(self, name: str):
        if(type(name) != str):
            errorMessage = str('FileNames instance variable folderName should be of type str, was of type %s' % (type(name)))
            raise Exception(errorMessage)
        else:
            self._folderName = name
        
    @property
    def baseName(self):
        return self._baseName
    
    @baseName.setter
    def baseName(self, name: str):
        if(type(name) != str):
            errorMessage = str('FileNames instance variable folderName should be of type str. was of type %s' %(type(name)))
            raise Exception(errorMessage)
        else:
            self._baseName = name
    
    @property
    def supplementalInformation(self):
        return self._supplementalInformation
    
    @supplementalInformation.setter
    def supplementalInformation(self, si: str):
        if(type(si) != str):
            errorMessage = str("FileNames instance variable supplementalInformation should be of type str, was of type %s." % (type(si)))
            raise Exception(errorMessage)
        else:
            self._supplementalInformation = si
    
    @property
    def dateString(self):
        return self._dateString
    
    @property
    def suffix(self):
        return self._suffix
    
    @suffix.setter
    def suffix(self, name: str):
        if(type(name) != str):
            errorMessage = str('FileNames instance variable suffix should be of type str, was of type %s' % (type(name)))
            raise Exception(errorMessage)
        else:
            self._suffix = name
    
    @property
    def outFileName(self):
        return self._outFileName
    
    def splitFileName(self):
        self.folderName = os.path.dirname(self.fileName)
        [self.baseName, self.suffix]=os.path.basename(self.fileName).split(".")
        
    def mergeFileName(self):
        self._outFileName = str('%s/%s_%s_%s.%s' % (self.folderName,
                                                    self.baseName,
                                                    self.supplementalInformation,
                                                    self.dateString,
                                                    self.suffix))
    
    def updateDateString(self):
        now = datetime.now()
        self._dateString = str("%s%s%s" %(now.strftime("%y"),
                                         now.strftime("%m"),
                                         now.strftime("%d")))
        
    def __str__(self):
        string = str("FileNames\nfileName: %s\nfolderName: %s\nbaseName: %s\nsupplementaryInformation: %s\ndateString: %s\nsuffix: %s\noutFileName: %s\n" %(self.fileName,
                                                                                                                                                            self.folderName,
                                                                                                                                                            self.baseName,
                                                                                                                                                            self.supplementalInformation,
                                                                                                                                                            self.dateString,
                                                                                                                                                            self.suffix,
                                                                                                                                                            self.outFileName))
        return string
    
    def __del__(self):
        message  = str("removed instance of FileNames from heap.")
        print(message)
        
    
def main():
    fn = FileNames()
    fn.fileName = "/home/test.txt"
    fn.splitFileName()
    fn.updateDateString()
    print(fn)
    fn.supplementalInformation = "fluxImage"
    fn.suffix = "jpg"
    fn.mergeFileName()
    print(fn)
    
   
if __name__ == '__main__':
    main()