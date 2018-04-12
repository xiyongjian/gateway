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

import sys
sys.path.append('..')
# from config import config
import config


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


def load_data(codes, dt_from, dt_to) :
    print("load_data codes : " + codes)
    print("load_data dt_from : " + dt_from)
    print("load_data dt_to : " + dt_to)

    data = download_1min(codes, dt_from, dt_to)

    print(data.info());
    # print(data)
    print("time length :", len(data['time']))

    print("create db connection to " + config.config['db_url'])
    engine = create_engine(config.config['db_url'])
    # engine = create_engine("mysql+mysqlconnector://ths:ths@127.0.0.1:3306/test");
    data.rename(columns={'thscode': 'code', 'time': 'minute', 'open': 'open_', 'change': 'change_'}, inplace=True)
    data.to_sql(name='stockdata_stage', con=engine, if_exists='append', index=False)

    connection = engine.connect()
    result = connection.execute("replace into stockdata select * from stockdata_stage")
    print("replace into, return : ")

    print("clean stage table")
    result = connection.execute("delete from stockdata_stage")


if __name__=="__main__":
    print("try to use db connection " + config.config['db_url'])
    print("THS login")
    # ret = THS_iFinDLogin("sissi008","677085")
    # ret = THS_iFinDLogin("qhfh001","429742")
    ret = THS_iFinDLogin("qhfh002","891111")
    print("ths login return : " + str(ret))

    if False :
        codes = '600026.SH,600027.SH'
        dt_from = '2018-04-03 09:15:00'
        dt_to = '2018-04-03 10:15:00'
    if False :
        THS_HighFrequenceSequence(
            '600028.SH,600029.SH,600030.SH,600031.SH,600033.SH,600035.SH,600036.SH,600037.SH,600038.SH,600039.SH,600048.SH,600050.SH',
            'open;high;low;close;avgPrice;volume;amount;change;changeRatio;turnoverRatio;sellVolume;buyVolume;buyAmount;sellAmount',
            'CPS:0,MaxPoints:500000,Fill:Previous,Interval:1', '2018-04-03 09:15:00', '2018-04-03 15:15:00')

    dt_from = '2018-04-11 09:30:00'
    dt_to = '2018-04-11 15:00:00'

    if True :
        codes = '600028.SH,600029.SH,600030.SH,600031.SH,600033.SH,600035.SH,600036.SH,600037.SH,600038.SH,600039.SH,600048.SH,600050.SH'
        load_data(codes, dt_from, dt_to)

    if False :
        codes = '600026.SH,600027.SH'
        load_data(codes, dt_from, dt_to)

        codes = '600030.SH,600031.SH'
        load_data(codes, dt_from, dt_to)

        codes = '600033.SH,600035.SH'
        load_data(codes, dt_from, dt_to)

        codes = '600036.SH,600037.SH'
        load_data(codes, dt_from, dt_to)

        codes = '600038.SH,600039.SH'
        load_data(codes, dt_from, dt_to)

        codes = '600048.SH,600050.SH'
        load_data(codes, dt_from, dt_to)

    if False :
        data = download_1min(codes, dt_from, dt_to)

        print(data.info());
        # print(data)
        print("time length :", len(data['time']))

        THS_iFinDLogout()
        print("ths logout")

        print("create db connection to " + config.config['db_url'])
        engine = create_engine(config.config['db_url'])
        # engine = create_engine("mysql+mysqlconnector://ths:ths@127.0.0.1:3306/test");
        data.rename(columns={'thscode': 'code', 'time': 'minute', 'open': 'open_', 'change': 'change_'}, inplace=True)
        data.to_sql(name='stockdata_stage', con=engine, if_exists='append', index=False)

        connection = engine.connect()
        result = connection.execute("replace into stockdata select * from stockdata_stage")
        print("replace into, return : " )

        print("clean stage table")
        result = connection.execute("delete from stockdata_stage")

    THS_iFinDLogout()
    print("ths logout")
    print("done.")
