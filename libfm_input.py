#!/usr/bin/env python
# encoding: utf-8

import cPickle

def write_output():
    fpath = 'userreview.pickle'
    f = open(fpath, 'r')
    m = cPickle.load(f)

    ulist = []
    shoplist = []
    for s in m:
        if s[2] < 0:
            continue
        ulist.append(s[0])
        shoplist.append(s[1])

    ulist = list(set(ulist))
    shoplist = list(set(shoplist))

    shoplist = sorted(shoplist)

    shopdic = {shoplist[i]:i for i in range(len(shoplist))}
    shopcount = len(shoplist)
    udic = {ulist[i]:i+shopcount for i in range(len(ulist))}
    print 'total users %d total shops %d total reviews %d' % (len(ulist), len(shoplist), len(m))

    f = open('shopdic.pickle', 'w')
    cPickle.dump(shopdic, f)
    f = open('userdic.pickle', 'w')
    cPickle.dump(udic, f)
    f.close()
    output = open('libffm_all', 'w')
    counter = 0
    for s in m:
        if s[2] < 0:
            counter += 1
            continue
        output.write('%d ' % (s[2]/10))
        output.write('%s:1 ' % shopdic[s[1]])
        output.write('%s:1 ' % udic[s[0]])
        output.write('\n')
    print 'reviews with no scores %s' % counter


if __name__ == '__main__':
    matrix = write_output()

