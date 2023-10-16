#!/usr/bin/env python
# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
import json
import requests
import logging
import time
from utils.sql import findBidding
from utils.time import ymdToTs

extract_url = "http://127.0.0.1:8999/api/crack/bidding_re_extract"
retry_count = 3
max_thread = 8


def run():
    path = "/home/project/beetle_deploy/beetle_bidding_alg/test_data/re_extract_test.json"
    i = 0
    info_list = []
    executor = ThreadPoolExecutor(max_workers=max_thread + 1)
    with open(path, "r") as f:
        for line in f:
            info = json.loads(line.strip())
            if len(info_list) < max_thread:
                info_list.append(info)
            else:
                for extract_res in executor.map(request_extract_api, info_list):
                    if extract_res:
                        line = json.dumps(extract_res, ensure_ascii=False)
                        with open("./re_extract_res.json", "a+") as fw:
                            fw.write(line + "\n")
                info_list = [info]
                i += max_thread
                print(i)


def request_extract_api(data):
    extract_res = {}
    try:
        for i in range(retry_count):
            params = {
                "title": data.get("biddingAnncTitle"),
                "page": data.get("biddingPage")
            }
            response = requests.post(url=extract_url, data=params, timeout=3)
            if response.status_code == 200:
                json_data = json.loads(response.text).get("ret", {})
                if json_data.get("status", "") == 1:
                    if json_data.get("exist", "") == 1:
                        break
                    extract_res = {
                        "biddingSource": data['biddingSource'],
                        "biddingAnncType": data['biddingAnncType'],
                        "biddingAnncUrl": data['biddingAnncUrl'],
                        "biddingPageImage": data['biddingPageImage'],
                        "biddingProjectID": json_data.get("data", {}).get("biddingProjectID", ""),
                        "area": json_data.get("data", {}).get("area", ""),
                        "zhaobiao_list": json_data.get("data", {}).get("zhaobiao_list", []),
                        "zhongbiao_list": json_data.get("data", {}).get("zhongbiao_list", []),
                        "daili_list": json_data.get("data", {}).get("daili_list", []),
                        "budget": json_data.get("data", {}).get("budget", 0),
                        "winning_volume": json_data.get("data", {}).get("winning_volume", 0),
                    }

                    break
                else:
                    logging.info("return  extract data error {}".format(response.text))
            else:
                logging.info("status_code not 200")
            time.sleep(2)
    except Exception as e:
        logging.info("request_extract_api {}".format(e))
    print(extract_res)
    return extract_res


if __name__ == "__main__":
    run()
