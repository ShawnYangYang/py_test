#!/usr/bin/env python
# encoding: utf-8

import Queue
import gzip
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
            user = self.queue.get()
            print "worker %s is working on %s" % (self.name, user)
            work(user)
            self.queue.task_done()

def work(user):
    global tabel
    counter = 0
    with gzip.open('/mnt/nfs150/user_weibo/' + str(user) + '.gz', 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                userdic = eval(line)
                tweets = userdic['statuses']
                for tweet in tweets:
                    if tweet['geo']:
                        counter += 1
                        tweet['user'] = user
                        tabel.insert(tweet)
            except Exception as inst:
                print inst
                print 'error'

def main():
    ts = time()
    queue = Queue.Queue()
    conn = MongoClient('localhost', 27017)
    db = conn.weibo
    global tabel
    tabel = db.tweet
    userlist = loaduserlist('/mnt/nfs150/user_weibo/allist.user1')
    for x in range(16):
        worker = Worker(queue, x)
        # Setting the daemon to True will let the main thread exit
        # even though the works are blocked
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue
    for user in userlist:
        queue.put(user)
    queue.join()
    print('Took {}'.format(time() - ts))

main()
