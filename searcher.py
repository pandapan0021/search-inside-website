#-*- coding: utf8 -*-

import jieba
import redis
from redis import StrictRedis, ConnectionPool


class Searcher(object):
    """ Redis and jieba 

    use jieba cut the docs, then store in redis

    """

    def __init__(self, redis='localhost', port=6379, prefix='redis:'):
        if isinstance(redis, StrictRedis):
            self.redis = redis
        else:
            pool = ConnectionPool()
            self.redis = StrictRedis(host=redis, port=port, connection_pool=pool)
            self.prefix = prefix

    def _cut_doc(self, doc, doc_id=None):
        """
            cut to words.
        """

        if not doc_id:
            for item in jieba.cut(doc, cut_all=False):
                yield item
        else:
            seg_list = jieba.cut(doc, cut_all=False)
            for item in seg_list:
                length = len(item)+1
                if length > 1:
                    for k in xrange(1, length):
                        yield {'id': doc_id,
                               'key': item[0:k]}
                else:
                    yield {'id': doc_id,
                           'key': item}

    def _store(self, keys):
        self.redis.sadd(self.prefix+keys['key'], keys['id'])
        
    def add_document(self, doc, doc_id):
        for keys in self._cut_doc(doc, doc_id):
            self._store(keys)

    def _sinter(self, keys):
        keys = [self.prefix+key for key in keys]
        return self.redis.sinter(keys)

    def get_result(self, keys):
        seg_list = self._cut_doc(keys)
        newkeys = list(seg_list)
        return self._sinter(newkeys)
