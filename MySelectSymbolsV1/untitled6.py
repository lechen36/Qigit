# -*- coding: utf-8 -*-
import time
from multiprocessing.dummy import Pool as ThreadPool
def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s [%(levelname)s] %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
def process(item):
    log = _get_logger(item)
    log.info("item: %s" % item)
    time.sleep(5)
items = ['apple', 'bananan', 'cake', 'dumpling']
pool = ThreadPool()
pool.map(process, items)
pool.close()
pool.join()


