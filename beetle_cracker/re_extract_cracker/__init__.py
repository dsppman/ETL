#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .utils import load_task
from beetle_cracker.common.time_out import time_out
import time

import logging

# logger = logging.getLogger("re_extarct_cracker")
# logger.setLevel(level=logging.INFO)
# log_path = '/re_extract_time_statistics.log'
# handler = logging.FileHandler(log_path)
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)


tasks = load_task()


class BeetleReExtractCrackerClient():
    _type_name = "bidding_re_extract"
    # todo 关闭日志
    def crack(self):
        return
    # def crack(self, data):
    #     start_crack_time = time.time()
    #     title = ""
    #     try:
    #         title = data['title'][0].decode("UTF-8")
    #         page = data['page'][0].decode("UTF-8")
    #         try:
    #             is_cache = data['is_cache'][0].decode("UTF-8")  # 是否缓存
    #         except Exception as e:
    #             is_cache = "1"
    #         start_re_time = time.time()
    #         res_data, exist = get_data(title, page, is_cache)
    #         re_time = time.time() - start_re_time
    #         result = {
    #             "data": res_data,
    #             "error_msg": "",
    #             "status": 1,
    #             "exist": exist
    #         }
    #     except Exception as e:
    #         result = {
    #             "data": "",
    #             "error_msg": "error extract",
    #             "status": 0,
    #             "exist": 0
    #         }
    #         re_time = "re_deal_error"
    #     end_crack_time = time.time()
    #     # 正则识别超过30s的 需要记录title用于后续排查
    #     if end_crack_time - start_crack_time > 30:
    #         logger.info("deail this re_request all_time:{}; re_time:{}; request more 1min:{}; title is:{};".format(
    #             end_crack_time - start_crack_time, re_time, end_crack_time - start_crack_time > 60, title
    #         ))
    #     else:
    #         logger.info("deail this re_request all_time:{}; re_time:{}; request more 1min:{}".format(
    #                 end_crack_time - start_crack_time, re_time, end_crack_time - start_crack_time > 60
    #             ))
    #     return result



def timeout_callback(e):
    print(e.msg)
    return {}, 0


@time_out(2, timeout_callback)
def get_data(title, page, is_cache):
    res_data, exist = tasks.thread_extract(title, page, is_cache)
    return res_data, exist
