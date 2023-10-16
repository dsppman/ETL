#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bidding_rb.utils import read_json, dump_json
# from bidding_rb.pipeline import Pipeline
from bidding_rb.pipeline_conatct_person import Pipeline
from copy import deepcopy
from tqdm import tqdm
import pandas as pd


def run_pipeline(data_path):
    pipeline = Pipeline()
    datas = read_json(data_path)

    count = 0

    final = list()

    pred_datas = []
    for data in tqdm(datas):
        count = count + 1
        data = deepcopy(data)
        data.pop('招标单位联系人', '')
        url = data.get('biddingPageImage', None)
        page = data.get('content', None)
        title = data.get('title', None)
        try:
            result = pipeline.debug4url(url, page, title)
            # print('result: %s ' % result)
            data['招标单位联系人'] = list({i['text'] for i in result})
            data['source'] = list({i['source'] for i in result})
            # print('处理后的招标联系人: %s ' % data['招标联系人'])
            data['message'] = 'success'
            final.append(result)
        except Exception as e:
            print('exception: %s ' % str(e))
            data['message'] = str(e)
        pred_datas.append(data)
        # print('===================================')
        # if count >= 1:
        #     break
    # print('final: %s ' % final)
    save_path = data_path.replace('.json', '_pred.json')
    dump_json(pred_datas, save_path)
    # print('pred_datas: %s ' % pred_datas)


def evaluate(true_data_path, pred_data_path):
    true_datas = read_json(true_data_path)
    pred_datas = read_json(pred_data_path)
    
    url2true_data = {data['biddingPageImage']: data for data in true_datas}
    url2pred_data = {data['biddingPageImage']: data for data in pred_datas}
    true_set = set()
    pred_set = set()
    datas = []
    for url in url2true_data.keys():
        true_data = url2true_data[url]
        pred_data = url2pred_data[url]
        y_true = set(true_data.get('招标单位联系人', []))
        y_pred = set(pred_data.get('招标单位联系人', []))
        content = pred_data.get('content')
        if not y_pred:
            y_pred_index = ''
        else:
            if list(y_pred)[0] in content:
                y_pred_index = content.index(list(y_pred)[0], 0, len(content))
            else:
                y_pred_index = ''
        miss = y_true - y_pred
        error = y_pred - y_true

        match = y_true == y_pred

        true_set.update({(url, i) for i in y_true})
        pred_set.update({(url, i) for i in y_pred})

        datas.append({
            'source': true_data['biddingSource'],
            'biddingPageImage': true_data['biddingPageImage'],
            'y_true': '\n'.join(sorted(y_true)),
            'y_pred': '\n'.join(sorted(y_pred)),
            'y_pred_index': '\n'.join(sorted(str(y_pred_index))),
            'miss': '\n'.join(sorted(miss)),
            'error': '\n'.join(sorted(error)),
            'match': match,
            'source_found': pred_data.get('source', ''),
            'result': pred_data.get('message', '')
        })
        
    metrics, miss, error = calc_metrics(true_set, pred_set)
    print(metrics)
    report_path = pred_data_path.replace('.json', '_report.xlsx')

    excel_writer = pd.ExcelWriter(report_path, engine='openpyxl')

    # metrics, miss, error = calc_metrics(true_set, pred_set)
    # print(metrics)
    metrics_df = pd.DataFrame([metrics], index=['招标单位联系人'])
    metrics_df.to_excel(excel_writer, sheet_name='metrics')

    datas_df = pd.DataFrame(datas)
    datas_df.to_excel(excel_writer, sheet_name='detail', index=False)

    excel_writer.close()
    return miss, error


def calc_metrics(set_true, set_pred):
    cross = set_true & set_pred
    error = (set_pred | set_true) - (set_pred & set_true)
    miss = set_true - set_pred
    error = set_pred - set_true
    precision = len(cross) / (len(set_pred) + 1e-5)
    recall = len(cross) / (len(set_true) + 1e-5)
    f1 = 2 * precision * recall / (precision + recall + 1e-5)
    metrics = {'precision': precision, 'recall': recall, 'f1': f1}
    return metrics, miss, error                                                                                                                                                 

"""

提取招标单位联系人/联系方式，准确率指标0.91，召回率指标0.90
提取中标单位联系人/联系方式（仅限中标公告），准确率指标0.90，召回率指标0.92
提取代理机构联系人/联系方式，准确率指标0.85，召回率指标0.85

test:   {'precision': 0.622559639423869, 'recall': 0.7592592391730361, 'f1': 0.6841428276542681}
        {'precision': 0.8907103338409653, 'recall': 0.7652581800348273, 'f1': 0.823227310381004}


train:  {'precision': 0.8372092861005953, 'recall': 0.901878895576641, 'f1': 0.8683366980312865}

"""
if __name__ == "__main__":
    # file = '招投标通用_train'
    file = '招投标通用_test'
    # file = '招投标通用_train_backup'
    run_pipeline('data/{}.json'.format(file))
    evaluate('data/{}.json'.format(file), 'data/{}_pred.json'.format(file))
