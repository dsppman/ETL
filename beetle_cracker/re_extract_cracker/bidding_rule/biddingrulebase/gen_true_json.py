#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  8 11:43:14 2021

@author: morning
"""

import pandas as pd
import json

if __name__ == '__main__':
    file = '招投标通用_test1'
    file_xlsx = '{}.xlsx'.format(file)
    data = pd.read_excel('data/'+file_xlsx, dtype=str)

    
    data['采购单位'] = data['招标单位名称``招标单位联系人``招标单位联系方式'].map(lambda x: x.strip().split('``')[0].strip(), 'ignore')
    data['招标单位联系人'] = data['招标单位名称``招标单位联系人``招标单位联系方式'].map(lambda x: x.strip().split('``')[1].strip(), 'ignore')
    data['招标单位联系方式'] = data['招标单位名称``招标单位联系人``招标单位联系方式'].map(lambda x: x.strip().split('``')[2].strip(), 'ignore')
    
    data['代理机构名称'] = data['代理机构名称``代理机构联系人``代理机构联系方式'].map(lambda x: x.strip().split('``')[0].strip(), 'ignore')
    data['代理机构联系人'] = data['代理机构名称``代理机构联系人``代理机构联系方式'].map(lambda x: x.strip().split('``')[1].strip(), 'ignore')
    data['代理机构联系方式'] = data['代理机构名称``代理机构联系人``代理机构联系方式'].map(lambda x: x.strip().split('``')[2].strip(), 'ignore')

    data['项目联系人'] = data['项目联系人``项目联系方式'].map(lambda x: x.strip().split('``')[0].strip(), 'ignore')
    data['项目联系方式'] = data['项目联系人``项目联系方式'].map(lambda x: x.strip().split('``')[1].strip(), 'ignore')
    
    del data['招标单位名称``招标单位联系人``招标单位联系方式']
    del data['代理机构名称``代理机构联系人``代理机构联系方式']
    del data['项目联系人``项目联系方式']
    
    columns = ['采购单位', '招标单位联系人', '招标单位联系方式', '代理机构名称',
               '代理机构联系人', '代理机构联系方式', '项目联系人', '项目联系方式']
            
    c = 0
    data['biddingPageImage'] = data['fromurl']
    del data['fromurl']
    data['biddingSource'] = pd.Series(['通用']*len(data))
    with open('data/{}.json'.format(file), 'w', encoding='utf-8') as f:    
        for i in range(len(data)):
            if pd.isnull(data['采购单位'][i]):
                continue
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
            
        