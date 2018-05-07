'''
copy from gateway, for development

general utility, implement watch lists management
'''

###############################################################################################
# WatchLists Setup & Defines Watch List functions:
# WatchLists is defined for each trading decision, and created when needed while setting up the strategy.
#
# Example:
#
#             watchlist_names              : vector/list of WatchList names provided by user.
#             tickers                                  : pass the list of tickers for the strategy.
#             base_sn               : defines the starting index/step number when list created.
#             window_size               : optional, determines the length of the trading cycle.
###############################################################################################

import sys
import logbook
log = logbook.Logger("watchlists.py")

class WatchList :
    def __init__(self, name):
        self.data = {}      # {sn : { set of tickers } }
        self.name = name
        pass

    def __str__(self) :
        s = []
        s.append("watchlist, type %s, name %s :"%(type(self), self.name))
        for sn in sorted(self.data.keys()) :
            s.append("sn %d, %s"%(sn, sorted(self.data[sn])))
        return '\n'.join(s)

    def add(self, sn, tickers) :
        if sn in self.data :
            self.data[sn].update(tickers)
        else :
            self.data[sn] = set(tickers)
        pass

    def set(self, sn, tickers) :
        self.data[sn] = set(tickers)
        pass

    def remove(self, sn, tickers) :
        assert sn in self.data or set(tickers) - self.data[sn] == set(), \
            "sn %d not in data %s or tickers %s not in data[sn]"%(sn, self.data, tickers)
        self.data[sn] =self.data[sn] - tickers
        pass

    def remove_until(self, sn, tickers) :
        current_tickers = self.get_until(sn)
        tickers = set(tickers)
        assert sn in self.data or tickers - current_tickers == set(), \
            "sn %d not in data %s or tickers %s not in current_tickers %s"%(sn, self.data, tickers, current_tickers)
        empties = set()
        for k in self.data.keys() :
            if k > sn :
                continue;
            t = self.data[k] - tickers
            self.data[k] = t
            if t == set() :
                empties.add(k)

        for k in empties :
            del self.data[k]
        pass

    def get(self, sn) :
        if sn not in self.data :
            return set()
        else :
            return self.data[sn]

    def get_until(self, sn) :
        tickers = set()
        for k in self.data.keys() :
            if k <= sn :
                tickers = tickers | self.data[k]
        return tickers

    def reset(self, sn = None, tickers = None) :
        self.data = {}
        if sn != None and tickers != None :
            self.data[sn] = set(tickers)

    def cut(self, cut_sn) :
        cuts = [ sn for sn in self.data.keys() if sn <= cut_sn ]
        for sn in cuts :
            del self.data[sn]

class WatchListConst(WatchList) :
    def __init__(self, name, tickers):
        self.data = set(tickers);
        self.name = name
        pass

    def __str__(self) :
        s = []
        s.append("watchlist, type %s, name %s : %s"%(type(self), self.name, sorted(self.data)))
        return '\n'.join(s)

    def add(self, *args) :
        log.warn("WatchListConst add N/A")
        pass

    def set(self, *args) :
        log.warn("WatchListConst set N/A")
        pass

    def remove(self, sn, tickers) :
        log.warn("WatchListConst remove N/A")
        pass

    def remove_until(self, sn, tickers) :
        log.warn("WatchListConst remove_until N/A")
        pass

    def get(self, sn) :
        return self.data
        pass

    def get_until(self, sn) :
        return self.data
        pass

    def reset(self, *args) :
        log.warn("WatchListConst reset N/A")
        pass

    def cut(self, *args) :
        # log.warn("WatchListConst cut N/A")
        pass

