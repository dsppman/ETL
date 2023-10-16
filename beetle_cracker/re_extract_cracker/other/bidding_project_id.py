#!/usr/bin/env python
# -*- coding: utf-8 -*-

from beetle_cracker.re_extract_cracker.bidding_rule.biddingrule_number.export_project_number_extraction import handler_contains_value
import re

keywords = [
    u'采购单编号',
    u'项目编号',
    u"项目编码",
    u'招标编号',
    u'询价单编号',
    u"询价单号",
    u'采购编号',
    u'项目标号',
    u'发包编号',
    u'公告编号',
    u'项目号',
    u'工程编号',
    u'项目代码',
    u'信息编码',
    u'征询编号',
    u'任务编号',
    u'备案文号',
    u'比选代理编号',
    u'招标登记编号',
    u'报建编号',
    u'寻源单据号',
    u'寻源单号',
    u"申购单号",
    u"反拍单号",
    u"询价书编号",
    u"询价编号",
    u"比价编号",
    u"计划编号",
    u"登记编号",
    u"公示编号",
    u"标段编号",
    u"竞价编号",
    u"包编号",
    u"标段（包）编号",
    u"标段(包)编号",
    u'标段编号',
    u'交易编号',
    u"备案号",
    u"计划明细编号",
    u'合同编号',
    u'合同号（订单号）',
    u"订单编号",
    # u'编号',
]


def get_data(page, tables):
    result = extract_from_content(page)
    if not result["data"]:
        result = extract_from_table(tables)
    # result = extract_from_content(page)
    return result


def extract_from_content(page):
    return get_data_ori(page, re_compiled_set={})


def get_data_ori(page, re_compiled_set={}):
    trans_dict = dict()
    content = page
    search_num = 0
    row = ["1", page]
    for keyword in keywords:
        num = content.count(keyword)
        if num == 1:
            search_num += 1
            trans_dict, row, _ = process_keyword(content, keyword, trans_dict, row)
        else:  # 关键词未匹配到或者匹配到多次
            content_tmp = content
            while num > 0:
                search_num += 1
                num -= 1
                trans_dict, row, content_tmp = process_keyword(content_tmp, keyword, trans_dict, row)
    if search_num == 0:
        res_data = ""
    else:
        res_data = handler_contains_value(trans_dict[row[0]]).get("content", "").strip()
    # else:
    #     # 对包含关系的编号进行特殊处理
    #     # print(trans_dict[row[0]])
    #     try:
    #         handle_data = handler_contains_value(trans_dict[row[0]])
    #         res_data = handle_data.get("content", "").strip()
    #         if res_data:
    #             res_data = handle_res_data(res_data)
    #         if res_data and not check_data(res_data):
    #             res_data = ""
    #     except Exception as e:
    #         res_data = ""

    # if "***" in res_data:
    #     res_data = ""
    res_dict = {"type": "project_id", "data": res_data}
    return res_dict


def process_keyword(content, keyword, trans_dict, row):
    """_summary_

    Args:
        content (_type_): _description_
        keyword (_type_): _description_
        trans_dict (_type_): _description_
        row (_type_): _description_

    Returns:
        trans_dict:
        row:
        content:
    """
    start_index = content.find(keyword)
    record_index = start_index
    if record_index != -1:
        # 首先对注册编号匹配进行剔除
        if keyword == '编号':
            if content[record_index - 2:record_index + 2] == '注册编号':
                temp_row = trans_dict.get(row[0], None)
                if temp_row is None:
                    trans_dict[row[0]] = {
                        'content': '',
                        'repeat': []
                    }
                else:
                    repeat = trans_dict[row[0]].get('repeat', None)
                    if not len(repeat):
                        trans_dict[row[0]] = {
                            'content': '',
                            'repeat': []
                        }
                return

        end_index = record_index + 70
        result_content = content[record_index: end_index]
        result_content = extract_number(result_content, keyword)
        """原文
        """
        # result_content = handler_content_one(result_content)
        # result_content = handler_content_two(result_content)
        # result_content = handler_content_three(result_content)
        # 在最后进行一次数据的清晰，把含有不规则符号的字符串去掉
        # is_need = data_cleaning(result_content)
        # if is_need:
        #     result_content = ' '
        if row[0] in trans_dict.keys():
            if result_content not in trans_dict[row[0]]['repeat']:
                old_content = trans_dict[row[0]]['content']
                if result_content != ' ':
                    trans_dict[row[0]]['repeat'].append(result_content)
                    if old_content and result_content:
                        trans_dict[row[0]]['content'] = old_content + "，" + result_content
                    elif old_content and not result_content:
                        pass
                    else:
                        trans_dict[row[0]]['content'] = result_content
        else:
            repeat_list = list()
            if result_content != ' ':
                repeat_list.append(result_content)
            trans_dict[row[0]] = {
                'content': result_content,
                'repeat': repeat_list
            }
    content = content[start_index + len(keyword):len(content)]
    return trans_dict, row, content


def process_brackets(number):
    """处理编号中的括号
    """
    if not number:
        return number
    brackets = [
        ("(", ")"),
        ("（", "）"),
        ("[", "]"),
        ("【", "】"),
    ]
    for _b in brackets:
        if _b[0] in number and _b[1] not in number:
            start_index = number.find(_b[0])
            number = number[start_index + 1:]
        elif _b[1] in number and _b[0] not in number:
            end_index = number.find(_b[1])
            number = number[:end_index]
        elif number and number[0] == _b[0] and number[-1] == _b[1]:
            number = number[1:-1]
    return number


