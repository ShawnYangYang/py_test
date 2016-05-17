#!/usr/bin/env python
# encoding: utf-8

import cPickle
from scipy.sparse import coo_matrix
from sklearn.decomposition import TruncatedSVD

def load_matrix():
    fpath = '/mnt/nfs150/review/userreview.pickle'
    f = open(fpath, 'r')
    m = cPickle.load(f)

    ilist = []
    jlist = []
    dlist = []

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

    udic = {ulist[i]:i for i in range(len(ulist))}
    shopdic = {shoplist[i]:i for i in range(len(shoplist))}

    for s in m:
        if s[2] < 0:
            continue
        ilist.append(shopdic[s[1]])
        jlist.append(udic[s[0]])
        dlist.append(s[2])

    sparse_m = coo_matrix((dlist, (ilist, jlist)), shape=(len(shopdic.keys()), len(udic.keys())))
    print 'users %s, shops %s, total %s' %(len(udic.keys()), len(shopdic.keys()), len(m))

    output = open('shoplist', 'w')
    cPickle.dump(shoplist, output)
    return sparse_m

if __name__ == '__main__':
    matrix = load_matrix()
    svd = TruncatedSVD(n_components=100,)
    dense = svd.fit_transform(matrix)

    output = open('densematrix', 'w')
    cPickle.dump(dense, output)