class WatchLists :
    '''
    watch lists management
    '''

    def __init__(self, tickers, watchlist_names,
                 base_sn=0,
                 window_size=None,
                 watchlist_windows={},    # dict, name : windows_size, e.g { 'a' : 5, 'b' : 14 }
                 watchList_relation=None):
        # { name : { sn : [tickers...] } }
        self.watchlists = {}
        self.watchlist_names = watchlist_names
        for i, n in enumerate(self.watchlist_names) :
            if i == 0 :
                self.watchlists[n] = WatchListConst(n, tickers)
            else :
                self.watchlists[n] = WatchList(n)

        self.tickers = set(tickers)
        self.base_sn = base_sn
        self.window_size =window_size
        self.watchlist_relation = watchList_relation
        self.watchlist_windows = watchlist_windows
        self.sn = base_sn
        pass

    def __str__(self) :
        s = []
        s.append("watchlists, type %s : "%(type(self)))
        s.append("tickers         : %s"%self.tickers)
        s.append("watchlist_names : %s"%self.watchlist_names   )
        s.append("base_sn : %s"%self.base_sn)
        s.append("     sn : %s"%self.sn)
        s.append("window_size     : %s"%self.window_size)
        s.append("watchlist_windows  : %s"%self.watchlist_windows)
        s.append("watchlist_relation : %s"%self.watchlist_relation)
        for n in self.watchlist_names :
            s.append(str(self.watchlists[n]))
        return '\n'.join(s)

    def _get_watchlist(self, name):
        assert name in self.watchlists, "wtachlist '%s' not been created"%name
        return self.watchlists[name]

    def watchlist(self, name):
        return self._get_watchlist(name)

    def _validate_tickers(self, tickers) :
        s = set(tickers)
        s = s - self.tickers
        assert s == set(), "passed in tickers %s not in watchlists tickers %s"%(sorted(s), sorted(self.tickers))

    def wl_set_sn(self, sn) :
        assert sn >= self.sn, "wl_set_sn sn %d must >= current sn %d"%(sn, self.sn)
        self.sn = sn

        for n in self.watchlist_names :
            if n in self.watchlist_windows :
                cut_sn = sn - self.watchlist_windows[n]
            elif self.window_size != None :
                cut_sn = sn - self.window_size
            else :
                continue
            self.watchlist(n).cut(cut_sn)
        #

    def wl_get(self, name, pos = 0):
        assert pos<=0, "pos %d ust <= 0"%pos
        s = self.watchlist(name).get(self.sn + pos)
        return sorted(s)

    def wl_get_until(self, name, pos = 0):
        assert pos<=0, "pos %d ust <= 0"%pos
        s = self.watchlist(name).get_until(self.sn + pos)
        return sorted(s)

    def wl_add(self, name, tickers) :
        watchlist = self._get_watchlist(name)
        self._validate_tickers(tickers)
        watchlist.add(self.sn, tickers)

    def wl_set(self, name, tickers) :
        watchlist = self._get_watchlist(name)
        self._validate_tickers(tickers)
        watchlist.set(self.sn, tickers)

    def wl_del(self, name, tickers) :
        watchlist = self._get_watchlist(name)
        self._validate_tickers(tickers)
        watchlist.remove(self.sn, tickers)

    def wl_del_until(self, name, tickers, pos = 0) :
        assert pos <= 0, "pos %d must <= 0"%pos
        watchlist = self._get_watchlist(name)
        self._validate_tickers(tickers)
        watchlist.remove_until(self.sn + pos, tickers)

    def wl_move(self, from_name, tickers, to_name) :
        from_wl = self._get_watchlist(from_name)
        to_wl = self._get_watchlist(to_name)
        self._validate_tickers(tickers)
        from_wl.remove(self.sn, tickers)
        to_wl.add(self.sn, tickers)

    def wl_reset(self, name, tickers = None) :
        assert name in self.watchlists, "wtachlist '%s' not been created"%name
        self.watchlists[name].reset(self.sn, tickers)

    def wl_reset_all(self):
        for i, n in enumerate(self.watchlist_names) :
            if i == 0 :
                continue;
            self.watchlists[n].reset()

    # API interface used by public
    def set_sn(self, sn) :
        assert sn >= self.sn, "set_sn sn %d must >= current sn %d"%(sn, self.sn)
        self.sn = sn

        for n in self.watchlist_names :
            if n in self.watchlist_windows :
                cut_sn = sn - self.watchlist_windows[n]
            elif self.window_size != None :
                cut_sn = sn - self.window_size
            else :
                continue
            self.watchlist(n).cut(cut_sn)

    def remove(self, name, tickers, until_pos = 0, pos = None) :
        watchlist = self._get_watchlist(name)
        self._validate_tickers(tickers)
        if pos is not None :
            watchlist.remove(self.sn + pos, tickers)
        else :
            watchlist.remove_until(self.sn + until_pos, tickers)

    def add(self, name, tickers, pos = 0):
        assert pos <= 0, "pos {} must <= 0".format(pos)
        watchlist = self._get_watchlist(name)
        self._validate_tickers(tickers)
        watchlist.add(self.sn + pos, tickers)

    def set(self, name, tickers, pos = 0):
        assert pos <= 0, "pos {} must <= 0".format(pos)
        watchlist = self._get_watchlist(name)
        self._validate_tickers(tickers)
        watchlist.add(self.sn + pos, tickers)

    def reset(self, name, tickers = None):
        watchlist = self._get_watchlist(name)
        watchlist.reset(self.sn, tickers)

    def get(self, name, pos = None, until_pos = 0) :
        watchlist = self._get_watchlist(name)
        if pos is not None :
            s = watchlist.get(self.sn + pos)
        else :
            s = watchlist.get_until(self.sn + until_pos)
        return list(s)

