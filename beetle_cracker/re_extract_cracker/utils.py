#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import traceback
from datetime import datetime
import json
import click
from concurrent.futures import ThreadPoolExecutor, as_completed
from beetle_cracker.re_extract_cracker.other.area import get_data as get_area
from beetle_cracker.re_extract_cracker.other.bidding_project_id import get_data as get_project_id
from beetle_cracker.re_extract_cracker.daili.daili import get_data as get_daili
from beetle_cracker.re_extract_cracker.daili.daili_contact_name import get_data as get_daili_contact_name
from beetle_cracker.re_extract_cracker.daili.daili_contact_phone import get_data as get_daili_contact_phone
from beetle_cracker.re_extract_cracker.zhaobiao.zhaobiao import get_data as get_zhaobiao
from beetle_cracker.re_extract_cracker.zhaobiao.zhaobiao_contact_name import get_data as get_zhaobiao_contact_name
from beetle_cracker.re_extract_cracker.zhaobiao.zhaobiao_contact_phone import get_data as get_zhaobiao_contact_phone
from beetle_cracker.re_extract_cracker.zhongbiao.zhongbiao import get_data as get_zhongbiao
from beetle_cracker.re_extract_cracker.zhongbiao.zhongbiao_contact_name import get_data as get_zhongbiao_contact_name
from beetle_cracker.re_extract_cracker.zhongbiao.zhongbiao_contact_phone import get_data as get_zhongbiao_contact_phone
from beetle_cracker.re_extract_cracker.other.get_budget import get_data as get_budget
from beetle_cracker.re_extract_cracker.other.winning_volume import get_data as get_winning_volume
from beetle_cracker.re_extract_cracker.common.group_org import group_by_org, across_exam
from beetle_cracker.re_extract_cracker.common.utils import get_pre_extract, get_pre_extract_v2
from functools import wraps
import time

source_name = "rextract"
project_path = "/home/lgmi/interface/flask_interface"


