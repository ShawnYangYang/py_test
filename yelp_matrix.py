#!/usr/bin/env python
# encoding: utf-8
import codecs
import Queue
import gzip
import cPickle
from threading import Thread
from time import time
from pymongo import MongoClient
from scipy.sparse import coo_matrix
from sklearn.decomposition import TruncatedSVD

def getShop():
    global tabel
    shops = []
    for s in tabel.find({"$or": [{"categories":"Restaurants"}, {"categories": "Food"}]}):
        shops.append(s["business_id"])
    return shops

def getReview(shop):
    global tabel_review
    r = []
    for s in tabel_review.find({"business_id": shop}):
        r.append([s["user_id"], shop, s["stars"]])
    return r

def filtermatrix(allreview):
    usercount = {}
    shopcount = {}
    for r in allreview:
        if not usercount.has_key(r[0]):
            usercount[r[0]] = 0
        usercount[r[0]] += 1
        if not shopcount.has_key(r[1]):
            shopcount[r[1]] = 0
        shopcount[r[1]] += 1
    shoplist = []
    userlist = []
    for shop in shopcount:
        if shopcount[shop] > 30:
            shoplist.append(shop)
    for user in usercount:
        if usercount[user] > 10:
            userlist.append(user)

    shoplist = set(shoplist)
    userlist = set(userlist)
    result = []
    for r in allreview:
        if r[0] in userlist and r[1] in shoplist:
            result.append(r)
    return result

def getSparse(allreview):
    users = []
    shops = []
    for r in allreview:
        users.append(r[0])
        shops.append(r[1])
    users = list(set(users))
    shops = list(set(shops))
    shops = sorted(shops)
    users = sorted(users)
    shopdic = {shops[i]:i for i in range(len(shops))}
    userdic = {users[i]:i for i in range(len(users))}

    ilist = []
    jlist = []
    slist = []
    for r in allreview:
        ilist.append(shopdic[r[1]])
        jlist.append(userdic[r[0]])
        slist.append(r[2])

    print '%s shops, %s users, %s items' % (len(shopdic.keys()), len(userdic.keys()), len(slist))

    output = open('shoplist', 'w')
    cPickle.dump(shops, output)
    matrix = coo_matrix((slist, (ilist, jlist)), shape=(len(shopdic.keys()), len(userdic.keys())))
    return matrix

def getChain():
    f = open('shoplist', 'r')
    shoplist = cPickle.load(f)

    global tabel
    namedic = {}
    for shop in shoplist:
        s = tabel.find_one({"business_id": shop})
        name = s['name']
        if not namedic.has_key(name):
            namedic[name] = []
        namedic[name].append(shop)

    namecount = []
    for name in namedic:
        namecount.append([name, len(namedic[name])])

    namecount = sorted(namecount, key=lambda x: x[1], reverse= True)
    output = codecs.open('namecount', 'w', 'utf-8')
    for name in namecount:
        print name
        output.write('%s %s\n' %(name[0], name[1]))


def main():
    conn = MongoClient('localhost', 27017)
    db = conn.yelp
    global tabel
    tabel = db.business
    global tabel_review
    tabel_review = db.review
    '''shops = getShop()
    allreview = []
    for shop in shops:
        r = getReview(shop)
        allreview.extend(r)
    allreview = filtermatrix(allreview)
    sparse_matrix = getSparse(allreview)

    svd = TruncatedSVD(n_components=100,)
    dense = svd.fit_transform(sparse_matrix)

    output = open('densematrix', 'w')
    cPickle.dump(dense, output)'''

    getChain()


main()
