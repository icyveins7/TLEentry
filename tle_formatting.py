# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 10:46:24 2020

@author: Seo
"""

import re
import datetime as dt
import hashlib

def TLEformatting(readmepath='tle.format'):
    f = open(readmepath,'r')
    l = f.readlines()
    f.close()
    
    l = [i.strip() for i in l]
    
    linenumber = []
    fieldnumber = []
    labels = []
    idx = []
    
    for i in range(len(l)):
        line = l[i]
        # get line number
        linenumber.append(line[0])
        # get field number
        fieldnumber.append(line[2:4].strip())
        # get idx
        a = line[5:10]
        thisidx = [int(i) for i in a.split('-')]
        thisidx[0] = thisidx[0] - 1 # correct for starting index
        idx.append(thisidx)
        # get labels
        labels.append(line[11:])
        
    return idx, labels, linenumber, fieldnumber

def readTLE(tlepath, idx, labels, linenumber, fieldnumber, names):
    f = open(tlepath,'r')
    l = f.readlines()
    f.close()
    
    l = [i.strip() for i in l]
    
    for name in names:
        found = False
        # start from 1st line
        i = 0
        while (i<len(l)):
            if re.match(name, l[i]):
                i = i + 1
                linesRead = 0
                # read more lines until the 2nd line is read (to avoid \r\n ambiguity)
                while (linesRead < 2):
                    if (len(l[i]) > 0):
                        if 
                    
            else:
                # increment
                i = i + 1
    
    

def bulletinFormatting(readmepath = 'readme.finals'):
    f = open(readmepath,'r')
    l = f.readlines()
    f.close()
    
    l = [i.strip() for i in l]
    
    labels = []
    idx = []
    
    # iterate only lines with number - number
    for i in range(len(l)):
        if re.match('\d+[-]\d+', l[i][0:7]) is not None:
            # we also want the contents to not be blank
            if re.search('blank', l[i][17:]) is None:
                a = l[i][:7]
                thisidx = [int(i) for i in a.split('-')]
                thisidx[0] = thisidx[0] - 1 # correct for starting index
                idx.append(thisidx)
                
                labels.append(l[i][17:])
    
    return idx, labels
    
def readBulletin(bullpath, idx, labels, t=dt.datetime.now()):
    f = open(bullpath,'r')
    l = f.readlines()
    f.close()
    
    l = [i.strip() for i in l]
    
    # we look for the line corresponding to now
    y = t.strftime('%y')
    m = t.strftime('%m')
    d = t.strftime('%d')
    # correction to turn starting 0s into blanks
    if y[0] == '0':
        y = ' ' + y[1]
    if m[0] == '0':
        m = ' ' + m[1]
    if d[0] == '0':
        d = ' ' + d[1]
    ymd = y + m + d
    
    found = False
    vals = []
    for i in range(len(l)):
        if l[i][:6] == ymd:
            # then we process each bit one by one
            line = l[i]
            # fill out the string to the same length
            if len(line) != 185:
                line = line.ljust(185)
            for k in range(len(idx)):
                start = idx[k][0]
                end = idx[k][1]
                print('Label %s : %s' % (labels[k], line[start:end]))
                
                if line[start:end].isspace():
                    vals.append('') # just append a blank
                else:
                    vals.append(float(line[start:end]))
                
            # let's conveniently fix the first 3 as integers
            for k in range(3):
                vals[k] = int(vals[k])
                
            print(l[i])
            
            # let's hash it with a simple function
            m = hashlib.blake2b(digest_size=4)
            m.update(l[i].encode('utf-8'))
            hashdigest = m.hexdigest()
            print('Blake2b hash = %s' % (hashdigest))
            
            # end it here
            found = True
            break
        
    if found:
        return hashdigest, vals, line
    else:
        return None