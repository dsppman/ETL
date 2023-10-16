#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  8 11:05:21 2021

@author: morning
"""

import json
from bidding_rb.pipeline_zhaobiao_money import Pipeline as zhaobiao
from bidding_rb.pipeline_zhongbiao_money import Pipeline as zhongbiao


file = 'data/招标金额_test.json'
data = []
with open(file, 'r') as f:
    for line in f.readlines():
        line = line.strip()
        data.append(json.loads(line))


if __name__ == '__main__':
    # 单条数据的索引
    index = 501
    url = data[index-1]['url']
    page = data[index-1]['content']
    # title = data[index-2]['title']

    pipeline_zhaobiao = zhaobiao()
    pipeline_zhongbiao = zhongbiao()
    result_zhaobiao = pipeline_zhaobiao.money_match(page)
    result_zhongbiao = pipeline_zhongbiao.money_match(page)
    print(result_zhaobiao)
    print(result_zhongbiao)

