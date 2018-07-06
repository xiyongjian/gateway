
import pandas as pd
import numpy as np
from collections import OrderedDict

def test01() :
    print('this test demo panel creation, and the major index will be sorted automatcially')
    data = OrderedDict()

    df = pd.DataFrame(np.random.randn(6, 4), columns=list('ABCD'))
    df.set_index('A', inplace=True)
    data['first'] = df

    df = pd.DataFrame(np.random.randn(6, 4), columns=list('ABCD'))
    df.set_index('A', inplace=True)
    data['second'] = df

    panel = pd.Panel(data)

    print('panel items (codes) : ', panel.items)
    print('panel major axis : ', panel.major_axis)
    print('panel minor axis : ', panel.minor_axis)

    print(panel.get('first'))
    print(panel.get('second'))

    pass

def test02() :
    timeindex = pd.DatetimeIndex(start='2018-04-03 12:12:00',
                                 periods=10,
                                 freq='60S')
    print("timeindex : ", timeindex)

    ps = pd.Series(timeindex)
    print("sereis : ", ps)

    for t in timeindex :
        print("timeindex item : ", t)

    for t in ps :
        print("series item : ", t)

def test03() :
    minutes = pd.DatetimeIndex(start='2018-04-03 12:12:00',
                                 periods=6,
                                 freq='60S')
    stocks = ["a", "b"]
    index = pd.MultiIndex.from_product([minutes, stocks], names=['minute', 'stock'])
    columns = ["close", "open", "volume", "price"]
    df = pd.DataFrame(np.random.rand(12, 4), index = index, columns = columns)
    print("create data frame : ", df)

    df2 = df["close"]
    print("data frame close, type: ", type(df2))
    print("data frame close: ", df2)
    df2 = df2.unstack(level=1)
    print("data frame close, unstack level 1: ", df2)
    print("data frame close, unstack level 1, columns : ", df2.columns)

    df2 = df["close"]
    df2 = df2.unstack(level=0)
    print("data frame close, unstack level 0: ", df2)
    print("data frame close, unstack level 0, columns : ", df2.columns)

    df2 = df[["close", "price"]]
    print("data frame close, type: ", type(df2))
    print("data frame close: ", df2)

    df2 = df2.unstack(level=1)
    print("data frame close/price, unstack level 1: ", df2)
    print("data frame close/price, unstack level 1, columns : ", df2.columns)

def test04() :
    df = pd.DataFrame({"A": [9, 9, 2, 2, 3, 3],
           "B": [3, 4, 3, 4, 3, 4],
           "close": range(10, 16),
           "open": range(10, 16)
       })
    print("df :\n", df)

    df.set_index(["A", "B"], inplace = True)
    print("df set_index A,B :\n", df)

    pass

if __name__ == '__main__' :
    # test01()
    # test02()
    # test03()
    test04()