def time_decorator(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        start = time.time()
        doing = f(*args, **kwargs)
        end = time.time()
        data = "time:{} page:{}".format("%.2f" % (end - start), args[2])
        if int(end - start) > 2:
            with open("re_extract_time.log", "a+") as fw:
                fw.write(data + "\n")
            # exit("time out")
        return doing

    return decorated


class Tasks(object):
    def __init__(self, _redis, logger):
        self._redis = _redis
        self.logger = logger


    def log(self):
        return self.logger

    def get_redis_data(self, md5_id):
        key = "{}_bidding_cache".format(source_name)
        str_result = self._redis.hget(key, md5_id)
        return json.loads(str_result)

    def set_redis_data(self, md5_id, json_result):
        key = "{}_bidding_cache".format(source_name)
        self._redis.hset(key, md5_id, json.dumps(json_result, ensure_ascii=False))
        if self._redis.ttl(key) == -1:
            self._redis.expire(key, 86400 * 4)
            # extime = datetime.datetime.now().strftime('%Y-%m-%d') + " 16:00:00"
            # extime = int(time.mktime(time.strptime(extime, '%Y-%m-%d %H:%M:%S')))
            # self._redis.expireat(key, extime)

    # @time_decorator
    def thread_extract(self, title, page, is_cache="1"):
        exist = 0
        # md5_id = hashlib.md5(page.encode("utf8")).hexdigest()
        # if is_cache == "1":
        #    try:
        #        res = self.get_redis_data(md5_id)
        #        exist = 1
        #    except:
        #        res = {}
        #    res = {}
        # else:
        #    res = {}
        res = {}
        if not res:
            wait_group_data = {}
            re_compiled_set = {}
            tables, text = get_pre_extract(page)
            tables_v2, text_v2 = get_pre_extract_v2(page)

            if len(text) > 50:
                with ThreadPoolExecutor(max_workers=13) as t:
                    obj_list = []
                    # 获取项目 省份 城市 区
                    task = t.submit(get_area, title, page, re_compiled_set)
                    obj_list.append(task)
                    # 获取招标编号
                    task = t.submit(get_project_id, text_v2, tables_v2)
                    obj_list.append(task)
                    # 获取代理机构名称
                    task = t.submit(get_daili, tables, text, re_compiled_set)
                    obj_list.append(task)

                    task = t.submit(get_daili_contact_name, tables, text, re_compiled_set)
                    obj_list.append(task)

                    task = t.submit(get_daili_contact_phone, tables, text, re_compiled_set)
                    obj_list.append(task)

                    task = t.submit(get_zhaobiao, tables_v2, text_v2, title, re_compiled_set)
                    obj_list.append(task)

                    task = t.submit(get_zhaobiao_contact_name, tables, text, re_compiled_set)
                    obj_list.append(task)

                    task = t.submit(get_zhaobiao_contact_phone, tables, text, re_compiled_set)
                    obj_list.append(task)

                    task = t.submit(get_zhongbiao, tables_v2, text_v2, re_compiled_set)
                    obj_list.append(task)

                    task = t.submit(get_zhongbiao_contact_name, tables, text, re_compiled_set)
                    obj_list.append(task)

                    task = t.submit(get_zhongbiao_contact_phone, tables, text, re_compiled_set)
                    obj_list.append(task)

                    task = t.submit(get_budget, tables_v2, text_v2, re_compiled_set)
                    obj_list.append(task)

                    task = t.submit(get_winning_volume, tables_v2, text_v2, re_compiled_set)
                    obj_list.append(task)

                    for future in as_completed(obj_list, timeout=2):
                        return_data = future.result()
                        if return_data.get("type") == "area":
                            if return_data.get("data", ""):
                                res['area'] = return_data.get('data', "")
                        elif return_data.get("type") == "project_id":
                            if return_data.get("data", ""):
                                res['biddingProjectID'] = return_data.get('data', "")

                        elif return_data.get("type") == "daili":
                            wait_group_data['daili'] = return_data.get('data', "")
                        elif return_data.get("type") == "daili_contact_name":
                            wait_group_data['daili_contact_name'] = return_data.get('data', "")
                        elif return_data.get("type") == "daili_contact_phone":
                            wait_group_data['daili_contact_phone'] = return_data.get('data', "")

                        elif return_data.get("type") == "zhaobiao":
                            wait_group_data['zhaobiao'] = return_data.get('data', "")
                        elif return_data.get("type") == "zhaobiao_contact_name":
                            wait_group_data['zhaobiao_contact_name'] = return_data.get('data', "")
                        elif return_data.get("type") == "zhaobiao_contact_phone":
                            wait_group_data['zhaobiao_contact_phone'] = return_data.get('data', "")

                        elif return_data.get("type") == "zhongbiao":
                            wait_group_data['zhongbiao'] = return_data.get('data', "")
                        elif return_data.get("type") == "zhongbiao_contact_name":
                            wait_group_data['zhongbiao_contact_name'] = return_data.get('data', "")
                        elif return_data.get("type") == "zhongbiao_contact_phone":
                            wait_group_data['zhongbiao_contact_phone'] = return_data.get('data', "")

                        elif return_data.get("type") == "budget":
                            if len(return_data.get('data', [])) == 1:
                                if return_data['data'][0].get("value", 0):
                                    res['budget'] = return_data['data'][0].get("value")

                        elif return_data.get("type") == "winning_volume":
                            winning_volume = 0
                            for item in return_data.get("data", []):
                                if item.get("value", 0):
                                    winning_volume += float(item['value'])
                            if winning_volume > 100:
                                res["winning_volume"] = winning_volume

                wait_group_data['zhaobiao'] = across_exam(wait_group_data.get("daili", []), wait_group_data.get("zhaobiao", []))

                zhongbiao_list = group_by_org(
                    wait_group_data.get("zhongbiao", []),
                    wait_group_data.get("zhongbiao_contact_name", []),
                    wait_group_data.get("zhongbiao_contact_phone", []),
                    "zhongbiao",
                )
                zhaobiao_list = group_by_org(
                    wait_group_data.get("zhaobiao", []),
                    wait_group_data.get("zhaobiao_contact_name", []),
                    wait_group_data.get("zhaobiao_contact_phone", []),
                    "zhaobiao"
                )
                daili_list = group_by_org(
                    wait_group_data.get("daili", []),
                    wait_group_data.get("daili_contact_name", []),
                    wait_group_data.get("daili_contact_phone", []),
                    "daili"
                )
                if zhongbiao_list:
                    res["zhongbiao_list"] = zhongbiao_list
                if zhaobiao_list:
                    res["zhaobiao_list"] = zhaobiao_list
                if daili_list:
                    res['daili_list'] = daili_list
                # if res and is_cache == "1":
                #    try:
                #        self.set_redis_data(md5_id, res)
                #    except:
                #        pass
        return res, exist



def load_task():
    # todo 关闭日志
    return
    # redis_pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    # _redis = redis.Redis(connection_pool=redis_pool)
    # logger = logging.getLogger(__name__)
    # logger.setLevel(level=logging.INFO)
    # log_path = '{}/logs/{}.log'.format(project_path, source_name)
    # handler = logging.FileHandler(log_path)
    # handler.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
    # tasks = Tasks(_redis, logger)
    # return tasks


from beetle_cracker.re_extract_cracker.common.time_out import time_out, time_out_gevent


def timeout_callback(e):
    print("run func timeout")
    return {}, 0


@time_out_gevent(1, timeout_callback)
def get_data(tasks, title, page, is_cache):
    res_data, exist = tasks.thread_extract(title, page, is_cache)
    return res_data, exist


def run():
    import json
    project_path = "/home/gzw/project/beetle_deploy/beetle_bidding_alg"
    project_path = "D://qike//beetle_bidding_alg"
    
    path = "{}/test_data/re_extract_test.json".format(project_path)
    tasks = load_task()
    with open(path, "r") as f:
        for line in f:
            item = json.loads(line.strip())
            if item.get("biddingPage", ""):
                res_data, exist = get_data(tasks, item.get("biddingAnncTitle"), item.get("biddingPage"), "0")
                print(res_data)


import pandas as pd


def run_test_analy():
    path = '/Users/ronniehwang/projects/beetle_bidding_alg/外包标注数据 - 招投标（修1）.xlsx'
    from pprint import pprint
    from bidding_rule.biddingrulebase.bidding_rb.html_process import download_page_test, extract_table
    import os

    oss_base = ''
    root = ""

    data = pd.read_excel(path)
    tasks = load_task()
    count = 0
    ta = tb = tc = xa = xb = xc = ya = yb = yc = 0
    for item in data.iterrows():
        count += 1
        oss_tail = item[1][1]
        if pd.isna(oss_tail):
            continue

        if 'spider/S998.html' != oss_tail:
            continue
        # if count < 180:
        #     continue
        # if count < 150:
        #     continue
        zhongbiao = []
        agent = []
        zhaobiao = [{'name': item[1][4], 'contact_name': item[1][5], 'phone': item[1][6]}]
        agent.append({'name': item[1][7], 'contact_name': item[1][8], 'phone': item[1][9]})
        index = 10
        while index <= len(item[1]) - 1:
            zhongbiao_item = {'name': item[1][index], 'contact_name': item[1][index + 1], 'phone': item[1][index + 2]}
            if not pd.isna(zhongbiao_item['name']):
                zhongbiao.append(zhongbiao_item)
            index += 3

        if not pd.isna(oss_tail) and oss_tail:

            oss_url = oss_base + oss_tail
            file_name = oss_url[oss_url.rindex('/') + 1:]
            page = None
            for root, dirs, files in os.walk(root):
                for file in files:
                    if file_name == file:
                        with open(root + file, 'r') as f:
                            page = f.read()
            if not page:
                page = download_page_test(oss_url)
                with open(root + file_name, 'w+') as f:
                    f.write(page)
            res = ''
            try:
                res = tasks.thread_extract("", page)
            except TypeError as e:
                print('--- can NOT extract file %s: %s' % (count, oss_tail))
                traceback.print_exc()

            if not res:
                continue
            print('---%s: %s' % (count, oss_tail))
            a, b, c, d = compare('代理', res[0].get('daili_list', []), agent)
            ta += a
            tb += b
            tc += c
            a, b, c, d = compare('招标', res[0].get('zhaobiao_list', []), zhaobiao)
            xa += a
            xb += b
            xc += c
            a, b, c, d = compare('中标', res[0].get('zhongbiao_list', []), zhongbiao)
            ya += a
            yb += b
            yc += c
    t_total = ta + tb + tc
    x_total = xa + xb + xc
    y_total = ya + yb + yc
    a_total = ta + xa + ya
    b_total = tb + xb + yb
    c_total = tc + xc + yc
    total = t_total + x_total + y_total
    print('-----total------')
    print('总共数量: {}, 解析数量:{}, 召回率: {:.2%}, 准确率: {:.2%}'.format(
        total, a_total + b_total, 1 - c_total / total, a_total / (a_total + b_total)))
    if t_total:
        print('代理 match: {} {:.2%} not match: {} {:.2%}  miss: {} {:.2%}'.format(
            ta, ta / t_total, tb, tb / t_total, tc, tc / t_total))
    if x_total:
        print('招标 match: {} {:.2%} not match: {} {:.2%}  miss: {} {:.2%}'.format(
            xa, xa / x_total, xb, xb / x_total, xc, xc / x_total))
    if y_total:
        print('中标 match: {} {:.2%} not match: {} {:.2%}  miss: {} {:.2%}'.format(
            ya, ya / y_total, yb, yb / y_total, yc, yc / y_total))


def compare(tag, xp_result, bi_result):
    if len(xp_result) != len(bi_result):
        print(tag + ' length NOT equal, 解析: %s, 标注: %s' % (len(xp_result), len(bi_result)))
    else:
        # print(tag + ' length equal ')
        pass
    match_cnt = 0
    mismatch_cnt = 0
    miss_cnt = 0
    invalid_cnt = 0
    for bi_item in bi_result:
        if pd.isna(bi_item.get('name', '')):
            continue
        bi_name = bi_item.get('name', '').strip().replace(' ', '').replace('\xa0', '')
        bi_phone = bi_item.get('phone', '')
        bi_phone = '' if pd.isna(bi_phone) else str(bi_phone).strip().replace(' ', '').replace('无', '')

        if not bi_phone:
            continue

        found = False
        for xp_item in xp_result:
            xp_name = xp_item.get('name')
            if xp_name == bi_name:
                found = True
                xp_phone = xp_item.get('contact', [{}])[0].get('contact_phone', '')

                # 解析、标注的电话号码可能有多个，先将多个电话转换为列表
                def change_phone_to_list(phone):
                    if phone[4:6] == '- ':  # 0595- 22766369
                        phone = phone.replace(' ', '')
                    phone_str = re.sub(r'[、/， ]', ',', phone.strip())
                    phone_ls = [i.strip() for i in phone_str.split(',') if i.strip()]
                    # 0898-65328224 转换为 089865328224
                    new_phone_ls = []
                    for i in phone_ls:
                        if i[0] == '0' and i[4] == '-':
                            i = i.replace('-', '')
                        new_phone_ls.append(i)
                    return list(set(new_phone_ls))

                algorithm_phone_ls = change_phone_to_list(xp_phone)
                standard_phone_ls = change_phone_to_list(bi_phone)

                # if re.sub(r"\s|、|,|\-|转", '', xp_phone) == re.sub(r"\s|、|,|\-|转", '', bi_phone):
                if set(algorithm_phone_ls) == set(standard_phone_ls):
                    match_cnt += 1
                    # print(tag + ' match ' + xp_name)
                else:
                    # if bi_phone and not xp_phone or xp_phone in bi_phone:
                    # 判断算法比标注的结果少
                    if not algorithm_phone_ls and set(algorithm_phone_ls) < set(standard_phone_ls):
                        print(tag + ' MISS ' + xp_name + " 解析结果:" + xp_phone + " 标注结果:" + bi_phone)
                        miss_cnt += 1
                    else:
                        print(tag + ' NOT MATCH ' + xp_name + " 解析结果:" + xp_phone + " 标注结果:" + bi_phone)
                        mismatch_cnt += 1
        if not found:
            if bi_phone:
                miss_cnt += 1
                print(tag + ' NOT contain ent ' + bi_name + " " + bi_phone)
            else:
                invalid_cnt += 1
    return match_cnt, mismatch_cnt, miss_cnt, invalid_cnt


def run_test_get_re_result():
    """
    获取re正则的提取结果，不需要与标注的做比较
    """
    path = ''
    from beetle_cracker.re_extract_cracker.bidding_rule.biddingrulebase.bidding_rb.html_process import download_page_test, extract_table
    import os

    oss_base = ''
    root = ""

    data = pd.read_excel(path)
    tasks = load_task()
    count = 0
    for item in data.iterrows():
        count += 1
        res = {
            'biddingAnncUrl': item[1][0],
            'biddingPageImage': item[1][1],
            'biddingSource': item[1][2],
            'import_update_time': item[1][3],
            'create_time': item[1][4],
            'biddingAnncType': item[1][5],
            '_id': item[1][6],
        }

        oss_tail = item[1][1]
        if pd.isna(oss_tail):
            continue

        if 'spiderl' != oss_tail:
            continue
        # if count < 1865:
        #     continue

        if not pd.isna(oss_tail) and oss_tail:
            oss_url = oss_base + oss_tail
            file_name = oss_url[oss_url.rindex('/') + 1:]
            page = None
            for root, dirs, files in os.walk(root):
                for file in files:
                    if file_name == file:
                        with open(root + file, 'r') as f:
                            page = f.read()
            if not page:
                page = download_page_test(oss_url)
                with open(root + file_name, 'w+') as f:
                    f.write(page)
            re_result = ''
            try:
                re_result = tasks.thread_extract("", page)
                if re_result:
                    res.update(re_result[0])
            except TypeError as e:
                print('--- can NOT extract file %s: %s' % (count, oss_tail))
                traceback.print_exc()
        print('---%s: %s' % (count, oss_tail))
        with open('', 'a+') as f:
            f.write('{}\n'.format(json.dumps(res, ensure_ascii=False)))


@click.command()
@click.option('--input_path')
@click.option('--output_path')
def run_origin_test_get_re_result(input_path, output_path):
    """
    直接读取文本内容进行提取
    """
    # root_path = "/tmp/leisl/beetle_bidding_alg/beetle_cracker/re_extract_cracker/"
    # input_path = root_path + "data/导出Bidding表未提取的数据_2022-02-16_00_dc"
    # output_path = root_path + "output/导出Bidding表未提取的数据_2022-02-16_00_dc_result4.json"

    tasks = load_task()
    count = 0

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("start get re result time:{}".format(current_time))
    import time
    start = time.time()
    with open(input_path, 'r') as in_f, open(output_path, 'w') as out_f:
        for line_data in in_f:
            count += 1
            try:
                line_json_data = json.loads(line_data)
                page = line_json_data.get('biddingPage', '')
                if page:
                    res = {
                        'biddingAnncUrl': line_json_data.get('biddingAnncUrl'),
                        'biddingSource': line_json_data.get('biddingSource'),
                        'biddingAnncType': line_json_data.get('biddingAnncType'),
                        'import_update_time': line_json_data.get('import_update_time'),
                        'create_time': line_json_data.get('create_time'),
                        '_id': line_json_data.get('_id'),
                    }
                    re_result = tasks.thread_extract("", page)
                    if re_result:
                        res.update(re_result[0])
                        out_f.write('{}\n'.format(json.dumps(res, ensure_ascii=False)))
            except Exception as e:
                print("[Exception]:" + str(e))

            if count % 100 == 0:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print("get re result count:{} time:{}".format(count, current_time))

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("end get re result time:{}".format(current_time))
    print("%s 条数据, spent: %s s" % (count, time.time() - start))


if __name__ == "__main__":
    # run()
    run_test_analy()
    # run_test_get_re_result()
    # run_origin_test_get_re_result()

