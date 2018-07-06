import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )


def locker(lock):
    logging.debug('Starting')
    while True:
        lock.acquire()
        try:
            logging.debug('Locking')
            time.sleep(1.0)
        finally:
            logging.debug('Not locking')
            lock.release()
        time.sleep(1.0)
    return


def worker(lock):
    logging.debug('Starting')
    num_tries = 0
    num_acquires = 0
    while num_acquires < 3:
        time.sleep(0.5)
        logging.debug('Trying to acquire')
        acquired = lock.acquire(0)
        try:
            num_tries += 1
            if acquired:
                logging.debug('Try #%d : Acquired', num_tries)
                num_acquires += 1
            else:
                logging.debug('Try #%d : Not acquired', num_tries)
        finally:
            if acquired:
                lock.release()
    logging.debug('Done after %d tries', num_tries)


def test01() :
    lock = threading.Lock()

    locker = threading.Thread(target=locker, args=(lock,), name='Locker')
    locker.setDaemon(True)
    locker.start()

    worker = threading.Thread(target=worker, args=(lock,), name='Worker')
    worker.start()

test02_lock = threading.Lock()
def test02(count = 2) :
    logging.debug("test02, count : {}".format(count))
    test02_lock.acquire();


if __name__ == '__main__':
    # test01()

