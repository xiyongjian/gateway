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

import data
import watchlists

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
    context.stocks = stocks
    context.symbols = [symbol(s) for s in stocks]
    context.sn = 0

    log.info("list of symbols: %r"%context.symbols)
    log.info("list of codes/stockes : %r"%context.symbols)

    log.info("context.data exists : %r"%hasattr(context, "data"))
    log.info("context.watchlists exists : %r"%hasattr(context, "watchlists"))

    log.info("create data object and watchlist objecrt within context")
    context.data = create_data(context.symbols)
    context.watchlists = create_watchlists(context.symbols);

    log.info("done")
    pass

start_dt = None;
sn = 0;
end_dt = None;
def handle_data(context, bar_data):
    global start_dt, end_dt, sn

    sn = context.sn
    sn = sn + 1
    context.sn = sn

    prepare_data_and_watchlists(context, bar_data)
    do_strategy(sn, context.symbols, context.data, context.watchlists)

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

##########################################################################################
# user defined function to prepare and using data/watchlists
##########################################################################################

# list 'a' is initial one, always includes all symbols
def create_watchlists(symbols) :
    wls = watchlists.WatchLists(tickers=symbols, watchlist_names=['a', 'b', 'c'], window_size=20)
    return wls

def create_data(symbols) :
    d = data.Data(tickers=symbols, windows_size=20)
    d.create_factor(name="sma5")
    return d

def prepare_data_and_watchlists(context, bar_data) :
    sn = context.sn
    d = context.data
    wls = context.watchlists
    symbols = context.symbols

    wls.wl_set_sn(sn)

    d.prepare(sn, bar_data)

    ######### prepare factors ##################
    if sn > 10 :    # if using history data, leave some blank at beginning
        f = d.get_factor("sma5")
        f.set(symbols, [sn] * len(symbols))
    pass

# filter list a (list of object), based on condition c (list of boolean)
def filter(a, c) :
    return [i for (i, cond) in zip(a, c) if cond]

# d: data, wls: watchlists
def do_strategy(sn, symbols, d, wls) :
    if sn == 33 :
        log.info("data sma5(sn) : %r"%d.get_factor("sma5").get(tickers=symbols))

        log.info("data get(sma5, symbols) : %r"%d.get(name="sma5", tickers=symbols))
        log.info("data get_range(close, symbols, -2) : %r"%d.get_range(name="close", tickers=symbols, pos_from=-2))

        log.info("watchlist 'a' : %r"%wls.wl_get("a"))

    if sn > 10 :  # consider hitory data
        if sn == 11 :
            wl_a = wls.wl_get("a")
            c = d.get(name="close", tickers=wl_a)
            c1 = d.get(name="close", tickers=wl_a, pos=-1)
            s = (c > c1)
            log.info("c %r"%c)
            log.info("c1 %r"%c1)
            log.info("s %r"%s)

            selected = filter(wl_a, s)
            log.info("selected symbols : %r"%selected)

            wls.wl_set("b", selected)

            print(wls)
        pass
    pass

##########################################################################################
# app entry, __main__
##########################################################################################
if __name__ == '__main__' :
    if False :
        log.info("in testing block")
        data.test_set_get()
        watchlists.test_general()
        sys.exit(0)


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
    # !! must span > 1 days!!, otherwise got error !!
    if False :
        panel = utils.create_data_panel("2018-04-03 09:30:00", "2018-04-04 09:31:00")
    else :
        codes = ['000001.SZ', '000002.SZ', '000004.SZ', '000005.SZ', '000006.SZ', '000007.SZ', '000008.SZ', '000009.SZ', '000010.SZ', '000011.SZ', '000012.SZ']
        panel = utils.create_data_panel_with_codes("2018-04-03 09:30:00", "2018-04-04 09:31:00", codes)
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

