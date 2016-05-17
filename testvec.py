#!/usr/bin/env python
# encoding: utf-8

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(min_df=1)
corpus = [['今天', '是', '3', '月', '18号'],
          ['明天', '是', '3月', '19号'],
          ['后天', '是', '3月', '20号']]
X = vectorizer.fit_transform(corpus)
for s in vectorizer.get_feature_names():
    print s,
print ' '
print X.toarray()
