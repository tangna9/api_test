#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/9 14:11
# @Author  : Tang Na
# @Site    : 
# @File    : comm.py
# @Software: PyCharm Community Edition


import requests
from confparser import cf
from conf import para
import json
import logging
from logging.config import fileConfig
__all__ = ['post_https', 'post_http']

fileConfig("../conf/logging.conf")
log = logging.getLogger("api")

host = cf().get("host", "hostIP")
h = para.headers
def post_https(url, data, headers=h):
    '''
    :param url: 请求url
    :param data: 请求数据
    :param headers: 请求headers
    :return:
    '''
    s = requests.Session()
    r = s.post(url=url, data=data, headers=headers, verify=False)
    log.debug("request:%s" %url)
    log.debug("request_data:%s" %data)
    log.debug("response:(code:%s)(mess:%s)" %(r.status_code, r.text))
    return r.status_code, r.text

def post_http(url, data, headers=h):
    '''
    :param url: 请求url
    :param data: 请求数据
    :param headers: 请求headers
    :return:
    '''
    r = requests.post(url=url, data=data, headers=headers)
    log.debug("request:%s" % url)
    log.debug("request_data:%s" %data)
    log.debug("response:(code:%s)(mess:%s)" % (r.status_code, r.text))
    return r.status_code, r.text

def get_sign(app_id=para.APPid, sdk_v=para.SDK_V, flag=1):
    '''
    :param app_id:
    :param sdk_v:
    :param flag: 1鉴权sign 2datasign
    :return: sign
    '''
    if flag == 1:
        url = cf().get("url", "SIGN1")
    else:
        url = cf().get("url", "SIGN2")
    url = "https://" + host + url
    r_data = para.SIGN_PARA
    r_data['app_id'] = app_id
    r_data['sdk_version'] = sdk_v
    re = post_https(url=url, data=r_data, headers=h)
    return re

def crypt(flag, app_id, data):
    '''
    :param flag: 1加密 2解密
    :param app_id:
    :param data:
    :return:
    '''

    r_data = para.CRYPT_PARA
    r_data["app_id"] = app_id
    if flag == 1:
        url = cf().get("url", "ENCRYPT")
        r_data["data"] = json.dumps(data)
    else:
        url = cf().get("url", "DECRYPT")
        r_data["data"] = data
    url = "http://" + host + url
    re = post_http(url=url, data=r_data, headers=h)
    return re

if __name__ == "__main__":

    encrypt_data = ""
    crypt(flag=2, app_id=para.APPid, data=encrypt_data)