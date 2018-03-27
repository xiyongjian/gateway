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


if __name__=="__main__":
    print("THS login")
    THS_iFinDLogin("sissi008","677085")
    ID=c_int32(0)

    stats = THS_DataStatistics()
    print("stats : ", json.dumps(stats, indent=4))

    stats = THS_DataStatistics()
    print("stats2 : ", json.dumps(stats, indent=4))

    THS_iFinDLogout()
    print("done.")
