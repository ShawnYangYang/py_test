import thread
import time

#define a function for the thread
def print_time(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print '%s: %s' %(threadName, time.ctime(time.time()))

# create two threads as follows
try:
    thread.start_new_thread(print_time, ("Thread1", 2,))
    thread.start_new_thread(print_time, ("Thread2", 5,))
except:
    print "Error: unable to start thread"


