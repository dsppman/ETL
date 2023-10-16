#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  8 11:43:14 2021

@author: morning
"""

import pandas as pd
import json

if __name__ == '__main__':
    file = 'data/中标单位'
    file_xlsx = '{}.xlsx'.format(file)
    data = pd.read_excel(file_xlsx, dtype=str)

    data['中标单位名称'] = data['中标单位名称``中标单位联系人``中标单位联系方式'].map(lambda x: x.strip().split('``')[0].strip(), 'ignore')
    data['中标单位联系人'] = data['中标单位名称``中标单位联系人``中标单位联系方式'].map(lambda x: x.strip().split('``')[1].strip(), 'ignore')
    data['中标单位联系方式'] = data['中标单位名称``中标单位联系人``中标单位联系方式'].map(lambda x: x.strip().split('``')[2].strip(), 'ignore')

    del data['中标单位名称``中标单位联系人``中标单位联系方式']
    columns = ['中标单位名称', '中标单位联系人', '中标单位联系方式']




    c = 0
    with open('{}.json'.format(file), 'w', encoding='utf-8') as f:    
        for i in range(len(data)):
            tmp = {}
            for j in list(data.columns):
                if j in columns:
                    d = data[j][i].split(';')
                    tmp[j] = [x for x in d if x != '!']
                else:
                    tmp[j] = data[j][i]
            c += 1
            json.dump(tmp, f, ensure_ascii=False)
            f.write('\n')
