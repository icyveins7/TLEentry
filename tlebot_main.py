# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 19:31:32 2019

@author: Seo
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
#from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import datetime as dt
import re
import os

import time
import ntpath
import pytz

# getTLE imports
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
# ============

utc=pytz.UTC

time_bot_started = dt.datetime.utcnow().timestamp()

# open file with telegram token
telegramtokenpath = os.path.join(ntpath.split(os.path.realpath(__file__))[0],'tlebot.token')
with open(telegramtokenpath,'r') as f:
    teletoken = f.readline().strip()

# # open file with chat id of me
# selfidpath = ntpath.split(os.path.realpath(__file__))[0] + '\\self.id'
# with open(selfidpath,'r') as f:
#     selfid = f.readline()[:-1]


updater = Updater(token=teletoken, use_context=True)
dispatcher = updater.dispatcher
jobQueue = updater.job_queue

chatIDlist = []


def checkCommandIsOld(message):
    print('Datetime message was received was '+str(message.date))
    if message.date.timestamp() <= time_bot_started:
        return True
    else:
        return False
    
def status(update, context):
    if not checkCommandIsOld(update.message):
        timeNow = dt.datetime.utcnow().timestamp()
        context.bot.send_message(chat_id=update.message.chat_id,
                         text='This bot was started at UTC'+str(dt.datetime.fromtimestamp(time_bot_started)))

def downloadLatest(update, context):
    if not checkCommandIsOld(update.message):
        timenow = str(datetime.now())
        storeDir = os.getcwd()
        onlyfiles = [f for f in listdir(storeDir) if (os.path.isfile(os.path.join(storeDir, f)) and f[-4:]=='.txt')] #list the .txt files in the dir
        modtimes = [os.path.getmtime(os.path.join(storeDir, f)) for f in onlyfiles]
        latesttime = max(modtimes)
        latesttime_ind = modtimes.index(latesttime) # find the index of max
        
        bullfilename = timenow.split(':')
        bullfilename = bullfilename[0]+'_'+bullfilename[1]+'finals.daily' # for bulletin filename
        
        onlybullfiles = [f for f in listdir(storeDir) if (os.path.isfile(os.path.join(storeDir, f)) and f[-12:]=='finals.daily')] #list the bulletin files in the dir
        modbulltimes = [os.path.getmtime(os.path.join(storeDir, f)) for f in onlybullfiles]
        latestbulltime_ind = modbulltimes.index(max(modbulltimes))
        
        context.bot.send_message(chat_id=update.message.chat_id,
                         text='Please wait while we are uploading the latest TLE file..')
        context.bot.sendDocument(chat_id=update.message.chat_id, document=open(os.path.join(storeDir,onlyfiles[latesttime_ind]), 'rb'))
        context.bot.send_message(chat_id=update.message.chat_id,
                         text='Please wait while we are uploading the latest bulletin file..')
        context.bot.sendDocument(chat_id=update.message.chat_id, document=open(os.path.join(storeDir,onlybullfiles[latestbulltime_ind]), 'rb'))

def getTLE(context: CallbackContext):
    print('Initiated GetTLE job')
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
    
    # logic for the bulletin files
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
    
    # post-Oct 2020 (with login)
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
    


status_handler = CommandHandler('status', status)
dispatcher.add_handler(status_handler)
dlLatest_handler = CommandHandler('dl', downloadLatest)
dispatcher.add_handler(dlLatest_handler)

getTLEjob = jobQueue.run_repeating(getTLE, interval=60*60*12, first=10)

updater.start_polling()
updater.idle()