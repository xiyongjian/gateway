
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from collections import OrderedDict
import utils

def create_data_panel_removed(dt_from, dt_to) :
    # engine = create_engine("mysql+mysqlconnector://ths:ths@127.0.0.1:3306/test");
    print("create db connection to ", config.config['db_url'])
    engine = create_engine(config.config['db_url'])
    sql = ' select minute, code, open_, high, low, close, volume from stockdata ' \
        + ' where minute >= "' + dt_from + '" and minute <="' + dt_to + '"'
    print("run sql : " + sql)
    df = pd.read_sql(sql, engine)
    df.rename(columns={'minute':'date',"open_":"open", "change_":"change"}, inplace=True)
    print("loaded, shape : ", df.shape)

    data = OrderedDict()
    for code, df_code in df.groupby('code'):
        print("code : ", code)
        print('df_code, type : ', type(df_code))
        df_code.set_index('date', inplace=True)
        df_code.sort_index(inplace=True)
        data[code] = df_code

    panel = pd.Panel(data)
    return panel

def test01() :
    engine = create_engine("mysql+mysqlconnector://ths:ths@127.0.0.1:3306/test");
    # df = pd.read_sql("select * from clock", "mysql+mysqlconnector://ths:ths@127.0.0.1:3306/test")
    # df = pd.read_sql("select * from clock", engine)
    # df = pd.read_sql("select * from stockdata", engine)
    df = pd.read_sql("select minute, code, open_, high, low, close, volume from stockdata", engine)
    df.rename(columns={'minute':'date',"open_":"open", "change_":"change"}, inplace=True)

    print("loaded, shape : ", df.shape)

    if False:
        print(df)
        print(df.info(verbose=True))

    t = None
    for code, df_code in df.groupby('code'):
        print("code : ", code)
        print('df_code, type : ', type(df_code))
        if t is None :
            t = df_code

    t.set_index('date', inplace=True)
    # t.sort_index(ascending=False, inplace=True)
    t.sort_index(inplace=True)
    print(t)

    df.rename(columns={'date':'minute',"open":"open_", "change":"change_"}, inplace=True)
    pass

if __name__ == '__main__' :
    # test01();

    panel = utils.create_data_panel("2018-04-03 09:32:00", "2018-04-03 09:45:00")
    print('panel items (codes) : ', panel.items)
    print('panel major axis : ', panel.major_axis)
    if False :
        print('panel major axis : ', panel.major_axis)
        print('panel minor axis : ', panel.minor_axis)
        print("panel created : ", panel)
        print('panel dir : ', str(dir(panel)).replace(',', '\n'))
        print('panel __dict__ : ', panel.__dict__)

    df = panel.get('600026.SH')
    print('600026.SH data frame : ', df)

    print("done")
