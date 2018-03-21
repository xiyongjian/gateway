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

end = None

def OnCallback(puser,ID,sResult,length,errorcode,reserve):
    print(sResult)
    print("OnCallback(), type of sResult : %s"%str(type(sResult)))
    print("OnCallback(), sResult : %s"%str(sResult))
    print("result : %s"%json.dumps(json.loads(sResult), indent=4))
    global end
    end = datetime.now()
    return 0
CALLBACKRESULT=CFUNCTYPE(c_int,c_void_p,c_int32,c_wchar_p,c_int32,c_int32,c_int32)
pCallbackFunc=CALLBACKRESULT(OnCallback)


if __name__=="__main__":
    print("THS login")
    # THS_iFinDLogin("ifind_e001","ifinde001")
    THS_iFinDLogin("sissi008","677085")
    ID=c_int32(0)

    start = datetime.now()

    print("THS run query")
    # THS_AsyHighFrequenceSequence('300033.SZ','open;high;low;close','CPS:0,MaxPoints:50000,Fill:Previous,Interval:1','2017-03-09 09:30:00','2017-03-09 09:31:00',pCallbackFunc,c_void_p(0),byref(ID))
    # THS_AsyRealtimeQuotes('600000.SH,600004.SH','close;open;high;low;change','pricetype:1',pCallbackFunc,c_void_p(0),byref(ID))
    # THS_AsyHistoryQuotes('600000.SH,600004.SH,600005.SH','lastclose;open;low','period:D,pricetype:1,rptcategory:0,fqdate:1900-01-01,hb:YSHB','2016-02-23','2017-02-23',pCallbackFunc,c_void_p(0),byref(ID))
    THS_AsyHistoryQuotes('600000.SH,600004.SH,600005.SH','lastclose;open;low','period:D,pricetype:1,rptcategory:0,fqdate:1900-01-01,hb:YSHB','2016-02-13','2016-02-20',pCallbackFunc,c_void_p(0),byref(ID))
    #THS_AsyBasicData('600000.SH,600004.SH,600005.SH','ths_gpdm_stock','',pCallbackFunc,c_void_p(0),byref(ID))
    #THS_AsyDateSequence('600000.SH,600004.SH,600005.SH','stockname;stockcode;thscode','CPS:0,Days:Tradedays,Fill:Previous,Interval:D,Currency:ORIGINAL','2017-01-23','2017-02-23',pCallbackFunc,c_void_p(0),byref(ID))
    #THS_AsyDataPool('block','2017-02-23;001005260','date:Y,security_name:Y,thscode:Y',pCallbackFunc,c_void_p(0),byref(ID))
    #THS_AsyEDBQuery('M001620326;M002822183;M002834227','2010-02-23','2017-02-23',pCallbackFunc,c_void_p(0),byref(ID))

    print("sleep 2 seconds")
    time.sleep(2)

    print("start at : %s"%str(start))
    print("end at   : %s"%str(end))
    # print("time using : %f"%(end.microsecond - start.microsecond))
    print("time using : " + str(end - start))
    print("time using : " + str((end-start).total_seconds()))
    print("time using : %f"%(end-start).total_seconds())
    print("time using type : " + str(type(end - start)))

    THS_iFinDLogout()
    print("done.")

