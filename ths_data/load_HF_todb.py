'''
load high frqequent data (1 minute) from THS into file. copy from load_HF
'''

import argparse

import datetime
from sqlalchemy import create_engine
import sys
import traceback
from multiprocessing import Process, Queue
import os

from iFinDPy import *

import glob
import pandas as pd

sys.path.append('..')
import config

# logging setup
import sys
import logbook
# from logbook import NestedSetup, NullHandler, FileHandler, MailHandler, Processor
if True :
    handler = logbook.StreamHandler(sys.stdout, level=logbook.DEBUG, bubble=True)
    # handler.formatter.format_string = '{record.time}|{record.process_name}-{record.thread_name}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno} - {record.message}'
    handler.formatter.format_string = '{record.time}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno} - {record.message}'
    # handler.push_application()

    fhandler = logbook.FileHandler("load_HF.log", level=logbook.DEBUG, bubble=True)
    # fhandler.formatter.format_string = '{record.time}|{record.process_name}-{record.thread_name}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno} - {record.message}'
    fhandler.formatter.format_string = '{record.time}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno} - {record.message}'
    # fhandler.push_application()

    setup = logbook.NestedSetup([
        # make sure we never bubble up to the stderr handler
        # if we run out of setup handling
        logbook.NullHandler(),
        handler, fhandler
    ])
    setup.push_application()

    log = logbook.Logger("load_HF")

def t01_test_db() :
    engine = create_engine(config.config['db_url'])
    log.info("db engine created, id {}, str {}".format(id(engine), engine))

    with engine.connect() as con:
        log.info("run sql : SELECT * FROM stockdata_stage0 limit 3")
        rs = con.execute('SELECT * FROM stockdata_stage0 limit 3')
        log.info("restu rs : {}".format(rs))
        for row in rs:
            log.info("row : {}".format(row))

    log.info("test_db done.")

if __name__ == '__main__':
    if False:
        t01_test_db()
        exit(0)

    if len(sys.argv) > 1 :
        path = sys.argv[1]
    else :
        path = "."

    log.info("locd all csv file under path {}".format(path))

    for file in glob.glob(path + "/HF*.csv") :
        log.info("load file {} to DB".format(file))

        data = pd.read_csv(file)
        # log.info(data.info())
        # log.info(data[:2])

        data.drop(columns=["Unnamed: 0"], inplace=True)
        # data.set_index("time", inplace=True)
        data.rename(columns={'thscode': 'code', 'time': 'minute', 'open': 'open_', 'change': 'change_'}, inplace=True)
        # log.info(data.info())
        # log.info(data[:2])

        if True :
            log.info("data length : %d"%len(data['minute']))
            log.info("create db connection to " + config.config['db_url'])
            engine = create_engine(config.config['db_url'])
            # engine = create_engine("mysql+mysqlconnector://ths:ths@127.0.0.1:3306/test");

            worker_id = 0
            stage_table = "stockdata_stage%d"%worker_id
            log.info("load into %s"%stage_table)
            data.to_sql(name=stage_table, con=engine, if_exists='append', index=False, chunksize=100)

            log.info("replace into from %s"%stage_table)
            result = engine.execute("replace into stockdata select * from %s"%stage_table)
            log.info("replace into, return : " + str(result))

            log.info("clean stage table %s"%stage_table)
            # result = connection.execute("delete from %s"%stage_table)
            result = engine.execute("delete from %s"%stage_table)
            log.info("delete from, return : " + str(result))

            log.info("close engine")
            engine.dispose()

