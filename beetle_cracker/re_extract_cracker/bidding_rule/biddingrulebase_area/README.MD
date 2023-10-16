# 基于cpca模块从公告标题和正文中提取公告地址

## python版本
python3.6以上

## 项目结构
```shell
.
├── cpca                      # cpca模块
│  │── resources
│  │  ├── 56_nations.csv
│  │  ├── adcodes.csv
│  │  └── __init__.py
│  ├── drawer.py
│  ├── exceptions.py
│  ├── __init__.py
│  └── matcher.py
├── data                     # 存放数据
│  ├── area.py               # 本地用的地址映射
│  ├── 招投标通用_test.json    
│  └── 招投标通用_train.json
├── LICENSE
├── local-sync.py
├── main.py                       # 提取批量数据，计算准确率
├── Makefile
├── MANIFEST.in
├── pipeline.py                   # 主函数，实体提取的整个流程
├── Pipfile
├── README.MD
├── requirements.txt
├── setup.py
├── sync.py
├── test.py                       # 提取单条数据
├── tests                         # 单元测试模块
│  ├── addr.csv
│  ├── __init__.py
│  ├── test_cpca.py
│  ├── test_drawer.py
│  ├── test_matcher.py
│  └── test_structures.py
└── unit.py                       # 数据的读取函数
```

## 调用方式(如test.py)

1.调用pipline.Pipeline.area_match方法<br>
2.输入 __公告标题__ 和 __公告正文__ 两个参数<br>
3.输出结果为一个字典，包含省、市、区县， 有如下几种情况：<br>
{'province': '广东省', 'city': '广州市', 'area': '番禺区'}<br>
{'province': '广东省', 'city': '广州市', 'area': None}<br>
{'province': '广东省', 'city': None, 'area': None}<br>
{'province': None, 'city': None, 'area': None}<br>


```python
# -*- coding: utf-8 -*-
# test.py
import json
from pipeline import Pipeline


pipeline_ = Pipeline()

datas = []
with open('./data/招投标通用_train.json', 'r', encoding='utf-8') as f:
    contents = f.readlines()
    for con in contents:
        datas.append(json.loads(con))

# 单条数据的索引
index = 450
data = datas[index]
match_result = pipeline_.area_match(data['title'], data['content'])
print(match_result)
```

##了解cpca模块更多信息

[一个用于提取简体中文字符串中省，市和区并能够进行映射，检验和简单绘图的python模块](https://github.com/DQinYuan/chinese_province_city_area_mapper)