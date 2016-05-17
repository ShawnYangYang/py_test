#!/usr/bin/env python
# encoding: utf-8


import Queue
import threading
import time

exitFlag = 0
class myThread(threading.Thread):
    def __init__(self, threadName, threadId, q):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.threadId = threadId
        self.q = q

    def run(self):
        print "Starting " + self.threadName
        process(self.threadName, self.q)
        print "Ending " + self.threadName

def process(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (threadName, data)
        else:
            queueLock.release()
        time.sleep(1)

threadList = ["Thread1", "Thread2", "Thread3"]
namelist = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"]
queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
threadId = 1

#create new threads
for tname in threadList:
    thread = myThread(tname, threadId, workQueue)
    thread.start()
    threads.append(thread)
    threadId += 1

#Fill in the queue
queueLock.acquire()
for name in namelist:
    workQueue.put(name)
queueLock.release()

# wait for the queue to be empty
while not workQueue.empty():
    pass

#Notify the threads it's time to end
exitFlag = 1

#wait for all threads to end
for t in threads:
    t.join()

print "Exiting main threads"


