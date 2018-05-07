
import logbook
import sys

# logging setup
if True :
    handler = logbook.StreamHandler(sys.stdout, level=logbook.DEBUG)
    handler.formatter.format_string = '{record.time}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno}|{record.message}'
    handler.push_application()
    # or using this : with handler.applicationbound():
    log = logbook.Logger("app01")

import data
import watchlists
import utils

class TradingEnv :
    def __init__(self):
        self.strategy_initialized = False
        self.strategy = None
        self.data= None
        pass

    def set_input(self, panel) :
        self.panel = panel
        # setup clock (from panel*), symbols/tickers (from panel), data

        tickers = set()
        for item in panel.items :
            tickers |= set(panel[item].columns)
        tickers -= set(["date"])
        self.tickers = tickers
        log.info("tickers : {}".format(tickers))

        d = data.Data(tickers = tickers, window_size = 10)
        for item in panel.items :
            bar = data.Bar(name = item, df = panel[item], base_sn = 0)
            d.add_bar(bar)
            log.info("bar {}, index {}...{}".format(bar.name, bar.df.index[:2], bar.df.index[-2:]))

        self.data = d;
        log.info("data : {}".format(d))

        self.initalize_strategy()

    def set_strategy(self, strategy) :
        self.strategy = strategy
        self.initalize_strategy()

    def initalize_strategy(self) :
        if self.strategy_initialized == True :
            return;
        if self.data is not None and self.strategy is not None :
            log.info("initalized strategy")
            self.strategy.initialize(self.data)
            self.strategy_initialized = True;

    def gen_clock(self) :
        for sn, dt in enumerate(panel.major_axis) :
            # always start from sn = 0
            yield (sn, dt)

    def run(self) :
        for sn, dt in self.gen_clock() :
            log.info("SN {}, time {}".format(sn, dt))
            self.data.set_sn(sn)
            self.strategy.prepare(sn, self.data)
            self.strategy.handle(sn, self.data)
        pass

class Strategy :
    def __init__(self) :
        pass

    def initialize(self, d) :
        log.info("initialized strategy")
        pass

    def prepare(self, sn, d) :
        log.info("prepare, sn {}".format(sn))
        pass

    def handle(self, sn, d) :
        log.info("handle, sn {}".format(sn))
        pass

class MyStrategy(Strategy) :
    def __init__(self) :
        super(Strategy, self).__init__()
        pass

    def initialize(self, d) :
        log.info("initialized strategy")
        self.tickers = d.tickers

        wls = watchlists.WatchLists(d.tickers, ["W0", "W1", "W2"], window_size=10)
        self.watchlists = wls

        d.create_factor(name="sma5", window_size=10)
        pass

    def prepare(self, sn, d) :
        log.info("prepare, sn {}".format(sn))
        self.watchlists.set_sn(sn)

        if sn > 5 :
            # sma5 = d.get(name="close", tickers=self.tickers, pos=0, len=5).mean()
            sma5 = d.get(name="close", tickers=self.tickers, len=5).mean()
            # d.set(name="sma5", tickers=self.tickers, value=sma5, pos=0)
            d.set(name="sma5", tickers=self.tickers, value=sma5)
        pass

    def handle(self, sn, d) :
        log.info("----------- handle, sn {} --------------".format(sn))

        if sn <= 5 :
            log.info("skip first 5 for sma5 history of 5")
            return

        #-------------------------------------------------------------------------
        # example to access watch list and factor/bar
        #-------------------------------------------------------------------------
        W0 = self.watchlists.get(name="W0", until_pos = 0)
        sma5 = d.get(name="sma5", tickers=W0)
        # log.info("sma5 : {}\n{}".format(type(sma5), sma5))

        #-------------------------------------------------------------------------
        # process watch list W0 -> W1
        #-------------------------------------------------------------------------
        # get watch list W0 tickers
        W0      = self.watchlists.get(name="W0", until_pos = 0)

        sma5    = d.get(name="sma5", tickers=W0)
        bar_close   = d.get(name="close", tickers=W0)
        bar_close_2 = d.get(name="close", tickers=W0, pos = -1)

        selected = (sma5 > bar_close) & (sma5 > bar_close_2)
        W1 = utils.filter(W0, selected)

        self.watchlists.set(name="W1", tickers=W1, pos=0)
        log.info("select into W1 : {}".format(W1))

        #-------------------------------------------------------------------------
        # process watch list W1 -> W2
        #-------------------------------------------------------------------------
        # get watch list W0 tickers
        W1      = self.watchlists.get(name="W0", until_pos = -2)

        sma5    = d.get(name="sma5", tickers=W1, pos=-1)
        bar_close   = d.get(name="close", tickers=W1, pos=-1)

        selected = (sma5 > bar_close)
        W2 = utils.filter(W1, selected)

        self.watchlists.set(name="W2", tickers=W2, pos=0)
        log.info("select into W2 : {}".format(W2))

        #-------------------------------------------------------------------------
        # for debug only
        #-------------------------------------------------------------------------
        if sn == 15 :
            log.info("DEBUG - watchlist : \n{}".format(self.watchlists))
        pass

if __name__ == "__main__" :
    panel = utils.create_data_panel("2018-04-09 09:30:00", "2018-04-11 15:00:00")
    log.info("panel shape : {}".format(panel.shape))
    log.info("panel items : {}".format(panel.items))
    # log.info("panel columns : {}".format(panel.columns))
    log.info("panel major_axis : {}".format(panel.major_axis))
    log.info("panel['close'].iloc[:2, :2] : \n{}".format(panel["close"].iloc[:2, :2]))

    env = TradingEnv();
    strategy = MyStrategy();

    env.set_input(panel);
    env.set_strategy(strategy)

    env.run();


