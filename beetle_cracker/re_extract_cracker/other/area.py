#!/usr/bin/env python
# -*- coding: utf-8 -*-
from beetle_cracker.re_extract_cracker.bidding_rule.biddingrulebase_area.pipeline import Pipeline

pipeline = Pipeline()


def get_data(title, text, re_compiled_set):
    res = ""
    try:
        pre_result = pipeline.area_match(title, text)
    except Exception as e:
        pre_result = {}
    # if pre_result.get("province", ""):
    #     res += pre_result['province']
    # if pre_result.get("city", ""):
    #     res += pre_result["city"]
    # if pre_result.get("area", ""):
    #     res += pre_result['area']
    if len(pre_result) > 200:
        pre_result = ""
    res_dict = {"type": "area", "data": pre_result}
    return res_dict

if __name__ == '__main__':
    # todo 1.获取 省 市 区
    from utils.sql import findBidding
    from utils.time import ymdToTs
    # 提取
    arrFix = [('deb6a48f37a5431c90be1feac5a5b523', ymdToTs('2023-07-20'))]
    for (id, pbTime) in arrFix:
        bidding = findBidding(id, pbTime)

        url = bidding['source_url']
        page = bidding['snapshot']
        title = bidding['title']

        print(get_data(title,page,{}))
