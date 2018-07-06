# -*- coding: utf-8 -*-
"""
download high frquence

"""

from ctypes import *
from iFinDPy import *

import time
import json
from datetime import datetime
import pandas as pd
import argparse

import glob
import os
import traceback

from sqlalchemy import create_engine
import logbook

log = logbook.Logger("ths08_load_realtime_files")

#----------------------------------------------------------------------------
#
config = {
    'db_url' : 'mysql+mysqlconnector://ths:ths@127.0.0.1:3306/quant'
}

def get_sql_engine() :
    filepath = os.path.abspath(__file__)
    certs_dir = os.path.dirname(filepath) + os.path.sep + "certs"
    ca_file = certs_dir + os.path.sep + 'ca-cert.pem';
    log.info("ca certs file : {}, exists {}".format(ca_file, os.path.exists(ca_file)))
    engine = create_engine(config['db_url'], connect_args={
        'ssl_ca': ca_file
    })
    return engine

#----------------------------------------------------------------------------
#
def load_realtime_file(filepath) :
    log.info("read file : {}".format(filepath))

    fname = os.path.basename(filepath)
    log.info("filename : {}".format(fname))

    date_str = re.sub(r'rt_(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2}).*',
                      r'\1-\2-\3 \4:\5:\6', fname)
    log.info("date_str : {}".format(date_str))

    with open(filepath, "rt") as fp :
        content = fp.read()
    log.info("read string : \n{}".format(content[:100]))

    quotes = json.loads(content)
    log.info("json quotes : \n{}".format(json.dumps(quotes, indent=4)[:100]))

    data = THS_Trans2DataFrame(quotes)
    log.info(" dataframe {}: \n{}".format(data.shape, str(data)[:200]))

    log.info(" columns : {}".format(data.columns))
    data.rename(columns={'thscode': 'code', 'time': 'minute', 'open': 'open_', 'change': 'change_', 'latest' : 'close'}, inplace=True)
    data['minute'] = date_str
    log.info(" columns(renamed) : {}".format(data.columns))

    log.info(" index( : {}".format(data.index))
    log.info(" put to sql, dataframe : \n{}".format(str(data)[:100]))

    dup = list(data['code'].duplicated())
    if dup.count(True) > 0 :
        log.warning("file {} has duplicated code (be removed) : \n{}"\
                    .format(filepath, [ c for i, c in enumerate(data['code']) if dup[i] ]))
        data.drop_duplicates(subset=['code'], inplace=True)
    else :
        log.info("no duplicated code, passed")

    engine = get_sql_engine()
    log.info("clear table stockdata_stage")
    result = engine.execute("delete from stockdata_stage")
    log.info("clear table stockdata_stage return {}".format(result))

    log.info("put dataframe to stockdata_stage table, shape {}".format(data.shape))
    data.to_sql(name='stockdata_stage', con=engine, if_exists='append', index=False)

    log.info("replace into table stockdata")
    result = engine.execute("replace into stockdata select * from stockdata_stage")
    log.info("replace into table stockdata retuern {}".format(result))

    log.info("done");

#----------------------------------------------------------------------------
#
def t01_pilot() :
    filepath = "c:/xyj/tmp/ths/rt_20180622-150000_07.dat"
    filepath = "c:/xyj/tmp/ths/20180620/rt_20180620-093600_02.dat"
    log.info("read file : {}".format(filepath))

    fname = os.path.basename(filepath)
    log.info("filename : {}".format(fname))

    date_str = re.sub(r'rt_(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2}).*',
           r'\1-\2-\3 \4:\5:\6', fname)
    log.info("date_str : {}".format(date_str))

    with open(filepath, "rt") as fp :
        content = fp.read()
    log.info("read string : \n{}".format(content))

    quotes = json.loads(content)
    log.info("json quotes : \n{}".format(json.dumps(quotes, indent=4)))

    data = THS_Trans2DataFrame(quotes)
    data2 = data.copy()
    log.info(" dataframe : \n{}".format(data))

    log.info(" columns : {}".format(data.columns))

    # engine = create_engine(config['db_url'])
    engine = get_sql_engine()
    # engine = create_engine("mysql+mysqlconnector://ths:ths@127.0.0.1:3306/test");
    data.rename(columns={'thscode': 'code', 'time': 'minute', 'open': 'open_', 'change': 'change_', 'latest' : 'close'}, inplace=True)
    data['minute'] = date_str
    log.info(" columns(2) : {}".format(data.columns))
    log.info(" index( : {}".format(data.index))
    log.info(" put to sql, dataframe : \n{}".format(data))
    # data.to_sql(name='stockdata_stage', con=engine, if_exists='append', index=False)

    log.info("data2 columns : {}".format(data2.columns))
    data2.rename(columns={'latest':'close', 'time':'date', 'thscode':'code'}, inplace=True)
    data2['date'] = date_str
    log.info("data2 columns : {}".format(data2.columns))

    dup = list(data2['code'].duplicated()).count(True)
    if dup > 0:
        log.warning("block id {}, dt {} has duplicated code".format(1, 2))
        data2.drop_duplicates(subset=['code'], inplace=True)
    df_close = data2.pivot(index="date", columns="code", values="close")
    log.info("df_close : \n{}".format(df_close))
    log.info("done");

def t02_sql_dup_key() :
    log.info("data frame to sql, duplication in key")
    engine = get_sql_engine()

    data = pd.DataFrame(index=range(3), data={"id":[1,2,1], "name":["a", "b", "c"]})
    log.info("data frame : \n{}".format(data))
    data.to_sql(name='t02', con=engine, if_exists='append', index=False)

    log.info("done");
#----------------------------------------------------------------------------
#
if __name__ == '__main__':

    handler = logbook.StreamHandler(sys.stdout, level=logbook.DEBUG, bubble=True)
    handler.formatter.format_string = '{record.time}|{record.process_name}-{record.thread_name}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno} - {record.message}'
    handler.push_application()

    fhandler = logbook.FileHandler("ths08_load_file.log", level=logbook.DEBUG, bubble=True)
    fhandler.formatter.format_string = '{record.time}|{record.process_name}-{record.thread_name}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno} - {record.message}'
    # fhandler.push_application()

    setup = logbook.NestedSetup([
        # make sure we never bubble up to the stderr handler
        # if we run out of setup handling
        logbook.NullHandler(),
        handler, fhandler
    ])
    setup.push_application()

    log.info("start..")

    if False :
        # t01_pilot()
        t02_sql_dup_key()

    parser = argparse.ArgumentParser(description='load realtime data to database (1 minute).')
    parser.add_argument('--file', dest='file', help='filename of realtime data', nargs=1, required=True)
    result = parser.parse_args(sys.argv[1:])
    # result = parser.parse_args(['--file', 'c:/xyj/tmp/ths/20180704/rt_20180704-111200_00.dat'])
    # result = parser.parse_args(['--file', 'c:/xyj/tmp/ths/*/rt*.dat'])
    log.info('parsing result : ' + str(result))

    file = result.file[0]
    cnt = 0
    for f in glob.glob(file) :
        cnt = cnt + 1
        try :
            log.info("file # {}, load file {}".format(cnt, f))
            load_realtime_file(f)
        except KeyboardInterrupt:
            raise
        except :
            log.error("exception in loading file {}\n{}".format(f, traceback.format_exc()))

    log.info("done")