def extract_number(content, keyword, source="page"):
    """_提取出编号

    Args:
        content (_type_): _description_
        keyword (_type_): _description_
    """
    # idx = 0 + len(keyword)
    # while idx < len(content) and re.match("\\s", content[idx]):
    #     idx += 1

    number = ""
    if source == "page":
        content = content[len(keyword):]
        patterns = [
            "[:：\\s]*([^\\s:：]*?)[,?，。？、\\s]",
            "[:：\\s]*([^\\(\\s:：]*?)[\\),?，。？、\\s]",
            "[:：\\s]*([^\\[\\s:：]*?)[\\],?，。？、\\s]",
            "[:：\\s]*([^\\s:：【]*?)[】,?，。？、\\s]",
            "[:：\\s]*([^\\s:：（]*?)[）,?，。？、\\s]"
        ]
        r = re.search("|".join(patterns), content)
        if r:
            for group in r.groups():
                if group and group.strip():
                    number = group.strip()
                    break
    elif source == "table":
        number = content
    number = process_brackets(number)
    if len(number) <= 4 or not re.search("[a-zA-Z0-9]", number):
        number = ""
    if "元" in number:
        number = ""
    if number:
        number = handle_res_data(number)
    if number and not check_data(number):
        number = ""
    return number


def extract_from_table(tables):
    result = []
    for table in tables:
        result.extend(target_keywords_table(table, keywords))
    return {
        "type": "project_id",
        "data": result[0]["text"] if result else "",
        "source": "keyword_tables"
    }


def target_keywords_table(table, keywords_args=keywords):
    target_cells = regrex_match_table(table, keywords_args)
    # 获取右侧或下侧单元格内容并判断是否包含结尾词，
    # 若不包含则优先获取右侧内容
    for cell in target_cells:
        if not isinstance(cell['text'], str):
            cell['text'] = str(cell['text'])
        cell['source'] = 'target_keywords_table'
    result = target_cells
    # result = self.result_clean(target_cells)
    return result


def regrex_match_table(table, regrexs):
    '''
    通过正则组合获取符合条件的cell的右边和下面的cell
    '''

    def check_end_words(cell_args):
        if not re.search("[a-zA-Z0-9]", str(cell_args)):
            return False
        return True

    def search_right_cell(i, j):
        right_cell = None
        if j + 1 < col_size:
            right_cell = table[i][j + 1]
        return right_cell

    def search_down_cell(i, j):
        down_cell = None
        if i + 1 < row_size:
            down_cell = table[i + 1][j]
        return down_cell

    # 匹配精准关键词定位在表格内时，
    # 判断关键词所在单元格字数是否大于15个字符，则跳过该关键词
    match_ij = []
    row_size = len(table)
    col_size = len(table[0])
    for i, cells in enumerate(table):
        for j, cell in enumerate(cells):
            if not isinstance(cell, str):
                cell = str(cell)
            if len(cell) > 15:
                continue
            for keyword in regrexs:
                if cell.find(keyword) != -1:
                    match_ij.append({
                        'cell': (i, j),
                        'targetword': keyword,
                    })
    # 获取右侧或下侧单元格内容并判断是否包含结尾词，
    # 若不包含则优先获取右侧内容
    target_cells = []
    for item in match_ij:
        i, j = item.pop('cell')
        right_cell = search_right_cell(i, j)
        down_cell = search_down_cell(i, j)
        right_flag = False
        down_flag = False
        if right_cell:
            right_flag = check_end_words(right_cell)
        if down_cell:
            down_flag = check_end_words(down_cell)
        if right_flag:
            item['text'] = extract_number(str(right_cell), item["targetword"], source="table")
            # item['text'] = right_cell
            target_cells.append(item)
        elif down_flag:
            item['text'] = extract_number(str(down_cell), item["targetword"], source="table")
            # item['text'] = down_cell
            target_cells.append(item)
        elif not right_flag and not down_flag and right_cell:
            item['text'] = ""
            target_cells.append(item)
    return target_cells


def handle_res_data(value):
    if "\u00A0" in value:
        value = value.split("\u00A0")[0]
    if "\u0020" in value:
        value = value.split("\u0020")[0]
    if "\u3000" in value:
        value = value.split("\u3000")[0]
    if "\t" in value:
        value = value.split("\t")[0]
    if "\n" in value:
        value = value.split("\n")[0]
    if "\r" in value:
        value = value.split("\r")[0]
    return value


def check_data(value):
    if len(value) < 5 or len(value) > 50:
        return False
    if re.search('[^a-zA-Z0-9\u4e00-\u9fa5\(\)\[\]【】［］〔〕{}\-—－/*\s―_·、《》﹝﹞()（）.]', value):
        return False
    if not re.match('^[a-zA-Z0-9\u4e00-\u9fa5\(\[【［〔{*]', value):
        return False
    if not re.match('[a-zA-Z0-9\u4e00-\u9fa5\)）\]】］〕}*]', value[-1]):
        return False
    if "line" in value:
        return False
    if "span" in value:
        return False
    if "font" in value:
        return False
    return True


if __name__ == '__main__':
    # todo 2.获取招标编号
    from beetle_cracker.re_extract_cracker.common.utils import get_pre_extract, get_pre_extract_v2
    from utils.sql import findBidding
    from utils.time import ymdToTs
    # 提取
    arrFix = [('deb6a48f37a5431c90be1feac5a5b523', ymdToTs('2023-07-20'))]
    for (id, pbTime) in arrFix:
        bidding = findBidding(id, pbTime)

        url = bidding['source_url']
        page = bidding['snapshot']
        title = bidding['title']

        tables, text = get_pre_extract(page)
        tables_v2, text_v2 = get_pre_extract_v2(page)
        print(get_data(text_v2, tables_v2))