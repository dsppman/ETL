# -*- coding: utf-8 -*-

from pipeline import Pipeline
from data.area import complete_address
from unit import read_json


def run_pipeline(file):
    datas = read_json(file)
    pl = Pipeline()
    pre_data = []
    true_data = []
    for item in datas:
        pre_result = pl.area_match(item['title'], item['content'])
        pre_data.append(pre_result)
        true_data.append(item['areaid'])
    return true_data, pre_data


def evaluate(true_data, pred_data):
    true_list = []
    false_list = []
    for areaid, pre in zip(true_data, pred_data):
        true_set = set(complete_address(areaid))
        pre_set = set([pre['province'], pre['city']])
        if None in pre_set:
            pre_set.remove(None)
        match = (true_set | pre_set) == true_set
        if match:
            true_list.append((true_set, pre))
        else:
            false_list.append((true_set, pre))
    p = len(true_list) / (len(true_list) + len(false_list))
    print('准确率：', p)


if __name__ == '__main__':
    file = './data/招投标通用_test.json'
    true_data, pre_data = run_pipeline(file)
    evaluate(true_data, pre_data)
