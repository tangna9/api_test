#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/9 14:13
# @Author  : Tang Na
# @Site    : 
# @File    : excl_operation.py
# @Software: PyCharm Community Edition

import xlrd
from lib import confparser, comm
import logging
from logging.config import fileConfig
import json
from conf import para

fileConfig("../conf/logging.conf")
log = logging.getLogger("api")
__all__ = ['ExcelOperation', 'get_raw_cases_data']

class ExcelOperation(object):
    '''
    测试case的excel文件相应处理
    '''
    def __init__(self, sheet):

        try:
            file = confparser.cf().get("file", "TESTCASES")
            self.data = xlrd.open_workbook(file)
            self.table = self.data.sheet_by_name(sheet)
        except Exception, e:
            log.debug(str(e))

    def get_cases_row(self):
        nrow = self.table.nrows
        return nrow

    def get_single_row_test_info(self, active=8, row_no=2):
        '''
        :param active:
        :param row_no:
        :return:
        '''
        status = self.table.cell(row_no, active).value
        if "y" in status:
            test_info = []
            for col in range(self.table.ncols):
                cell = self.table.cell(row_no, col).value
                test_info.append(cell)
            return test_info

    def all_test_info(self, start=1, **col):
        '''
        :param start: the start row index of actual test data(exclude title)
        :param col: a dict that map the testcases'title and its index
        :return:
        '''
        col = para.excel_map
        item = []
        test_info = []
        for row in range(start, self.table.nrows):
            no = self.table.cell(row, col["NO"]).value
            test_des = self.table.cell(row, col["TEST_DESCRIP"]).value
            url = self.table.cell(row, col["URL"]).value
            test_data = self.table.cell(row, col["TESTDATA"]).value
            ex_code = self.table.cell(row, col["EXPECTCODE"]).value
            ex_mess = self.table.cell(row, col["EXPECTMESS"]).value
            encryp = self.table.cell(row, col["ENCRYPT"]).value
            condi = self.table.cell(row, col["CONDITION"]).value
            status = self.table.cell(row, col["ACTIVE"]).value
            if "y" in status and encryp:
                for i in (no, test_des, url, ex_code, ex_mess, condi):
                    item.append(i)
                #encrypt data and then insert it to the test_info list
                test_data = json.loads(test_data)
                encrypted = comm.crypt(flag=1, app_id=test_data["app_id"], data=test_data["data"])
                test_data["data"] = encrypted
                item.insert(col["TESTDATA"], json.dumps(test_data))
            elif "y" in status and not encryp:
                for i in (no, test_des, url, ex_code, ex_mess, condi):
                    item.append(i)
                #directly insert test data into test_info list
                item.insert(col["TESTDATA"], json.dumps(test_data))
            else:
                continue
            test_info.append(item)
            item = []
        print test_info
        return test_info

    # def get_single_wrong_para(self, start=1):
    #     col = para.excel_map
    #     for row in range(start, self.table.nrows):
    #         data = self.table.cell(row, col["TESTDATA"]).value
    #         data = json.loads(data)
    #         keys = data.keys()
    #         for key in keys:
    #             para.MATERIAL_LIST_PARA[key] = data[key]
    #         print para.MATERIAL_LIST_PARA


if __name__ == "__main__":
    teste = ExcelOperation("para_wrong")
    #teste.get_single_wrong_para()
    teste.all_test_info()
