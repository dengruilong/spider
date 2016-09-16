#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: mini_spider.py
Author: Ruilong Deng (dengruilong@163.com)
Date: 2015/09/20 21:20:43
"""

import log
import sys
import time
import getopt
import socket
import logging
import datetime

from spider import Spider

global VERSION
VERSION = '1.0.0'


class MiniSpider(Spider):
    """
    Mini Spider
    """
    def __init__(self, config):
        """
        Initialize
        """

        Spider.__init__(self, config)
        self.config = config


def parse_opts():
    """
    parse_opts - Parse command line options

    Args:
        -v
        --version                - Print version number

        -h
        --help                   - Print help message

        -c <config_file>         
        --config=<config_file>   - Specify config file

    Raises:
        Error                    - Fail to parse command line options
    """

    try:
        # Parse command line argumants
        opts, args = getopt.getopt(sys.argv[1:], 'c:hv', ['config=', 'help', 'version'])

        config = ''

        for o, a in opts:
            if o in ('-h', '--help'):
                print_usage()
                sys.exit(0)
            elif o in ('-v', '--version'):
                print_version()
                sys.exit(0)
            elif o in ('-c', '--config'):
                config = a

        return config
    except IOError as e:
        logging.error('Fail to parse command line options, msg:{}', format(str(e)))


def print_usage():
    """
    print_usage - Print usage info
    """

    usage  = ('DESCRIPTION:\n'
              '  This script is a mini spider, it crawls the internet web page \n'
              '  according to its config file\n'
              '\n'
              'USAGE: \n  ' + sys.argv[0] + ' [options]\n'
              '  -c config_file  # specify config file for this option\n'
              '  -v              # print version number for mini spider system\n'
              '  -h              # print help message\n\n'
              'EXAMPLE:\n'
              '  ' + sys.argv[0] + ' -c spider.conf\n')

    print usage


def print_version():
    """
    print_version - Print version info
    """

    info = 'Version: ' + VERSION + '\n'

    print info


def main():
    """
    main - Mini Spider Main function

    Return:
        True  - good
        False - error
    """

    status = True

    start_time = datetime.datetime.now()

    # Log will go to ./log/mini_spider.log and ./log/mini_spider.log.wf 
    # Separated by day and keep for 7 days
    log.init_log("./log/mini_spider")
    logging.info('Mini Spider crawling is starting ...')

    config = parse_opts()
    mini_spider = MiniSpider(config)

    try:
        mini_spider.run()
    except ThreadException as e:
        logging.error(e)
        status = False

    # Set network connection timeout for urllib
    socket.setdefaulttimeout(mini_spider.spider_config.crawl_timeout)

    logging.info('Mini Spider crawling is done, please check the result under output/ directory.')
    mini_spider.summary()

    end_time = datetime.datetime.now()
    logging.info('Total time used:       ' + str((end_time - start_time).seconds) + ' seconds')
    logging.info('Exit main thread.')

    return status


if __name__ == '__main__':
    main()
