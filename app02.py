'''
run single stock (china A-stock) and try to use watch list, strategy framework
'''

from collections import OrderedDict
from gateway import TradingAlgorithm

import pandas as pd
from gateway.api import (order, symbol)
import numpy as np
import re

# from cn_calendar.gateway.exchange_calendar_shsz import SHSZExchangeCalendar
from cn_stock_holidays.gateway.exchange_calendar_shsz import SHSZExchangeCalendar

import sys
import logbook

# local import
import utils

# logging setup
if True :
    handler = logbook.StreamHandler(sys.stdout, level=logbook.DEBUG)
    handler.formatter.format_string = '{record.time}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno}|{record.message}'
    handler.push_application()
    # or using this : with handler.applicationbound():
    log = logbook.Logger("app01")

if False:    # hacking for url missing
    from pandas_datareader.google.daily import GoogleDailyReader
    @property
    def url(self):
        print("call @property get url, %s, %s" % (self, type(self)))
        return 'http://finance.google.com/finance/historical'
    GoogleDailyReader.url = url

stocks = ['600183', '600184', '601336']

def initialize(context):
    context.symbols = [symbol(s) for s in stocks]
    context.sn = 0
    pass

start_dt = None;
sn = 0;
end_dt = None;
def handle_data(context, bar_data):
    global start_dt, end_dt, sn

    sn = context.sn
    sn = sn + 1
    context.sn = sn

    if start_dt is None :
        start_dt = bar_data.current_dt
    end_dt = bar_data.current_dt

    if sn < 25  or sn > 1000:
        return

    log.info("-------- SN %d -----------, date : %s"%(sn, bar_data.current_dt))

    if True :
        if sn == 99 or (sn > 120 and sn<130) :       # for debug/testing only
            # context.batch.dump();
            print("history 5 : \n%s"%bar_data.history(context.symbols, 'close', 5, '1m'))

if __name__ == '__main__' :
    log.info("app01, main, entering")

    ## replace this part with database retrieving
    #  table : clock       sn (1,2,3,4....., integer), datetime (minute)
    #  select from clock and write to data/clock.csv (to generate clock)
    #       select id, minute from clock
    # select from stockdata,
    #       select * from stockdata where minute in (select minute from clock)
    #           order by code, minute
    #
    log.info('load panel')
    panel = utils.create_data_panel("2018-04-03 09:20:00", "2018-04-04 09:45:00")
    datetime_index = panel.major_axis

    global stocks
    stocks = list(panel.items)
    log.info("setup stocks list : " + str(stocks))

    cn_cal = SHSZExchangeCalendar()
    panel.major_axis = panel.major_axis.tz_localize(cn_cal.tz)
    algo_obj = TradingAlgorithm(initialize=initialize, handle_data=handle_data,
                                trading_calendar = cn_cal,
                                data_frequency = 'minute',
                                clock_dt_index=datetime_index)
    # clock_file = "data/clock.csv")

    log.info('run algorithm')
    perf_manual = algo_obj.run(panel)
    if False :
        print(perf_manual)

    if False :
        import pickle
        file = "e:\\perf.p"
        log.info("write performance to pickle : %s"%file)
        pickle.dump(perf_manual, open(file, 'wb'))

    log.info("total sn %d, start at %s, end at %s"%(sn, str(start_dt), str(end_dt)))
    log.info('done')
