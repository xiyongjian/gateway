'''
Data access interface, for bardata(gateway) and all kind of factors
with factor & bar data
'''

import pandas as pd
import numpy as np

import sys
import logbook
log = logbook.Logger("Data.py")

class Factor :
    def __init__(self, name, tickers, window_size, sn = 0) :
        self.name = name
        self.window_size = window_size
        self.rolling_size = window_size * 2 + 2

        self.tickers = tickers
        columns = sorted(self.tickers)

        index = range(sn, sn + self.rolling_size)
        self.df = pd.DataFrame(np.zeros((len(index), len(columns))), index = index, columns = columns)
        self.current_sn = sn

    def __str__(self):
        s = [];
        s.append("Factor : %s, window_size : %d, rolling_size : %d"%(self.name, self.window_size, self.rolling_size))
        s.append("  current_sn : %d(idx %d), # of tickers : %d, df frame shape : %s" \
                 %(self.current_sn, self.df.index.get_loc(self.current_sn), len(self.tickers), self.df.shape))
        return "\n".join(s)

    def full_string(self):
        s = []
        s.append(str(self))
        s.append("tickers : %s"%self.tickers)
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
        assert set(tickers).issubset(set(self.tickers)), "tickers %s must be subset of tickers %s"%(tickers, self.tickers)
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
        self.assert_sn(to_sn-1)
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

class Bar :
    def __init__(self, name, df, base_sn = 0) :
        self.name = name
        self.tickers = df.columns
        self.df = df
        self.base_sn = base_sn
        self.current_sn = base_sn
        self.window_size = len(self.df.index)

    def __str__(self):
        s = [];
        s.append("Bar : {}, base_sn {}, df frame shape {}".format(self.name, self.base_sn, self.df.shape))
        return "\n".join(s)

    def full_string(self):
        s = []
        s.append(str(self))
        s.append("tickers : %s"%self.tickers)
        s.append("df(DataFrame) : %s"%self.df)
        return "\n".join(s)

    def set_sn(self, sn) :
        self.assert_sn(sn)
        self.current_sn = sn
        idx = self.current_sn - self.base_sn

    def assert_sn(self, sn) :
        assert sn >= self.base_sn, "sn %d must >= current sn %d"%(sn, self.base_sn)
        assert sn < self.base_sn + self.window_size, "sn %d must < base sn %d + window size %d"%(sn, self.base_sn, self.window_size)
        pass

    def assert_tickers(self, tickers):
        assert set(tickers).issubset(set(self.tickers)), "tickers %s must be subset of tickers %s"%(tickers, self.tickers)
        pass

    # alwasy put to position : current_sn
    def set(self, tickers, values, sn = None) :
        assert False, "should not call this method in Bar"

    def get(self, tickers, sn = None):
        if sn == None :
            sn = self.current_sn
        self.assert_tickers(tickers)
        self.assert_sn(sn)
        idx = sn - self.base_sn
        return self.df.iloc[idx][tickers]

    def get_range(self, tickers, from_sn, to_sn) :
        self.assert_tickers(tickers)
        self.assert_sn(from_sn)
        self.assert_sn(to_sn-1)
        idx_from = from_sn - self.base_sn
        idx_to = to_sn - self.base_sn
        # df = self.df.iloc[idx_from:idx_to][tickers]
        # log.info("df : {}".format(df))
        # return self.df.iloc[idx_from:idx_to][tickers]
        return self.df.iloc[idx_from:idx_to][list(tickers)]
        pass

    def roll(self) :
        assert False, "should not call this method in Bar"

class Data :
    def __init__(self, tickers, window_size) :
        self.tickers = tickers
        self.current_sn = 0
        self.factors = {}   # factors include bars
        self.window_size = window_size

    def set_sn(self, sn):
        self.current_sn = sn
        # todo prepare factors, calcuation, and set current_idx -> sn (assert)
        for n, f in self.factors.items() :
            f.set_sn(sn)

    def __str__(self):
        s = []
        s.append("Data, # of tickers : %d, # of factors : %d"%(len(self.tickers), len(self.factors)))
        s.append("      window_size : %d, current_sn : %d"%(self.window_size, self.current_sn))
        for k in self.factors :
            s.append(str(self.factors[k]))
        return "\n".join(s)

    def full_string(self) :
        s = []
        s.append("Data, # of tickers : %d, # of factors : %d"%(len(self.tickers), len(self.factors)))
        s.append("      window_size : %d, current_sn : %d"%(self.window_size, self.current_sn))
        for k in self.factors :
            s.append(self.factors[k].full_string())
        return "\n".join(s)

    def create_factor(self, name, window_size = None):
        if window_size == None :
            window_size = self.window_size
        factor = Factor(name, self.tickers, window_size, self.current_sn)
        self.add_factor(factor)

    def add_factor(self, factor):
        self.factors[factor.name] = factor
        factor.set_sn(self.current_sn)

    def add_bar(self, bar) :
        self.factors[bar.name] = bar
        bar.set_sn(self.current_sn)

    # get tickers' name data of len, at pos (0, -1, -2...)
    def get(self, name, tickers, pos = 0, len = 1):
        pos_to = pos
        pos_from = pos - len + 1
        assert pos_from <= 0, "pos_from %d must <= 0"%pos_from
        assert pos_to <= 0, "pos_to %d must <= 0"%pos_to
        assert pos_from <= pos_to, "pos_from %d must <= pos_to %d"%(pos_from, pos_to)
        if len == 1 :
            return self.factors[name].get(tickers, self.current_sn + pos)
        else :
            return self.factors[name].get_range(tickers, self.current_sn + pos_from, self.current_sn + pos_to+1)

    def set(self, name, tickers, value, pos = 0):
        assert pos <= 0, "pos %d must <= 0"%pos
        self.factors[name].set(tickers, value, self.current_sn + pos)

def test_01() :
    log.info("test_01() {}".format("no args"))

    tickers = ['a', 'b', 'c', 'd']
    data = Data(tickers, 3)
    log.info("data : \n%s"%data)

    data.create_factor("sma50", 3)
    log.info("after create factor sma50, 10 : \n{}".format(data))

    data.set_sn(1);
    data.set("sma50", tickers, [1,2,3,4])
    log.info("data : \n%s"%data.full_string())

    df = pd.DataFrame(np.random.rand(10, 4), columns = tickers)
    bar = Bar("price", df)
    data.add_bar(bar)
    log.info("after add bar, data : \n%s"%data.full_string())
    pass

def test_02() :
    pass

if __name__ == "__main__" :
    handler = logbook.StreamHandler(sys.stdout, level=logbook.DEBUG)
    handler.formatter.format_string = '{record.time}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno}|{record.message}'
    handler.push_application()

    test_01()

