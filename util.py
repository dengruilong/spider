#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: util.py
Author: Ruilong Deng (dengruilong@163.com)
Date: 2015/09/21 23:38:27
"""

import chardet
import logging

def utf8_convert(content):
    """ 
    utf8_convert - Convert the content to utf8 coding
    """

    try:
        res = chardet.detect(content)

        if res['confidence'] > 0.5 and res['encoding'].lower() != 'utf-8':
            if res['encoding'].lower() == 'gbk' or res['encoding'].lower() == 'gb2312':
                res['encoding'] = 'gb18030'
            uni = content.decode(res['encoding'])
            content = uni.encode('utf-8')

            logging.info('Converting to UTF-8 successful.')
        else:
            logging.info('No need UTF-8 converting.')
    except UnicodeError as e:
        logging.error('Exception throwing while converting page to UTF-8: {}'.format(e))

    return content
