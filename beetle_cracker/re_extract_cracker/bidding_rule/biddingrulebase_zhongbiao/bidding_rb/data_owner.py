#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 拟中标	    中标单位联系人	    中标单位联系电话
# 中标单位	中标公司联系人	    中标公司联系电话
# 中标公司	中标联系人	    中标联系电话
# 中标人	    供应商单位联系人	供应商单位联系电话
# 供应商	    成交单位联系人	    成交单位联系电话
# 供应单位	供应商联系人	    供应商联系电话
# 成交单位	成交联系人	    成交联系电话
# 成交人	    成交人	        成交人联系电话
# 乙方	    联系人	        联系人电话
# 中标	    项目负责人	    联系人方式
# 成交	    项目主管	        联系方式
# 供应	    项目经理	        联络方式
# 	        姓名	            电话
# 	        联络人	        手机

target_keywords = [
    r"拟\s*中\s*标\b",
    r"中\s*标\s*单\s*位\b",
    r"中\s*标\s*公\s*司\b",
    r"中\s*标\s*人\b",
    r"供\s*应\s*商\b",
    r"供\s*应\s*单\s*位\b",
    r"承\s*包\s*单\s*位\b",
    r"承\s*包\s*人\b",
    r"成\s*交\s*单\s*位\b",
    r"成\s*交\s*人\b",
    r"乙\s*方\b",
    # r"标\s*段\b",
]

contact_person_words = [
    r"中标单位联系人\b",
    r"中标公司联系人\b",
    r"中标联系人\b",
    r"供应商单位联系人\b",
    r"成交单位联系人\b",
    r"供应商联系人\b",
    r"成交联系人\b",
    r"委托代理人\b",
    r"确\s*认\s*人\b",
    r"成\s*交\s*人\b",
    r"联\s*系\s*人\b",
    r"项目负责人\b",
    r"项目主管\b",
    r"项目经理\b",
    r"姓\s*名\b",
]

contact_number_words = [
    "中标单位联系电话",
    "中标公司联系电话",
    "中标联系电话",
    "供应商单位联系电话",
    "成交单位联系电话",
    "供应商联系电话",
    "成交联系电话",
    "成交人联系电话",
    "联系人电话",
    "联系人方式",
    "联系方式",
    "联络方式",
    "电话",
    "手机",
    '电 话',
    '电  话：',
    '供应商联系方式',
    # '中标供应商电话',
    # '成交供应商电话',
]

rule_supplement_words = [
    r"中\s*标\s*联\s*系\s*人",
    r"中\s*标\s*联\s*系\s*人\s*姓\s*名",
    r"中\s*标\s*联\s*系\s*人\s*名\s*称",
    r"中\s*标\s*机\s*构",
    r"中\s*标\s*单\s*位",
    r"中\s*标\s*人",
    r"供\s*应\s*商",
    r"承\s*包\s*商",
    r"承\s*包\s*人",
    r"承\s*包\s*单\s*位",
    r"供应商\S*电话",
    r"供应商\S*联系人",
    r"中标\S*电话",
    r"中标\S*联系人",
    r"承包\S*电话",
    r"承包\S*联系人",

]

family_name_words = []


with open('bidding_rb/family_name.txt', 'r') as input_file:
        lines = input_file.readlines()
        for line in lines:
            family_name_words.append(line.rstrip('\n'))

contact_filter_words = [
    "成交",
    "供应",
    "竞价",
    "供货",
    "承包",
    "质疑",
    "投诉",
    "投标人",
    "招标代理机构",
    "监督管理",
    "监督部门",
    "监督单位",
    "投诉部门",
    "投诉单位",
    "监督联系",
    "投诉联系"
]

phone_regexs = [
    r'1\d{2}(\d{4}|\*{4})(\d{4}|\d{3})',
    r'\+\d{2}-+\d*(-\d*)?',
    r'\d{3,4}-+\d{3,}-\d*',
    # r'\d{4}-\d{7}',
    r'\d{4}-+\d{7,8}(-\d{5})?',
    r'\d{3}-+\d{8}|\d{4}-(\d{8}|\d{7})',
    r'(\([0]\d{2}|\d{4}\))(\d{6,7})',
    r'\b\d{10}-+\d-\d{4}\b',
    r'\d{3,4}\s?-+\s?\d{7,8}',
    r'\d{3}-+\d{4}( |-)\d{4}',
    r'\d{8}-\d*',
    r'1\d{2}(\d{4}|\*{4})(\d{4}|\d{3})',
    r'\d{5,15}'
    # r'\d{5,20}'
]