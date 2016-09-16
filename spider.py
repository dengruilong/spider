#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: spider.py
Author: Ruilong Deng (dengruilong@163.com)
Date: 2015/09/20 21:20:43
"""

import re
import time
import logging
import ConfigParser

from crawl_url import CrawlUrl


class ThreadException(Exception):
    """
    ThreadException
    """

    pass


class Spider(object):
    """
    Spider
    """

    def __init__(self, config_file):
        """
        __init__ - Initialize the Spider class

        Args:
          config_file   - Spider config file path.
        """

        self.config_file = config_file
        self.spider_config = SpiderConfig(self.config_file)

        # Init the url_queue array
        for depth in range(0, self.spider_config.max_depth + 1):
            self.spider_config.url_queue[depth] = []

    def run(self):
        """
        run - Spider run function
        """

        status = self.parse_seed(self.spider_config.url_list_file)

        if status == True:
            self.process_seed()
        else:
            raise ThreadException("Can't parse the seed from url list file")

    def parse_seed(self, seed_file):
        """
        parse_seed - Parse the seed urls from seed file coming from Spider config file

        Args:
            seed_file - seed file which defines the url seeds

        Return:
            True      - successfully parsing seed
            False     - not successfully parsing seed
        """

        pattern = re.compile(r'^\s*(http|https):\/\/.*')

        try:
            with open(seed_file) as seed_file_lines:
                for line in seed_file_lines:
                    line = line.strip()

                    match = pattern.search(line)
                    if match:
                        # Put all the url seeds into depth=0 url_queue
                        self.spider_config.url_queue[0].append(match.group(0))
        except IOError as e:
            logging.fatal('Failed to open {}, msg:{}'.format(url, str(e)))
            return False

        return True

    def process_seed(self):
        """
        process_seed - Process seed url(s)

        Return:
            True  - success
            False - error
        """

        pattern = re.compile(r'%s' % self.spider_config.target_url)

        thread_pool = []

        # Do search in breadth-first
        for depth in range(0, self.spider_config.max_depth):
            thread_id = 1000

            while True:
                has_url = 'yes'

                while self.spider_config.thread_count > 0:
                    url = self.get_next_url(depth)

                    while self.is_visited(url):
                        url = self.get_next_url(depth)

                    if url != '':
                        crawler = CrawlUrl(thread_id, depth, self.spider_config, url, pattern)

                        thread_pool.append(crawler)
                        crawler.start()

                        self.spider_config.thread_count -= 1 
                        thread_id += 1

                        # Mark the visited url
                        self.spider_config.visited_urls[url] = 1
                    else:
                        logging.info('Depth:{} crawling is done.'.format(depth))

                        # No url in this queue
                        has_url = 'no'
                        time.sleep(self.spider_config.sleep_interval)

                        break

                # crawl_interval
                time.sleep(self.spider_config.crawl_interval)

                # Break the infinite loop while no urls, and will go ahead to do the next level search
                if has_url == 'no':
                    break
        
        # Wait all thread complete before exiting main thread
        for thread in thread_pool:
            thread.join()

        return True

    def get_next_url(self, depth):
        """
        get_next_url - Get the next url from the pending visiting list

        Args:
            depth - Specify the search depth of the page
        """
    
        if len(self.spider_config.url_queue[depth]) > 0:
            url = self.spider_config.url_queue[depth].pop()

            pattern = re.compile(r'\/$')
            if not pattern.search(url):
                url += '/'

            return url
        else:
            return ''

    def is_visited(self, url):
        """
        is_visited - Check if the url is visited or not

        Args:
            url - Specify the pending crawling url
        """

        if self.spider_config.visited_urls.get(url):
            return True
        else:
            return False

    def summary(self):
        """
        summary - Summerize the crawling result
        """

        self.spider_config

        logging.info('Total crawl depth:          ' + str(self.spider_config.max_depth))
        logging.info('Total crawl urls:           ' + str(len(self.spider_config.visited_urls)))
        logging.info('Total download image files: ' + str(self.spider_config.total_download_images))
        

class SpiderConfig(object):
    """
    Spider config options
    """

    def __init__(self, config_file):
        """
        __init__ - Initialize config options

        Args:
          config_file  - Spider config file path
        """

        config = ConfigParser.RawConfigParser()
        config.read(config_file)

        self.url_list_file = config.get('spider', 'url_list_file')
        self.output_directory = config.get('spider', 'output_directory')
        self.max_depth = config.getint('spider', 'max_depth')
        self.crawl_interval = config.getint('spider', 'crawl_interval')
        self.crawl_timeout = config.getint('spider', 'crawl_timeout')
        self.target_url = config.get('spider', 'target_url')
        self.thread_count = config.getint('spider', 'thread_count')
        self.sleep_interval = config.getint('spider', 'sleep_interval')
        
        self.visited_urls = {} # Put all the visited urls in this hash
        self.url_queue = {} # Put the urls in depth hash
        self.seeds = [] # Put all the seed urls in this seeds array

        self.total_download_images = 0

        logging.info('Load url_list_file: ' + self.url_list_file)
        logging.info('Load output_directory: ' + self.output_directory)
        logging.info('Load max_depth: ' + str(self.max_depth))
        logging.info('Load crawl_interval: ' + str(self.crawl_interval))
        logging.info('Load crawl_timeout: ' + str(self.crawl_timeout))
        logging.info('Load target_url: ' + self.target_url)
        logging.info('Load thread_count: ' + str(self.thread_count))
        logging.info('Load sleep_interval: ' + str(self.sleep_interval))
