
import pandas as pd

import sys
import logbook

# logging setup
if True :
    handler = logbook.StreamHandler(sys.stdout, level=logbook.DEBUG)
    handler.formatter.format_string = '{record.time}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno}|{record.message}'
    handler.push_application()
    # or using this : with handler.applicationbound():
    log = logbook.Logger("t01")

if __name__ == "__main__" :
    panel_file = "../db_panel0_03.h5"
    log.info("read panale from hdf5 file {} start".format(panel_file))
    panel = pd.read_hdf(panel_file)
    log.info("read panale from hdf5 file {} done".format(panel_file))
    datetime_index = panel.major_axis
    log.info("datetime_index : \n{}".format(datetime_index))
