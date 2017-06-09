#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/9 14:13
# @Author  : Tang Na
# @Site    : 
# @File    : confparser.py
# @Software: PyCharm Community Edition

import ConfigParser
__all__ = ['cf']

def cf():
    '''

    :return: 返回解析后的配置文件
    '''

    cf = ConfigParser.ConfigParser()
    cf.read(["../conf/url.conf"])
    return cf