
import argparse
from datetime import datetime
from datetime import timedelta

if __name__ == '__main__':
    if True :
        print('start...')
        parser = argparse.ArgumentParser(description='load historic data.')
        parser.add_argument('-l', '--list', dest='dates', help='start/end date, desc order e.g, 2018-04-03 2017-01-01', nargs=2)
        print('to parse...')
        # result = parser.parse_args('-h'.split())
        print('to parse end...')

        # print('result : ' + str(result))

        result = parser.parse_args('--list 2018-04-09 2017-01-01'.split())
        print('result : ' + str(result))

        day_start = datetime.strptime(result.dates[0], '%Y-%m-%d')
        day_end = datetime.strptime(result.dates[1], '%Y-%m-%d')
        print("start %s to %s"%(str(day_start), str(day_end)))
        print("type of day_start : %s"%(type(day_start)))

        day = day_start
        while day >= day_end :
            print("day %s, week day %d"%(day.strftime('%Y-%m-%d'), day.isoweekday()))
            if day.isoweekday() < 6 :
                print(day.strftime('%Y-%m-%d'))
            day = day - timedelta(days=1)

        print('done')

        # read file load_HF.conf, -> load_HF.status
