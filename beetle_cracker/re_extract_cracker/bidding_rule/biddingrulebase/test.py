#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  8 11:05:21 2021

@author: morning
"""
import json
from beetle_cracker.re_extract_cracker.bidding_rule.biddingrulebase.bidding_rb import html_process
import random
from bs4 import BeautifulSoup
from beetle_cracker.re_extract_cracker.bidding_rule.biddingrulebase.bidding_rb.pipeline import Pipeline
import re
import pandas as pd



# file = 'data/招投标通用_test1.json'
# data = []
# with open(file, 'r') as f:
#     for line in f.readlines():
#         line = line.strip()
#         data.append(json.loads(line))
#
# # 单条数据的索引
#
# index = 469
#
# url = data[index-2+4]['biddingPageImage']
# page = data[index-2+4]['content']
# title = data[index-2+4]['title']
#
# text = BeautifulSoup(page, 'lxml').get_text()
# #title = BeautifulSoup(page, 'lxml').find('div')
# tables = html_process.extract_table(page)
#
# pipeline = Pipeline()
# result = pipeline.debug4url(url, page, title)
# print(result)

if __name__ == '__main__':
    from utils.sql import findBidding
    from utils.time import ymdToTs
    # 提取
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
        result = pipeline.debug4url(url, page, title)
        print(result)


    