#-*- coding: utf8 -*-

import unittest
from unittest import TestCase

import redis

from searcher import Searcher


class TestSearcherMethods(TestCase):
    
    def setUp(self):
        self.s = Searcher()

    def test_init_with_redisinstance(self):
        r =  redis.StrictRedis()
        s = Searcher(r)
        s.redis.lpush('key:test', 'test')
        self.assertEqual(s.redis.lpop('key:test'), 'test')

    def test_init_with_url(self):
        self.s.redis.lpush('key:test', 'test')
        self.assertEqual(self.s.redis.lpop('key:test'), 'test')
        
    def test_result(self):
        self.s.add_document(u'python很美妙', 2)
        self.assertEqual(self.s.get_result(u'p'), set(['2']))
        self.assertEqual(self.s.get_result(u'python'), set(['2']))
        self.assertEqual(self.s.get_result(u'美妙'), set(['2']))
        
    def tearDown(self):
        self.s.redis.flushall()
        


if __name__ == '__main__':
    unittest.main()
