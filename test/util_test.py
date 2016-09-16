#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: util_test.py
Author: Ruilong Deng (dengruilong@163.com)
Date: 2015/09/20 21:20:43
"""

import re
import os
import sys
import urllib
import logging
import unittest

import log
import util


class UtilTest(unittest.TestCase):
    """
    Util test
    """

    def setUp(self):
        """
        setUp - Initialize test case
        """

        log.init_log("./log/test")

        fh = urllib.urlopen('http://family.baidu.com/portal/')
        self.page = fh.read()

    def test_utf8_convert_normal(self):
        """
        test_utf8_convert_normal
        """

        logging.info('Test util module')
        util.utf8_convert(self.page)

        line = os.popen("tail -n 1 ./log/test.log").readlines()
        pattern = re.compile(r'Converting to UTF-8 successful.|No need UTF-8 converting.')
        match = pattern.search(line[0].strip())
        self.assertNotEqual(match, None) 


if __name__ == '__main__':
    unittest.main()  
