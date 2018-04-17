'''
data access interface, for bardata(gateway) and all kind of factors
'''

import pandas as pd
import numpy as np

import sys
import logbook
log = logbook.Logger("data.py")

class Factor :
    def __init__(self, name, symbols, window_size, sn = 0) :
        self.name = name
        self.window_size = window_size
        self.rolling_size = window_size * 2 + 2

        self.symbols = symbols
        columns = sorted(self.symbols)

        index = range(sn, sn + self.rolling_size)
        self.df = pd.DataFrame(np.zeros((len(index), len(columns))), index = index, columns = columns)
        self.current_sn = sn

    def __str__(self):
        s = [];
        s.append("Factor : %s, window_size : %d, rolling_size : %d"%(self.name, self.window_size, self.rolling_size))
        s.append("  current_sn : %d(idx %d), # of symbols : %d, df frame shape : %s" \
                 %(self.current_sn, self.df.index.get_loc(self.current_sn), len(self.symbols), self.df.shape))
        return "\n".join(s)

    def full_string(self):
        s = []
        s.append(str(self))
        s.append("symbols : %s"%self.symbols)
        s.append("df(DataFrame) : %s"%self.df)
        return "\n".join(s)

    def set_sn(self, sn) :
        assert sn >= self.current_sn, "sn %d must >= current sn %d"%(sn, self.current_sn)
        self.current_sn = sn
        self.assert_sn(sn)
        assert sn in self.df.index, 'sn %d must in df.index %s'%(sn, self.df.index)
        idx = self.df.index.get_loc(self.current_sn)
        if idx >= self.rolling_size - 1 :
            self.roll()

    def assert_sn(self, sn) :
        assert sn + self.window_size > self.current_sn and sn <= self.current_sn, \
            "sn %d must be within current_sn %d 's window %d"%(sn, self.current_sn, self.window_size)
        pass

    def assert_tickers(self, tickers):
        assert set(tickers).issubset(set(self.symbols)), "tickers %s must be subset of symbols %s"%(tickers, self.symbols)
        pass

    # alwasy put to position : current_sn
    def set(self, tickers, values, sn = None) :
        if sn == None :
            sn = self.current_sn
        self.assert_sn(sn)
        self.df.loc[self.current_sn, tickers] = values

    def get(self, tickers, sn = None):
        if sn == None :
            sn = self.current_sn
        self.assert_tickers(tickers)
        self.assert_sn(sn)
        return self.df.loc[sn, tickers]

    def get_range(self, tickers, from_sn, to_sn) :
        self.assert_tickers(tickers)
        self.assert_sn(from_sn)
        self.assert_sn(to_sn)
        return self.df.loc[from_sn:to_sn, tickers]
        pass

    def roll(self) :
        idx = self.df.index.get_loc(self.current_sn)
        if idx > self.window_size :
            columns = self.df.columns
            base_sn = self.current_sn - self.window_size + 1
            index = range(base_sn, base_sn + self.rolling_size)
            df = pd.DataFrame(np.zeros((len(index), len(columns))), index = index, columns = columns)
            df.loc[base_sn:self.current_sn] = self.df.loc[base_sn:self.current_sn]
            self.df = df
        else :
            log.info("skip rolling, current_sn %d, idx %d must > windows size %d"%(self.current_sn, idx, self.window_size))

class Data :
    def __init__(self, symbols, windows_size) :
        self.symbols = symbols
        self.current_sn = 0
        self.factors = {}
        self.data = None
        self.window_size = windows_size

    def prepare(self, sn, data):
        self.current_sn = sn
        self.data = data
        # todo prepare factors, calcuation, and set current_idx -> sn (assert)
        for n, f in self.factors.items() :
            f.set_sn(sn)

    def __str__(self):
        s = []
        s.append("Data, # of symbols : %d, # of factors : %d"%(len(self.symbols), len(self.factors)))
        s.append("      window_size : %d, current_sn : %d"%(self.window_size, self.current_sn))
        for k in self.factors :
            s.append(str(self.factors[k]))
        return "\n".join(s)

    def create_factor(self, name, window_size = None):
        if window_size == None :
            window_size = self.window_size
        factor = Factor(name, self.symbols, window_size, self.current_sn)
        self.factors[name] = factor

    def get_factor(self, name) :
        assert name in self.factors, "name %s must be in factors %s"%(name, self.factors.keys())
        return self.factors[name]

    def history(self, tickers, name, n, frequency='1m', until = None):
        if until == None :
            until = self.current_sn
        if name in self.factors :
            pass
        else :
            return self.data.history(tickers, name, n, frequency)

    def current(self, tickers, name):
        if name in self.factors :
            pass
        else :
            return self.data.current(tickers, name)

    def get(self, tickers, name, pos = 0):
        assert pos <= 0, "pos %d must <= 0"%pos
        if name in self.factors :
            return self.factors[name].get(tickers, self.current_sn + pos)
        else :
            data = self.get(tickers, name, pos, 0)
            return data.loc[0, tickers]

    def get_range(self, tickers, name, pos_from, pos_to = 0):
        assert pos_from <= 0, "pos_from %d must <= 0"%pos_from
        assert pos_to <= 0, "pos_to %d must <= 0"%pos_to
        assert pos_from <= pos_to, "pos_from %d must <= pos_to %d"%(pos_from, pos_to)
        if name in self.factors :
            return self.factors[name].get_range(tickers, self.current_sn + pos_from, self.current_sn + pos_to)
        else :
            # example from, to : -1, 0
            d = self.data.history(tickers, name, -pos_from-1)
            return d.loc[0:pos_to - pos_from]
        pass


