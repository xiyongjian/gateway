
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

if __name__ == '__main__' :
    # test01()
    test02()
