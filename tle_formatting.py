# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 10:46:24 2020

@author: Seo
"""

import re
import datetime as dt

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
    
def readBulletin(bullpath, idx, labels):
    f = open(bullpath,'r')
    l = f.readlines()
    f.close()
    
    l = [i.strip() for i in l]
    
    # we look for the line corresponding to now
    utcnow = dt.datetime.now()
    y = utcnow.strftime('%y')
    m = utcnow.strftime('%m')
    d = utcnow.strftime('%d')
    # correction to turn starting 0s into blanks
    if y[0] == '0':
        y = ' ' + y[1]
    if m[0] == '0':
        m = ' ' + m[1]
    if d[0] == '0':
        d = ' ' + d[1]
    ymd = y + m + d
    
    found = False
    for i in range(len(l)):
        if l[i][:6] == ymd:
            # then we process each bit one by one
            line = l[i]
            for k in range(len(idx)):
                start = idx[k][0]
                end = idx[k][1]
                print('Label %s : %s' % (labels[k], line[start:end]))
                
                
            
            print(l[i])
            
            # end it here
            found = True
            break
        
    if found:
        return l[i]