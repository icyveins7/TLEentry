# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 00:21:58 2017

@author: Seororo
"""
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
import ssl
from datetime import datetime
from os import listdir, getcwd
import os.path
import urllib3 # requests doesn't support ftp apparently
import urllib.request # this is for python 3
import pycurl
import io


# This is the 2.11 Requests cipher string.
CIPHERS = (
    'RC4-SHA:ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
    'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:RSA+3DES-EDE-CBC:!aNULL:'
    '!eNULL:!MD5'
)

class MyAdapter(HTTPAdapter):
#    def init_poolmanager(self, *args, **kwargs):
#        context = create_urllib3_context(ciphers=CIPHERS)
#        kwargs['ssl_context'] = context
#        return super().init_poolmanager(*args, **kwargs)
    def init_poolmanager(self, connections, maxsize, block=False):
        context = create_urllib3_context(ciphers=CIPHERS)
        self.poolmanager = PoolManager(num_pools=connections,maxsize=maxsize,block=block,ssl_version=ssl.PROTOCOL_TLSv1,ssl_context=context)

s = requests.Session()
s.mount('https://www.celestrak.com/', MyAdapter())
r = s.get("https://www.celestrak.com/NORAD/elements/geo.txt")

storeDir = os.getcwd()
onlyfiles = [f for f in listdir(storeDir) if (os.path.isfile(os.path.join(storeDir, f)) and f[-4:]=='.txt')] #list the .txt files in the dir
modtimes = [os.path.getmtime(os.path.join(storeDir, f)) for f in onlyfiles]
latesttime = max(modtimes)
latesttime_ind = modtimes.index(latesttime) # find the index of max

latestfile = open(os.path.join(storeDir,onlyfiles[latesttime_ind]),'r') # change this to logic for reading latest file
latestdata = latestfile.read()
latestfile.close()

timenow = str(datetime.now())
filename = timenow.split(':')
filename = filename[0]+'_'+filename[1]+'.txt' # put your path and filename here!


if (r.text.split()==latestdata.split()):
    print('Latest TLE data is already saved!')
else:
    textfile = open(os.path.join(storeDir,filename),'w')
    textfile.write(r.text)
    textfile.close()
    print('Wrote new TLE file!')

#%% logic for the bulletin files
bullfilename = timenow.split(':')
bullfilename = bullfilename[0]+'_'+bullfilename[1]+'finals.daily' # for bulletin filename

onlybullfiles = [f for f in listdir(storeDir) if (os.path.isfile(os.path.join(storeDir, f)) and f[-12:]=='finals.daily')] #list the bulletin files in the dir
modbulltimes = [os.path.getmtime(os.path.join(storeDir, f)) for f in onlybullfiles]

if len(modbulltimes) > 0:
    latestbulltime = max(modbulltimes)
    latestbulltime_ind = modbulltimes.index(latestbulltime) # find the index of max
    
    latestbullfile = open(os.path.join(storeDir,onlybullfiles[latestbulltime_ind]),'r') # change this to logic for reading latest file
    latestbulldata = latestbullfile.read()
    latestbullfile.close()
else:
    latestbulldata = ''

#%% post-Oct 2020 (with login)
# Initialize the cURL connection object
curl = pycurl.Curl()

# Define the url to use
curl.setopt(curl.URL, "https://cddis.nasa.gov/archive/products/iers/" + "finals.daily")

# Set curl to follow redirects, needed to allow user login
curl.setopt(curl.FOLLOWLOCATION, True)

# Set the requirement that cURL use a netrc file found in users home directory (by default, but we change this)
curl.setopt(curl.NETRC,2)

curl.setopt_string(curl.NETRC_FILE, os.path.join(getcwd(), '.netrc'))

# Set the file used to store cookie
curl.setopt(curl.COOKIEJAR, '.cddis_cookies')

print(curl.getinfo(curl.EFFECTIVE_URL))

# Writes the remote file to a new file with the same name
e = io.BytesIO()
curl.setopt(curl.WRITEFUNCTION, e.write)
curl.perform()

if (e.getvalue().decode('UTF-8') == latestbulldata):
    print('Latest bulletin data already saved!')
else:
    f = open(os.path.join(storeDir, bullfilename), 'w')
    f.write(e.getvalue().decode('UTF-8'))
    f.close()
    print('Wrote new bulletin file!')

# Clean up and close the cURL object
curl.close()

# print(e.getvalue().decode('UTF-8'))

#%% pre-Oct 2020
#tt = urllib3.urlopen('ftp://cddis.gsfc.nasa.gov/pub/products/iers/finals.daily') # get the file from ftp server
#tt_text = tt.read()
#tt.close()

# # python 3 version..
# with urllib.request.urlopen('ftp://cddis.gsfc.nasa.gov/pub/products/iers/finals.daily') as tt:
#     tt_text = tt.read() # convert to string in python 3, was byte literal

# if (tt_text.decode('utf-8')==latestbulldata): # add .decode('utf-8') for python3
#     print('Latest bulletin data is already saved!')
# else:
#     bullfile = open(os.path.join(storeDir,bullfilename),'w')
# #    bullfile.write(tt_text)
#     bullfile.write(tt_text.decode('utf-8')) # python 3 version
#     bullfile.close()
#     print('Wrote new bulletin file!')

	
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.ssl_ import create_urllib3_context

# # This is the 2.11 Requests cipher string.
# CIPHERS = (
    # 'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
    # 'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
    # '!eNULL:!MD5'
# )

# class DESAdapter(HTTPAdapter):
    # def init_poolmanager(self, *args, **kwargs):
        # context = create_urllib3_context(ciphers=CIPHERS)
        # kwargs['ssl_context'] = context
        # return super(HTTPAdapter, self).init_poolmanager(*args, **kwargs)

# s = requests.Session()
# s.mount('https://10.192.8.89', DESAdapter())

# my error was gone by adding 'DES-CBC3-SHA' in the CIPHERS string. sigh...