def test_general() :
    log.info("test_general(), create new watchlists")
    watchlists = WatchLists(["a", 'b', 'c'], ['w1', 'w2', 'w3'], window_size=5)
    log.info(watchlists)

    log.info("reset 'w1'")
    watchlists.reset('w1')
    log.info("reset '1' : %s"%watchlists.watchlist('w1'))

    log.info("add tickers to to list 'w2'")
    watchlists.set_sn(1)
    watchlists.add('w2', ['b', 'a'])
    watchlists.set_sn(2)
    watchlists.set('w2', ['b', 'c'])
    log.info("get w2 @ sn 1 : %s"%watchlists.get('w2', pos = -1))
    log.info("get w2 until sn 1 : %s"%watchlists.get('w2', until_pos = -1))
    log.info("get w2 until sn 2 : %s"%watchlists.get('w2'))
    log.info(watchlists)

    log.info("reset list 'w2'")
    watchlists.set_sn(5)
    watchlists.reset('w2', ['c'])
    log.info(watchlists)

    if False :
        log.info("reset list '2'")
        watchlists.wl_set_sn(5)
        watchlists.wl_reset('2', ['c'])
        log.info(watchlists)

        log.info("add tickers to to list '2' outside trading window")
        watchlists.wl_set_sn(7)
        watchlists.wl_add('2', ['a'])
        log.info(watchlists)
        # log.info(watchlists.watchlist('2'))

        log.info("add tickers to to list '1'")
        watchlists.wl_add('1', ['b'])
        watchlists.wl_add('1', ['a'])
        watchlists.wl_add('1', ['b'])
        watchlists.wl_add('1', ['c'])
        log.info(watchlists)

        log.info("reset all");
        watchlists.wl_reset_all()
        log.info(watchlists)

        if False :
            watchlists.wl_add('1', 'x')
            watchlists.wl_set('1', 'x')

    log.info("done")

def test_remove() :
    log.info("test_remove(), create new watchlists")
    wls = WatchLists(["a", 'b', 'c'], ['1', '2', '3'], window_size=5)
    log.info(wls)

    wls.wl_set_sn(1);
    wls.wl_add('3', ['a', 'b'])
    wls.wl_set_sn(2);
    wls.wl_add('3', ['c', 'b'])
    wls.wl_add('2', ['a', 'b'])

    wls.wl_set_sn(3)
    wls.wl_add('3', ['c'])
    wls.wl_add('2', [ 'b'])
    log.info("after insert : %s"%wls)

    wls.wl_del_until('2', ['b'], -1)
    log.info("after del until '2', ['b'], -1 : %s"%wls)
    wls.wl_del_until('3', ['b'])
    log.info("after del until '3', ['b'] : %s"%wls)

if __name__ == "__main__" :
    handler = logbook.StreamHandler(sys.stdout, level=logbook.DEBUG)
    handler.formatter.format_string = '{record.time}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno}|{record.message}'
    handler.push_application()

    test_general()
    # test_remove()


"""
watchlist
    set_sn(self, sn)
    remove(self, name, tickers, until_pos = x)
    remove(self, name, tickers, pos = x)
    add(self, name, tickers, pos = 0)
    set(self, name, tickers, pos = 0)
    reset(self, name, tickers = None)
    get(self, name, until_pos = x)
    get(self, name, pos = x)
"""
