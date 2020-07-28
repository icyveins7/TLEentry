# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 19:20:20 2020

@author: Seo
"""


file = '2020-07-28 18_06.txt'

f = open(file,'r')
lines = f.readlines()
f.close()

# get rid of all white space and all empty lines
validlines = []
for i in lines:
    if len(i) > 1:
        validlines.append(i.strip())
        
# if not divisible by 3, there's something wrong
assert(len(validlines)%3 == 0)

# open a new file and write all of the constants into it
fw = open('knownGeos.txt','w')

for i in range(int(len(validlines)/3)):
    name = validlines[i*3 + 0]
    line1 = validlines[i*3 + 1]
    # line2 = validlines[i*3 + 2] # don't actually need this
    catnum = line1[2:7]
    classification = line1[7]
    intldesign = line1[9:17]

    # write it with comma delimiters
    s2write = [name,catnum,classification,intldesign]
    s2write = ','.join(s2write)
    fw.write(s2write + '\n')

# close file and end
fw.close()