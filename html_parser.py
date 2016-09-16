#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: html_parser.py
Author: Ruilong Deng (dengruilong@163.com)
Date: 2015/09/20 21:20:43
"""

import os
import re
import urllib
import logging
import urlparse

from HTMLParser import HTMLParser


class HtmlParser(HTMLParser):
    """
    Html Parser
    """

    def __init__(self, url):
        """
        Initialize
        """

        self.data = []

        self.pattern = ''
        self.url = url

        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        """
        Handle start tag of HTML

        Args:
          tag   - HTML tag, eg. <a>, <p>, <body>, ...
          attrs - HTML tag attributes key/value pairs
        """

        # Parsing the tag <a> and <img> which has url
        if tag == 'a' or tag == 'img':
            for name, value in attrs:
                if name == 'href' or name == 'src':

                    # Match the given pattern from spider config file
                    match1 = self.pattern.search(value)

                    # Match the link with prefix 'http'
                    pattern = re.compile(r'^\s*http', re.I)
                    match2 = pattern.search(value)

                    # Get the absolute img url
                    if match1 and match2:
                        logging.info('Save url to local: {}'.format(value))
                        self.save_to_local(value)

                    # Get the relative img url
                    elif match1 and not match2:
                        self.url = urlparse.urljoin(self.url, value)
                        logging.info('Save url to local: {}'.format(self.url))
                        self.save_to_local(self.url)

                    if tag == 'a' and name == 'href':
                        url = self.get_url(pattern, value)
                        url = url.strip()
                        self.spider_config.url_queue[self.next_depth].append(url) 

    def get_url(self, pattern, value):
        """
        get_url - get url
        """

        url = ''
        
        if pattern.search(value):
            url = value
        else:
            url = urlparse.urljoin(self.url, value)

        return url

    def set_pattern(self, pattern):
        """
        Set pattern which comes from Spider config file
        """

        self.pattern = pattern

    def set_urls(self, spider_config):
        """
        Set urls which comes from Spider config file
        """
        
        self.spider_config = spider_config

    def set_next_depth(self, depth):
        """
        Set search depth
        """

        self.next_depth = depth + 1

    def save_to_local(self, url):
        """
        save_to_local - Save the matched url into local location

        Args:
            url - url path

        Raises:
            IOError - fail to create file
        """

        file_name = url
        file_name = urllib.quote_plus(file_name)

        try:
            # Create output/ dir if not existing
            current_dir = os.getcwd()
            if not os.path.exists('{}/output/'.format(current_dir)):
                os.system('mkdir output/')
        except IOError as e:
            logging.fatal('Failed to create output/, msg:{}'.format(e))
            return False

        if not os.path.exists('{}/output/{}'.format(current_dir, file_name)):
            try:
                fh = open('{}/output/{}'.format(current_dir, file_name), 'wb')

                try:
                    fb = urllib.urlopen(url)
                    content = fb.read()
                    fh.write(content)
                    self.spider_config.total_download_images += 1
                except IOError as e:
                    logging.fatal('Failed to open {}, msg:{}'.format(url, str(e)))
                    return False

                fh.close()
            except IOError as e:
                logging.fatal('Failed to open {}/output/{}, msg:{}'.format(current_dir, 
                                                                           file_name, 
                                                                           str(e)))
                return False
        else:
            logging.warn(file_name + ' is existing, skip saving')
            return False

        return True
