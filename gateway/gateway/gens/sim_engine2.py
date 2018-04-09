'''
ref : gateway/gateway/gens/sim_engine.pyx
'''
import numpy as np
import pandas as pd

import sys
import logbook

log = logbook.Logger("sim_engine2.py")

BAR = 0
SESSION_START = 1
SESSION_END = 2
MINUTE_END = 3
BEFORE_TRADING_START_BAR = 4
action_names = ['BAR', "SESSION_START", "SESSION_END", "MINUTE_END", "BEFORE_TRADING_START_BAR"]

class MinuteSimulationClock:
    def __init__(self, spots) :
        '''
        spots is Series, from DatetimeIndex and convert to UTC
        :param spots:
        :param timezone:
        '''
        self._spots = spots
        print("MinuteSimulationClock, done")
        pass

    def REMOVED__init__(self, clock_file, timezone='UTC') :
        print("MinuteSimulationClock, init with file : ", clock_file)
        series = pd.Series.from_csv(clock_file)
        di = pd.DatetimeIndex(series);
        di = di.tz_localize(timezone).tz_convert("UTC")
        self._spots = pd.Series(di)
        # self._spots = pd.to_datetime(series)
        if False :
            print(type(self._spots[1]))
            print(self._spots.index)
            print(self._spots[0], self._spots[1])

        print("MinuteSimulationClock, done")
        pass

    def _get_minutes_for_list(self, minutes, minute_emission):
        for minute in minutes:
            yield minute, BAR
            if minute_emission:
                yield minute, MINUTE_END

    def __iter__(self):
        spots = self._spots;
        len = spots.size;
        prev = None
        next = None
        for i in range(len) :
            curr = spots[i]
            # next
            if i + 1 < len :
                next = spots[i+1]
            else :
                next = None
            # prev
            if i > 0 :
                prev = spots[i-1]
            # else prev is None

            if prev == None or prev.date() != curr.date() :
                yield curr, SESSION_START
            yield curr, BAR
            yield curr, MINUTE_END
            if next == None or next.date() != curr.date() :
                yield curr, SESSION_END
        pass

    pass

def create_clock(clock_file, timezone='UTC') :
    if clock_file == None :
        raise Exception("no clock file define")

    log.info("init with file : " + clock_file)
    series = pd.Series.from_csv(clock_file)
    di = pd.DatetimeIndex(series);
    di = di.tz_localize(timezone).tz_convert("UTC")
    spots = pd.Series(di)
    return create_clock2(spots)
    # log.info("spots type : " + str(type(spots)))
    # clock = MinuteSimulationClock(spots)
    # return clock

def create_sim_clock(clock_file = None, datetime_index = None, spots = None, timezone = 'UTC') :
    if clock_file is not None :
        log.info("init with file : " + clock_file)
        series = pd.Series.from_csv(clock_file)
        datetime_index = pd.DatetimeIndex(series);

    # fall through
    if datetime_index is not None :
        datetime_index = datetime_index.tz_localize(timezone).tz_convert("UTC")
        spots = pd.Series(datetime_index)

    # fall through
    if spots is not None :
        log.info("spots type : " + str(type(spots)))
        clock = MinuteSimulationClock(spots)
        return clock

    raise Exception("both spots and datetime_index are None, at least one should be set")

def test01() :
    clock_file = "..\\..\\..\\data\\clock.csv"
    # clock = MinuteSimulationClock(clock_file)
    clock = create_clock(clock_file)

    series = pd.Series.from_csv(clock_file)
    series = pd.to_datetime(series)
    di = pd.DatetimeIndex(series);
    di = di.tz_localize('UTC')
    print("di : ", di)
    print("len di :", len(di))
    print("di.size :", di.size)
    print("di [0] :", di[0])

    c = 0;
    for dt, action in clock :
        print("dt ", dt, ", action ", action, ", date ", dt.date(), ", time ", dt.time(), "event ", action_names[action])

        c = c + 1
        if c > 20 and True:
            break
    pass

if __name__ == '__main__' :
    handler = logbook.StreamHandler(sys.stdout, level=logbook.DEBUG)
    handler.formatter.format_string = '{record.time}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno}|{record.message}'
    handler.push_application()
    test01();

