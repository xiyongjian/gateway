# -*- coding: utf-8 -*-
"""
download data (1 minutes)

"""

from ctypes import *
from iFinDPy import *

import time
import json
from datetime import datetime

import os
import traceback

profile = 'e:\\tmp\\ths_profile_1min.log'

def download_1min(code, year, folder) :
    print('download 1min, code %s, year %s'%(code, year))

    csv_file = os.path.join(folder, code + "." + year + ".1m.csv")
    print('download&write to file %s'%csv_file)
    print('code %s, from %s to %s'%(code, year + '-01-01 05:00:00', year + '-12-31 23:00:00'))

    start = datetime.now()
    quotes = THS_HighFrequenceSequence(code,
                                       'open;high;low;close;amt',
                                       'CPS:0,MaxPoints:500000,Fill:Previous,Interval:1',
                                       year + '-01-01 05:00:00', year + '-12-31 23:00:00')
    data = THS_Trans2DataFrame(quotes)
    end = datetime.now()
    print('download pandas dataframe size : %s'%str(data.shape))

    print('data write to file %s'%csv_file)
    data.to_csv(csv_file)

    print("start at : %s"%str(start))
    print("end at   : %s"%str(end))
    using_time_secs = (end-start).total_seconds();
    print("time using : %f seconds"%(using_time_secs))

    shape = data.shape

    print('%s; %s; %s; %d points; %f secs\n'%(year, code, str(shape), shape[0] * 5, using_time_secs))
    with open(profile, 'a+') as f :
        f.write('%s; %s; %s; %d points; %f secs\n'%(year, code, str(shape), shape[0] * 5, using_time_secs))
    return data

if __name__=="__main__":
    print("THS login")
    THS_iFinDLogin("sissi008","677085")
    ID=c_int32(0)

    folder = 'e:\\tmp'
    year = '2016'
    code = '300033.SZ'
    code = '600000.SH'

    for i in range(2000, 2018) :
        year = str(i)
        try :
            data = download_1min(code, year, folder)
        except :
            print(traceback.format_exc())
            print("Unexpected error:", sys.exc_info()[0])

    THS_iFinDLogout()
    print("done.")
