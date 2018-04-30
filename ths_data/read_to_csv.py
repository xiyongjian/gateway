'''
select/read from database, and write result to csv file
'''
import argparse

# logging setup
import sys
import logbook
# from logbook import NestedSetup, NullHandler, FileHandler, MailHandler, Processor
if True :
    handler = logbook.StreamHandler(sys.stdout, level=logbook.DEBUG, bubble=True)
    handler.formatter.format_string = '{record.time}|{record.process_name}-{record.thread_name}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno} - {record.message}'
    # handler.push_application()

    fhandler = logbook.FileHandler("read_to_csv.log", level=logbook.DEBUG, bubble=True)
    fhandler.formatter.format_string = '{record.time}|{record.process_name}-{record.thread_name}|{record.level_name}|{record.module}|{record.func_name}|{record.lineno} - {record.message}'
    # fhandler.push_application()

    setup = logbook.NestedSetup([
        # make sure we never bubble up to the stderr handler
        # if we run out of setup handling
        logbook.NullHandler(),
        handler, fhandler
    ])
    setup.push_application()

    log = logbook.Logger("load_HF")

if __name__ == '__main__':
    log.info('start...')
    parser = argparse.ArgumentParser(description='read/select from database and write to csv file.')
    parser.add_argument('--csv-file', dest='csv_file', help='name of building list or todo list', nargs=1, required=True)
    parser.add_argument('--list', dest='dates', help='start/end date, desc order e.g, 2018-01-01 2018-12-31', nargs=2, required=True)

    if True :
        log.info("testing arg parsing")
        result= parser.parse_args(['--csv-file','20180328.csv','--list', '2018-03-28', '2018-04-04'])
        ## result= parser.parse_args(['--csv-file','20180328.csv'])
        log.info('parsing result : ' + str(result))
        # sys.exit(0)

    if False :
        log.info('to parse...' + str(sys.argv))
        result = parser.parse_args(sys.argv[1:])
        log.info('parsing result : ' + str(result))

    start_minute = result.dates[0] + " 09:30:00"
    end_minute = result.dates[1] + " 15:00:00"
    log.info("select from {} to {}".format(start_minute, end_minute))



    log.info("main done")
