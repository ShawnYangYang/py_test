#!/usr/bin/env python
# encoding: utf-8

import Queue
import gzip
import json
from threading import Thread
from time import time
from pymongo import MongoClient
#from bson.son import SON

from utils import *


class Worker(Thread):
    def __init__(self, queue, name):
        Thread.__init__(self)
        self.queue = queue
        self.name = name

    def run(self):
        while True:
            # get the work from the queue
            line = self.queue.get()
            dic = json.loads(line)
            print "worker %s is working on %s" % (self.name, dic['business_id'])
            work(dic)
            self.queue.task_done()

def work(dic):
    global tabel
    try:
        tabel.insert(dic)
    except Exception as inst:
        print inst
        print 'error'

def main():
    ts = time()
    queue = Queue.Queue()
    conn = MongoClient('localhost', 27017)
    db = conn.yelp
    global tabel
    tabel = db.checkin
    f = open('../yelp/yelp_academic_dataset_checkin.json', 'r')
    lines = f.readlines()

    for x in range(16):
        worker = Worker(queue, x)
        # Setting the daemon to True will let the main thread exit
        # even though the works are blocked
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue
    for line in lines:
        queue.put(line)
    queue.join()
    print('Took {}'.format(time() - ts))

main()
