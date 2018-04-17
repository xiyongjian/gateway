# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:57:58 2017

@author: viruser
"""

from ctypes import *
from iFinDPy import *

import time
import json
from datetime import datetime

sys.path.append('..')
import config

_users = config.get_users()
_passwords = config.get_passwords()

def check(user, password) :
    print("THS login, user %s, password %s"%(user, password))
    ## THS_iFinDLogin("sissi008","677085")
    printret = THS_iFinDLogin(user, password)
    ret = THS_iFinDLogin(user, password)
    print("login return : %r"%ret)

    stats = THS_DataStatistics()
    print("stats : ", json.dumps(stats, indent=4))

    stats = THS_DataStatistics()
    print("stats2 : ", json.dumps(stats, indent=4))

    THS_iFinDLogout()
    print("done.")

if __name__=="__main__":
    print("start")
    check(_users[0], _passwords[0])
    check(_users[1], _passwords[1])
    print("done")

