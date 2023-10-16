#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  8 11:05:21 2021

@author: morning
"""

import json
from utils.sql import findBidding
from utils.time import ymdToTs
from beetle_cracker.re_extract_cracker.bidding_rule.biddingrulebase_zhongbiao.bidding_rb import html_process
import random
from bs4 import BeautifulSoup
from beetle_cracker.re_extract_cracker.bidding_rule.biddingrulebase_zhongbiao.bidding_rb.pipeline import Pipeline
import re


# file = 'data/中标通用_test.json'
# data = []
# with open(file, 'r') as f:
#     for line in f.readlines():
#         line = line.strip()
#         data.append(json.loads(line))


# if __name__ == '__main__':
#     # 单条数据的索引
#     index = 265
#     url = data[index-2]['url']
#     page = data[index-2]['content']
#     # title = data[index-2]['title']
#
#
#     # text = BeautifulSoup(page, 'lxml').get_text()
#     # #title = BeautifulSoup(page, 'lxml').find('div')
#     # tables = html_process.extract_table(page)
#
#     pipeline = Pipeline()
#     result = pipeline.debug4url(url, page)
#     print(result)

 
# 单条数据的索引
# index = 478
# bias = 4
# url = data[index-2+bias]['biddingPageImage']
# page = data[index-2+bias]['content']
# title = data[index-2+bias]['title']
#
# text = BeautifulSoup(page, 'lxml').get_text()
# #title = BeautifulSoup(page, 'lxml').find('div')
# tables = html_process.extract_table(page)
#
# pipeline = Pipeline()
# result = pipeline.debug4url(url, page)
# print(result)


if __name__ == '__main__':
    arrFix = [('deb6a48f37a5431c90be1feac5a5b523', ymdToTs('2023-07-20'))]
    for (id, pbTime) in arrFix:
        bidding = findBidding(id, pbTime)
        print(bidding)

        url = bidding['source_url']
        page = bidding['snapshot']
        title = bidding['title']

        text = BeautifulSoup(page, 'lxml').get_text()
        # title = BeautifulSoup(page, 'lxml').find('div')
        tables = html_process.extract_table(page)

        pipeline = Pipeline()
        result = pipeline.debug4url(url, page)
        print(result)