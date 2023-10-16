#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io

import pandas as pd
from bs4 import BeautifulSoup


def get_pre_extract(page):
    try:
        tables = pd.read_html(io.StringIO(page), header=None)
    except Exception as e:
        tables = []

    datas = []
    for table in tables:
        data = table.fillna('').to_numpy().tolist()
        columns = list(table.columns)
        if columns != list(range(len(columns))):
            data = [columns] + data
        if data:
            datas.append(data)
    bs = BeautifulSoup(page, 'lxml')

    text = bs.get_text()
    return datas, text


from pandas.io.html import _LxmlFrameParser, _valid_parsers


class My_LxmlFrameParser(_LxmlFrameParser):
    def _parse_tbody_tr(self, table):
        from_tbody = table.xpath(".//tbody//tr")
        from_root = table.xpath("./tr")

        # HTML spec: at most one of these lists has content
        # 相比于原代码, 这里替换了顺序:
        #   因为发现某些网站的网页中, 表头会匹配到from_root中
        #   此处应当保证表头出现在内容之前, 不然会出现提取不到的情况
        #
        # todo: 需对此处进行更充分的测试, 以尽可能的适配各种类型网页
        return from_root + from_tbody


# _LxmlFrameParser = My_LxmlFrameParser

# 解析器替换为My_LxmlFrameParser
# _valid_parsers = {
#        "lxml": _LxmlFrameParser,
#        None: _LxmlFrameParser,
#        "html5lib": _BeautifulSoupHtml5LibFrameParser,
#        "bs4": _BeautifulSoupHtml5LibFrameParser,
#   }
_valid_parsers["lxml"] = My_LxmlFrameParser


def get_pre_extract_v2(page):
    try:
        tables = pd.read_html(io.StringIO(page), header=None)
    except Exception as e:
        tables = []
    datas = []
    for table in tables:
        data = table.fillna('').to_numpy().tolist()
        columns = list(table.columns)
        if columns != list(range(len(columns))):
            data = [columns] + data
        if data:
            datas.append(data)
    bs = BeautifulSoup(page, 'lxml')
    text = bs.get_text(separator=" ")
    return datas, text


def handle_special_string(text):
    text = text.replace(" ", "").replace("\n", "").replace("\r", "").replace("\t", "").replace("-", "")
    return text


def get_index(text, name):
    indexs = []
    if type(name) == str:
        count = text.count(name)
        start = 0
        length = len(name)
        end = len(text)
        try:
            for i in range(count):
                index = text.index(name, start, end)
                indexs.append(index)
                start = index + length + 1
        except Exception as e:
            pass
    return indexs


def repair_contact_name(name):
    res = ""
    if name[-1] not in ["市", "县", "省"]:
        res = name
    return res


if __name__ == "__main__":
    page = """
        Python index() 方法检测字符串中是否包含子字符串 str ，如果指定 beg（开始） 和 end（结束） 范围，则检查是否包含在指定范围内，该方法与 python find()方法一样，只不过如果str不在 string中会报一个异常。

    语法
    index()方法语法：

    str.index(str, beg=0, end=len(string))
    参数
    str -- 指定检索的字符串
    beg -- 开始索引，默认为0。
    end -- 结束索引，默认为字符串的长度。
    返回值index
    如果包含子字符串返回开始的索引值，否则抛出异常。
    """
    get_index(page, "index")
