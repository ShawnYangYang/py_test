#!/usr/bin/env python
# encoding: utf-8
import random
import sys


def loaduserlist(file_name):
    f = open(file_name, 'r')
    lines = f.readlines()
    r = []
    for line in lines:
        r.append(int(line.lstrip().rstrip()))
    return r

def split(file_name, training_c, test_c):
    total = training_c + test_c
    f = open(file_name, 'r')
    lines = f.readlines()
    f_train = open(file_name+'_train', 'w')
    f_test = open(file_name+'_test', 'w')
    for line in lines:
        if random.randint(0, total) <= training_c:
            f_train.write(line)
        else:
            f_test.write(line)
    f_train.close()
    f_test.close()
    f.close()

if __name__ == '__main__':
    split(sys.argv[1], 3, 1)