def test_general() :
    symbols = ['a', 'b', 'c', 'd']
    data = Data(symbols)
    log.info("data : %s"%data)

    data.create_factor("sma50", 10)
    log.info("after create factor sma50, 10 : %s"%data)

    factor = data.get_factor("sma50")
    log.info("before set factor sma50 values : %s"%factor.full_string())
    factor.set_sn(1)
    factor.set(['a', 'c'], [99, 11])
    log.info("after set factor sma50 values : %s"%factor.full_string())

    factor.set_sn(5)
    factor.set(['a', 'b'], [99, 44])
    log.info("get 1 'a' : %s"%factor.get(1, ['a']))
    log.info("after set factor sma50 at 5 : %s"%factor.full_string())
    pass

def test_factor_rolling() :
    symbols = ['a', 'b', 'c', 'd']
    data = Data(symbols)
    log.info("data : \n%s"%data)

    data.create_factor("sma50", 5)
    log.info("after create factor sma50, 10 : \n%s"%data)

    factor = data.get_factor("sma50")
    log.info("before set factor sma50 values : \n%s"%factor.full_string())
    factor.set_sn(1)
    factor.set(['a', 'c'], [99, 11])
    factor.set_sn(6)
    factor.set(['a', 'b'], [99, 23])
    factor.set_sn(7)
    factor.set(['d', 'c'], [88, 109])
    factor.set_sn(8)
    factor.set(['a', 'd'], [66, 1])
    factor.set_sn(11)
    factor.set(['a', 'c'], [66, 99])
    log.info("after set factor sma50 values : %s"%factor.full_string())

    factor.roll()
    log.info("after rolling : %s"%factor.full_string())

    log.info("before rolling : %s"%factor.full_string())
    factor.set_sn(11)
    factor.set(['a', 'b', 'd', 'c'], [1,2,3,4])
    factor.set_sn(12)
    factor.set(['a', 'b', 'd', 'c'], [11,2,3,4])
    factor.set_sn(14)
    factor.set(['a', 'c', 'd', 'b'], [1,2,3,4])
    factor.roll()
    log.info("after rolling : %s"%factor.full_string())

    log.info("factor.get(['a', 'b'] : %s"%factor.get(['a', 'b']))
    log.info("factor.get(['a', 'b'], 10 : %s"%factor.get(['a', 'b'], 10))

def test_set_get() :
    symbols = ['a', 'b', 'c', 'd']
    data = Data(symbols, 6)
    log.info("data : \n%s"%data)

    data.create_factor("sma50", 5)
    log.info("after create factor sma50, 10 : \n%s"%data)

    factor = data.get_factor("sma50")
    log.info("before set factor sma50 values : \n%s"%factor.full_string())
    factor.set_sn(1)
    factor.set(['a', 'c'], [10, 11])
    factor.set_sn(3)
    factor.set(['a', 'c'], [30, 33])
    factor.set_sn(5)
    factor.set(['a', 'c'], [50, 55])
    factor.set_sn(6)
    factor.set(['a', 'c'], [60, 66])
    log.info("after set factor sma50 values : \n%s"%factor.full_string())

    data.prepare(6, 'abcde')
    log.info("data : \n%s"%data)
    log.info("get sma50 : %s"%(data.get(['a', 'd', 'c'], 'sma50')))
    log.info("get sma50, -4 -2 : %s"%(data.get_range(['a', 'd', 'c'], 'sma50', -4, -2)))
    log.info("get sma50, -5 : %s"%(data.get_range(['a', 'd', 'c'], 'sma50', -4)))
    log.info("get sma50, -5, mean : %s"%(data.get_range(['a', 'd', 'c'], 'sma50', -4).mean()))
    pass

if __name__ == "__main__" :
    handler = logbook.StreamHandler(sys.stdout, level=logbook.DEBUG)
    handler.formatter.format_string = '{record.time}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno}|{record.message}'
    handler.push_application()

    # test_general()
    # test_factor_rolling()
    test_set_get()
