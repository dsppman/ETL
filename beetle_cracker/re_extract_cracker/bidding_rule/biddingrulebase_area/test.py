# -*- coding: utf-8 -*-

import json
from pipeline import Pipeline


pipeline_ = Pipeline()

datas = []
with open('./data/招投标通用_train.json', 'r', encoding='utf-8') as f:
    contents = f.readlines()
    for con in contents:
        datas.append(json.loads(con))

# 单条数据的索引
index = 456
data = datas[index]
match_result = pipeline_.area_match(data['title'], data['content'])
print(match_result)
