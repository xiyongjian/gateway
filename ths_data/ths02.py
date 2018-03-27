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

    start = datetime.now()
    print("THS run query")

    if False :
        quotes = THS_HistoryQuotes('300033.SZ,600000.SH',
                      'open;low;high;close',
                      'period:D,pricetype:1,rptcategory:0,fqdate:1900-01-01,hb:YSHB',
                      '2015-06-23','2016-06-23')
    quotes = THS_HighFrequenceSequence('300033.SZ',
                                       'open;high;low;close;amt',
                                       'CPS:0,MaxPoints:50000,Fill:Previous,Interval:1',
                                       '2017-05-15 09: 30:00','2017-05-15 16:00:00')
    print("return quotes, type : %s"%str(type(quotes)))
    data = THS_Trans2DataFrame(quotes)
    print("trans to data, type : %s"%str(type(data)))
    # print("trans to data, info : %s"%str(info(data)))
    print("data index : ", data.index)
    print("data : ", data)

    print("THS run query, done")
    end = datetime.now()

    print("start at : %s"%str(start))
    print("end at   : %s"%str(end))
    print("time using : " + str(end - start))
    print("time using : " + str((end-start).total_seconds()))
    print("time using : %f"%(end-start).total_seconds())
    print("time using type : " + str(type(end - start)))

    THS_iFinDLogout()
    print("done.")
