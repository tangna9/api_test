#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/9 14:15
# @Author  : Tang Na
# @Site    : 
# @File    : test_cases.py
# @Software: PyCharm Community Edition

import unittest
from lib import comm
from lib.excl_operation import ExcelOperation
from ddt import ddt, data
from conf import para
import logging
from logging.config import fileConfig

fileConfig("../conf/logging.conf")
log = logging.getLogger("api")

testc = ExcelOperation("401")
test_info = testc.all_test_info()

@ddt
class TestMaterialsList(unittest.TestCase):

    def setUp(self):
        # sign = comm.get_sign(app_id=para.APPid)
        # print sign
        pass

    def tearDown(self):
        pass

    @data(*test_info)
    def test_req_materials_list_401(self, data):
        comm.get_sign(app_id="1", flag=2)
        log.debug("excel_test_info:{0}".format(data))
        (code, mes) = comm.post_https(url=data[2], data=data[3])
        expect_re = (int(data[4]), data[5])
        log.debug("expect result:{0}".format(expect_re))
        self.assertEqual((code, mes), expect_re)


if __name__ == "__main__":
    unittest.main()