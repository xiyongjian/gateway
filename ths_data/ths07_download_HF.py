# -*- coding: utf-8 -*-
"""
download high frquence

"""

from ctypes import *
from iFinDPy import *

import time
import json
from datetime import datetime

import os
import traceback

from sqlalchemy import create_engine


if False :
    THS_HighFrequenceSequence('600026.SH,600027.SH',
                          'open;high;low;close;avgPrice;volume;amount;change;changeRatio;turnoverRatio;sellVolume;buyVolume;buyAmount;sellAmount',
                          'CPS:0,MaxPoints:50000,Fill:Previous,Interval:1',
                          '2018-04-03 09:15:00',
                          '2018-04-03 10:15:00')

def download_1min(code, dt_from, dt_to) :
    columns = 'open;high;low;close;avgPrice;volume;amount;change;changeRatio;turnoverRatio;sellVolume;buyVolume;buyAmount;sellAmount'
    # options = 'CPS:0,MaxPoints:50000,Fill:Previous,Interval:1'
    options = 'CPS:0,MaxPoints:500000,Fill:Previous,Interval:1'

    print('download 1min, code %s, from %s to %s'%(code, dt_from, dt_to))

    start = datetime.now()
    quotes = THS_HighFrequenceSequence(code, columns, options, dt_from, dt_to);
    data = THS_Trans2DataFrame(quotes)
    end = datetime.now()

    print('download pandas dataframe size : %s'%str(data.shape))

    print("start at : %s"%str(start))
    print("end at   : %s"%str(end))
    using_time_secs = (end-start).total_seconds();
    print("time using : %f seconds"%(using_time_secs))

    return data

if __name__=="__main__":
    print("THS login")
    THS_iFinDLogin("sissi008","677085")

    if False :
        codes = '600026.SH,600027.SH'
        dt_from = '2018-04-03 09:15:00'
        dt_to = '2018-04-03 10:15:00'
    if False :
        THS_HighFrequenceSequence(
            '600028.SH,600029.SH,600030.SH,600031.SH,600033.SH,600035.SH,600036.SH,600037.SH,600038.SH,600039.SH,600048.SH,600050.SH',
            'open;high;low;close;avgPrice;volume;amount;change;changeRatio;turnoverRatio;sellVolume;buyVolume;buyAmount;sellAmount',
            'CPS:0,MaxPoints:50000,Fill:Previous,Interval:1', '2018-04-03 09:15:00', '2018-04-03 15:15:00')

    codes = '600028.SH,600029.SH,600030.SH,600031.SH,600033.SH,600035.SH,600036.SH,600037.SH,600038.SH,600039.SH,600048.SH,600050.SH'
    codes = '600026.SH,600027.SH'
    dt_from = '2018-04-03 09:15:00'
    dt_to = '2018-04-03 15:15:00'
    data = download_1min(codes, dt_from, dt_to)

    print(data.info());
    # print(data)
    print("time length :", len(data['time']))

    THS_iFinDLogout()

    engine = create_engine("mysql+mysqlconnector://ths:ths@127.0.0.1:3306/test");
    data.rename(columns={'thscode': 'code', 'time': 'minute', 'open': 'open_', 'change': 'change_'}, inplace=True)
    data.to_sql(name='stockdata_stage', con=engine, if_exists='append', index=False)

    connection = engine.connect()
    result = connection.execute("replace into stockdata select * from stockdata_stage")
    print("replace into, return : " )

    print("clean stage table")
    result = connection.execute("delete from stockdata_stage")

    print("done.")
