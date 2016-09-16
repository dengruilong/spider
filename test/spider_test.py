#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: spider_test.py
Author: Ruilong Deng (dengruilong@163.com)
Date: 2015/09/20 21:20:43
"""

import sys
import unittest

import log
from spider import Spider


class SpiderTest(unittest.TestCase):
    """
    Spider test
    """

    def setUp(self):
        """
        setUp - Initialize test case
        """

        log.init_log("./log/test")

        self.spider = Spider('conf/spider.conf')

    def test_parse_seed_normal(self):
        """
        test_parse_seed_normal
        """

        self.spider.parse_seed('./conf/urls')
        self.assertEqual(['https://www.baidu.com', 
                          'http://www.163.com', 
                          'http://www.qq.com'],
                         self.spider.spider_config.url_queue[0])

    def test_parse_spider_config_normal(self):
        """
        test_parse_spider_config
        """

        self.assertEqual(self.spider.spider_config.url_list_file, './urls')
        self.assertEqual(self.spider.spider_config.output_directory, './output')
        self.assertEqual(self.spider.spider_config.max_depth, 2)
        self.assertEqual(self.spider.spider_config.crawl_interval, 1)
        self.assertEqual(self.spider.spider_config.crawl_timeout, 1)
        self.assertEqual(self.spider.spider_config.target_url, '.*.(gif|png|jpg|bmp)$')
        self.assertEqual(self.spider.spider_config.thread_count, 8)
        self.assertEqual(self.spider.spider_config.sleep_interval, 1)


if __name__ == '__main__':
    unittest.main()
