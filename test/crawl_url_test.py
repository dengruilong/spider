#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: crawl_url_test.py
Author: Ruilong Deng (dengruilong@163.com)
Date: 2015/09/20 21:20:43
"""

import re
import os
import sys
import logging
import unittest

import log
from spider import SpiderConfig
from crawl_url import CrawlUrl


class CrawlUrlTest(unittest.TestCase):
    """
    crawl_url test
    """

    def setUp(self):
        """
        setUp - Initialize test case
        """

        log.init_log("./log/test")

        self.pattern = re.compile(r'.*.(gif|png|jpg|bmp)$')
        self.spider_config = SpiderConfig('../conf/spider.conf')

        self.crawler = CrawlUrl(1000, 
                                0, 
                                self.spider_config, 
                                'http://family.baidu.com/portal/', 
                                self.pattern)

    def test_crawl_url_normal(self):
        """
        test_crawl_url
        """
        
        self.assertEqual(self.crawler.crawl_url(), True)
        
    def test_parse_html_normal(self):
        """
        test_parse_html
        """

        self.assertEqual(self.crawler.parse_html(), True)

if __name__ == '__main__':
    unittest.main()
