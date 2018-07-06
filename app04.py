'''
run single stock (china A-stock) and try to use watch list, strategy framework
base on app03
using data2, with improved bar data
select from database
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

    log.info("totoal symbols/stocks {}".format(context.symbols))
    log.info("list of symbols/stockes : {}".format(context.symbols)) \

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
        if sn == 99 : # or (sn > 120 and sn<130) :       # for debug/testing only
            # context.batch.dump();
            print("history 5 : \n%s"%bar_data.history(context.symbols, 'close', 5, '1m'))

##########################################################################################
# user defined function to prepare and using data/watchlists
##########################################################################################

_global_panel = None
def set_global_panel(p) :
    global _global_panel
    _global_panel = p

def get_global_panel() :
    return _global_panel

# list 'a' is initial one, always includes all symbols
def create_watchlists(symbols) :
    wls = watchlists.WatchLists(tickers=symbols, watchlist_names=['W0', 'W1', 'W2'], window_size=20)
    return wls

def create_data(symbols) :
    d = data.Data(tickers=symbols, windows_size=20)
    d.create_factor(name="sma5")

    # build bar for "close",
    d.create_bar("close", df)
    return d

def prepare_data_and_watchlists(context, bar_data) :
    sn = context.sn
    log.info("prepare, sn {}".format(sn))

    data = context.data
    wls = context.watchlists
    symbols = context.symbols

    wls.wl_set_sn(sn)

    data.prepare(sn, bar_data)

    ######### prepare factors ##################
    if sn > 5 :    # if using history data, leave some blank at beginning
        log.info("prepare, sma5, start");
        W0 = wls.wl_get_until("W0", 0)
        sma5 = data.history(W0, 'close', bar_count=5, frequency="1m").mean()
        data.get_factor("sma5").set(W0, sma5)
        log.info("prepare, sma5, done");
    pass

# filter list a (list of object), based on condition c (list of boolean)
def filter(a, c) :
    return [i for (i, cond) in zip(a, c) if cond]

# d: data, wls: watchlists
def do_strategy(sn, symbols, data, wls) :
    log.info("strategy, sn {}".format(sn))
    if sn == 10 :
        log.info("data sma5(sn) [:5] : %r"%data.get_factor("sma5").get(tickers=symbols[:5]))
        log.info("data get(sma5, symbols[:5]) : %r"%data.get(name="sma5", tickers=symbols[:5]))
        log.info("data get_range(close, symbols[:5], -2) : %r"%data.get_range(name="close", tickers=symbols[:5], pos_from=-2))
        log.info("watchlist 'W0' : %r"%wls.wl_get("W0"))

    if sn > 5 :  # consider hitory data
        if True :   # W0 -> w1
            log.info("strategy, get W0")
            W0 = wls.wl_get_until("W0")

            log.info("strategy, get c")
            c = data.get(name="close", tickers=W0)
            log.info("strategy, get c1")
            c1 = data.get(name="close", tickers=W0, pos=-1)
            log.info("strategy, get sma5")
            sma5 = data.get(W0, "sma5")
            # condition

            log.info("strategy, compare c/c1/sma5")
            s = (c > c1) & (c1 > sma5)
            W1 = filter(W0, s)
            log.info("W0 -> W1[:5] : {}".format(W1[:5]))
            wls.wl_set("W1", W1)
            # print(wls)

        if True :   # W1 -> W2
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
        panel = utils.create_data_panel("2018-03-28 09:30:00", "2018-04-03 15:00:00")
        log.info("get panal shape : {}".format(panel.shape))
    elif False:
        codes = ['000001.SZ', '000002.SZ', '000004.SZ', '000005.SZ', '000006.SZ', '000007.SZ', '000008.SZ', '000009.SZ', '000010.SZ', '000011.SZ', '000012.SZ']
        panel = utils.create_data_panel_with_codes("2018-04-03 09:30:00", "2018-04-04 09:31:00", codes)
        log.info("get panal shape : {}".format(panel.shape))
    else :
        panel_file = "db_panel.h5"
        log.info("read panale from hdf5 file {} start".format(panel_file))
        panel = pd.read_hdf(panel_file)
        log.info("read panale from hdf5 file {} done".format(panel_file))
    datetime_index = panel.major_axis
    set_global_panel(panel)

    global stocks
    stocks = list(panel.items)
    log.info("total {} stocks in panel, shape {}".format(len(stocks), panel.shape))
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
