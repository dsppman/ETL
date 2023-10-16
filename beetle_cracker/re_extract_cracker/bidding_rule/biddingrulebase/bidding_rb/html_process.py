#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time

import pandas as pd
import requests
import logging

logger = logging.getLogger('html_process')

__driver__ = None


def download_page_test(url, selenium=False, selenium_timesleep=1):
    if selenium:
        page = download_page_test_use_selenium(url,
                                               timesleep=selenium_timesleep)
    else:
        html_source = requests.get(url, timeout=5)
        page = html_source.content.decode()
    return page


def download_page_test_use_selenium(url, timesleep=1):
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    option = Options()
    option.add_argument("--headless")
    __driver__ = Chrome(options=option, keep_alive=False)

    __driver__.get(url)
    time.sleep(timesleep)
    page = __driver__.page_source
    __driver__.close()
    return page


def extract_table(page):
    try:
        tables = pd.read_html(page, header=None)
    except Exception as e:
        # logger.warn(f'pandas read table error: {e}')
        tables = []
    if not tables:
        return []

    datas = []
    for table in tables:
        data = table.fillna('').to_numpy().tolist()
        columns = list(table.columns)
        if columns != list(range(len(columns))):
            data = [columns] + data

        if data:
            datas.append(data)
    return datas
