'''
utilities for misc operation
'''

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from collections import OrderedDict
import logbook
import sys

# within project
import config

log = logbook.Logger("utils.py")

def create_data_panel(dt_from, dt_to) :
    '''
    return panel for each code/symbol/stock stored in table stockdata
    :param dt_from:
    :param dt_to:
    :return: panel object
    '''

    # engine = create_engine("mysql+mysqlconnector://ths:ths@127.0.0.1:3306/test");
    log.info("create db connection to " + config.config['db_url'])
    engine = create_engine(config.config['db_url'])

    sql = ' select minute, code, open_, high, low, close, volume from stockdata ' \
          + ' where minute >= "' + dt_from + '" and minute <="' + dt_to + '"'
    log.info("run sql : " + sql)
    df = pd.read_sql(sql, engine)
    df.rename(columns={'minute':'date',"open_":"open", "change_":"change"}, inplace=True)
    log.info("loaded, shape : %s"%str(df.shape))

    data = OrderedDict()
    for code, df_code in df.groupby('code'):
        # log.info("code : " + code)
        # log.info('df_code, type : ' + str(type(df_code)))
        df_code.set_index('date', inplace=True)
        df_code.sort_index(inplace=True)
        data[code] = df_code

    panel = pd.Panel(data)
    return panel

if __name__ == '__main__' :
    handler = logbook.StreamHandler(sys.stdout, level=logbook.DEBUG)
    handler.formatter.format_string = '{record.time}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno}|{record.message}'
    handler.push_application()
    log = logbook.Logger("utils.py testing")

    # test01();

    panel = create_data_panel("2018-04-03 09:32:00", "2018-04-03 09:45:00")
    log.info('panel items (codes) : ' + str(panel.items))
    log.info('panel major axis : ' + str(panel.major_axis))
    if False :
        log.info('panel major axis : ' + panel.major_axis)
        log.info('panel minor axis : ' + panel.minor_axis)
        log.info("panel created : " + panel)
        log.info('panel dir : ' + str(dir(panel)).replace(',', '\n'))
        log.info('panel __dict__ : ' + panel.__dict__)

    panel = panel.sort_index(axis=1, ascending=False)
    # panel = panel.sort_index(axis=0, ascending=False)
    df = panel.get('600026.SH')
    log.info('600026.SH data frame : ' + str(df))

    log.info("done")
