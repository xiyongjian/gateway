'''
ref : gateway/gateway/gens/sim_engine.pyx
'''
import numpy as np
import pandas as pd

BAR = 0
SESSION_START = 1
SESSION_END = 2
MINUTE_END = 3
BEFORE_TRADING_START_BAR = 4
action_names = ['BAR', "SESSION_START", "SESSION_END", "MINUTE_END", "BEFORE_TRADING_START_BAR"]

class MinuteSimulationClock:
    def __init__(self, clock_file, timezone='UTC') :
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
    clock = MinuteSimulationClock(clock_file, timezone)
    return clock

if __name__ == '__main__' :
    clock_file = "e:\\tmp\\quant\\data\\clock.csv"
    clock = MinuteSimulationClock(clock_file)

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
        if c > 20 and False:
            break
    pass
