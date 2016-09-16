#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: run.py
Author: Ruilong Deng (dengruilong@163.com)
Date: 2015/09/20 21:20:43
"""

import os
import sys
import unittest  

  
def test_suite():
    """
    test_suite - Run all test cases in this suite
    """

    suite = unittest.TestLoader().discover('', pattern = "*_test.py")
    alltests = unittest.TestSuite((suite))
    unittest.TextTestRunner(verbosity=2).run(alltests)


if __name__ == "__main__":                     
    sys.path.append(os.getcwd() + '/..')
    test_suite()
