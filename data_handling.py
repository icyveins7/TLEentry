# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 16:56:41 2020

@author: Lken
"""

import zipfile
import os
import re

# data specific
def compressTLEandBulletins(zippath='temp.zip', zipcomp=zipfile.ZIP_LZMA):
    filepaths = []
    zippath = os.path.join(os.getcwd(), zippath)
    for file in os.listdir('.'):
        if re.search('\d\d\d\d-\d\d-\d\d \d\d_\d\d', file) is not None:
            filepath = file
            filepaths.append(filepath)
    compressFiles(filepaths, zippath, zipcomp)

# generic
def compressFiles(filepaths, zippath, zipcomp=zipfile.ZIP_LZMA):
    z = zipfile.ZipFile(zippath, 'w', zipcomp)
    
    for i in range(len(filepaths)):
        z.write(filepaths[i])
    
    z.close()