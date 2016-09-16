#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: log_test.py
Author: Ruilong Deng (dengruilong@163.com)
Date: 2015/09/20 21:20:43
"""

import re
import os
import sys
import logging
import unittest

import log


class LogTest(unittest.TestCase):
    """
    Log test
    """

    def setUp(self):
        """
        setUp - Initialize test case
        """

        log.init_log("./log/test")

    def test_logging_normal(self):
        """
        test_logging
        """

        logging.info('Test logging')
        
        line = os.popen("tail -n 1 ./log/test.log").readlines()
        
        # INFO: 09-22 20:24:18: log_test.py:41 * 140109546473184 Test logging
        pattern = re.compile(r'INFO:\s\d+-\d+\s\d+:\d+:\d+:\s\S+\.py:\d+\s\*\s\d+\sTest logging')

        match = pattern.search(line[0].strip())

        self.assertNotEqual(match, None) 


if __name__ == '__main__':
    unittest.main()  
