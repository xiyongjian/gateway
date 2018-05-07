
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from collections import OrderedDict

import logbook
import sys

sys.path.append('..')
import config

log = logbook.Logger("watchlists.py")

#------------------------------------------------------------------------
# filter list a (list of object), based on condition c (list of boolean)
def filter(a, c) :
    return [i for (i, cond) in zip(a, c) if cond]

def create_data_panel(dt_from, dt_to, codes = None) :
    '''
    return panel for each code/symbol/stock stored in table stockdata
    :param dt_from:
    :param dt_to:
    :param codes:   list of codes to select
    :return: panel object, itmes are columns (e.g, price,close,high,low,volumn..)
    '''

    codes_str = None
    if codes is not None :
        for c in codes :
            if codes_str is None :   # first one, no ','
                codes_str = '"' + c + '"'
            else :
                codes_str = codes_str + ',"' + c + '"'

    # engine = create_engine("mysql+mysqlconnector://ths:ths@127.0.0.1:3306/test");
    log.info("create db connection to " + config.config['db_url'])
    engine = create_engine(config.config['db_url'])

    sql = ' select minute, code, open_, high, low, close, volume from stockdata ' \
          + ' where minute >= "' + dt_from + '" and minute <="' + dt_to + '"'
    if codes_str is not None :
          sql += ' and code in ( ' + codes_str + ' )'
    log.info("run sql : " + sql)
    df = pd.read_sql(sql, engine)
    df.rename(columns={'minute':'date',"open_":"open", "change_":"change"}, inplace=True)
    log.info("loaded data frame, shape : %s"%str(df.shape))
    log.info("loaded data frame, columns : %s"%str(df.columns))
    log.info("loaded data frame, index : %s"%str(df.index))
    log.info("loaded data frame, index type: {}".format(type(df.index)))

    log.info("pivot data frame, column by column")
    # df.pivot(index='a', columns='b', values='c').fillna(0)

    data = OrderedDict()
    for col in set(df.columns) - set(["code", "date"]):
        log.info("build panel for column : {}".format(col))
        df_col = df.pivot(index="date", columns="code", values=col)
        log.info("shape : {}".format(df_col.shape))
        # log.info("index : {}".format(df_col.index))
        data[col] = df_col

    if False :
        data = OrderedDict()
        for code, df_code in df.groupby('code'):
            # log.info("code : " + code)
            # log.info('df_code, type : ' + str(type(df_code)))
            df_code.set_index('date', inplace=True)
            df_code.sort_index(inplace=True)
            data[code] = df_code

    panel = pd.Panel(data)

    if False : # just added for debug/info output
        panel_file = "db_panel0.h5"
        log.info("panel to_hdf5 file {} start".format(panel_file))
        panel.to_hdf(panel_file, "db")
        log.info("panel to_hdf5 file {} done".format(panel_file))
        import os
        log.info("hdf5 file size : {}".format(os.path.getsize(panel_file)))

    return panel

def test_01() :
    panel = create_data_panel("2018-04-09 09:30:00", "2018-04-11 15:00:00")
    log.info("panel shape : {}".format(panel.shape))
    log.info("panel items : {}".format(panel.items))
    # log.info("panel columns : {}".format(panel.columns))
    log.info("panel major_axis : {}".format(panel.major_axis))
    pass

if __name__ == '__main__' :
    handler = logbook.StreamHandler(sys.stdout, level=logbook.DEBUG)
    handler.formatter.format_string = '{record.time}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno}|{record.message}'
    handler.push_application()
    log = logbook.Logger("utils.py testing")

    test_01()

