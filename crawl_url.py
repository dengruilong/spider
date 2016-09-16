#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: crawl_url.py
Author: Ruilong Deng (dengruilong@163.com)
Date: 2015/09/20 21:20:43
"""

import time
import util
import urllib
import thread
import logging
import threading

from html_parser import HtmlParser


class CrawlUrl(threading.Thread):
    """
    Crawl URL using multi-thread
    """

    def __init__(self, thread_id, depth, spider_config, url, pattern):
        """
        __init__ - Initialize thread id, name

        Args:
          thread_id     - Thread ID
          depth         - Search depth
          spider_config - Spider config options
          url           - URL
          pattern       - Regression expression pattern
        """

        super(CrawlUrl, self).__init__()

        self.thread_id = thread_id
        self.depth = depth
        self.spider_config = spider_config
        self.url = url
        self.pattern = pattern
        self.page = ''

    def run(self):
        """
        run - Start the thread

        Raises:
            Error - Fail to get the url
        """
         
        try:
            logging.info('Thread:{} starting'.format(self.thread_id))

            self.crawl_url()
            self.parse_html()
        except IOError as e:
            self.thread_post_processing()
            logging.error('CrawlUrlError url:{} msg:{}'.format(self.url, e))

        self.thread_post_processing()

    def thread_post_processing(self):
        """
        thread_post_processing
        """

        # Current thread is terminating, and the available thread count will increase 1
        self.spider_config.thread_count += 1

        logging.info('Thread:{} ending. Remaining available thread count:{}'
                     .format(self.thread_id, self.spider_config.thread_count))

    def crawl_url(self):
        """
        crawl_url - Crawl url
        """

        logging.info('Thread:{} crawls {}'.format(self.thread_id, self.url))

        try:
            url = self.url.encode("UTF-8")
            fh = urllib.urlopen(url)
            self.page = fh.read()
            # self.page = util.utf8_convert(self.page)
        except IOError as e:
            logging.error('Thread:{} crawl {} failed, msg:{}'.format(self.thread_id, self.url, e))
            return False

        return True

    def parse_html(self):
        """
        parse_html - Parse the html content
        """

        try:
            parser = HtmlParser(self.url)

            parser.set_pattern(self.pattern)
            parser.set_urls(self.spider_config)
            parser.set_next_depth(self.depth)
            parser.feed(self.page)
            parser.close()
        except UnicodeDecodeError as e:
            logging.error('Thread:{} parse {} failed, msg:{}'.format(self.thread_id, self.url, e))
            return False

        return True
