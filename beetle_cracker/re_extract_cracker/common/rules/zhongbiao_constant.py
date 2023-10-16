#!/usr/bin/env python
# -*- coding: utf-8 -*-

new_para_formats = [
    "([\u0391-\uFFE5]+)\\s*为第一中标候选人",
    "([\u0391-\uFFE5]+)\\s*为第一中标人",
    "拟由([\u0391-\uFFE5]+)\\s*中标",
    "确定([\u0391-\uFFE5]+)\\s*为成交单位",
    "推荐([\u0391-\uFFE5]+)为第一中标（成交）候选供应商",
    "经评定([\u0391-\uFFE5]+)\\s*确定为中标单位",
    "([\u0391-\uFFE5]+)\\s*为拟成交单位",
    "由([\u0391-\uFFE5]+)\\s*成交",
    "拟定由([\u0391-\uFFE5]+)\\s*为中标单位",
    "([\u0391-\uFFE5]+)\\s*为机关食堂承租人",
    "([\u0391-\uFFE5]+)\\s*为第一中标排序人",
    "([\u0391-\uFFE5]+)\\s*被确定为中标单位",
    "预确定([\u0391-\uFFE5]+)\\s*为预中标人",
    "经评标委员会一致评定，([\u0391-\uFFE5]+)\\s*确定为中标单位",
    "确定([\u0391-\uFFE5]+)\\s*中标",
    "共同推荐([\u0391-\uFFE5]+)\\s*为中标候选人",
    "最终选定([\u0391-\uFFE5]+)\\s*为中选供应商",
    "经过综合评价([\u0391-\uFFE5]+)\\s*中标",
    "推荐([\u0391-\uFFE5]+)\\s*中标人",
    "综合评审，([\u0391-\uFFE5]+)为预中标单位",
    "故选择([\u0391-\uFFE5]+)为中标单位",
    # "故选择为中标单位",
    "确定第一中标候选人为([\u0391-\uFFE5]+)",
    "询价开标现场中标单位为([\u0391-\uFFE5]+)",
    "确定排名第一的([\u0391-\uFFE5]+)为第一中标候选人",
    "本项目拟由([\u0391-\uFFE5]+)为采购供应商",
    "预中标单位：([\u0391-\uFFE5]+)成为中标单位",
    "拟定([\\s\\S]+)\\s*中标单位",
    "评标结果：([\\s\\S]+)\\s*为中标单位",
    "经评定([\\s\\S]+)\\s*为中标单位",
    "现拟定\\s*([\\s\\S]+)为中标人",
    "最终确定该项目的中标单位为\\s*([\\s\\S]+)。",
    "招投标会议综合评定：\\s*([\\s\\S]+)为该项目拟中标人",
    "拟定\\s*([\\s\\S]+)项目的中标候选供应商",
    "\\s*([\\s\\S]+)为第一中标单位",
    "\\s*([\\s\\S]+)为第一中标候选人",
    "\\s*([\\s\\S]+)为第二中标候选人",
    "\\s*([\\s\\S]+)为第三中标候选人",
    "由\\s*([\\s\\S]{0,50})\\s*中标",
    "经我公司综合评审，\\s*([\\s\\S]+)\\s*确定该公司为本次中标单位",
    "招标结果为：\\s*([\\s\\S]+)\\s*中标",
    "\\s*([\\s\\S]+)\\s*中标、中标价",
    "经谈判拟与\\s*([\\s\\S]+)\\s*成交",
    "现变更为：\\s*([\\s\\S]+)\\s*中标",
    "由\\s*([\\s\\S]+)\\s*以\\s*[\\s\\S]+\\s*元中标",
    "确定的中标候选单位是\\s*([\\s\\S]+)\\s*。",
    "询价小组专家意见：\\s*([\\s\\S]+)\\s*因此选该公司为最终供货商",
    "决定\\s*([\\s\\S]+)\\s*第一顺位中标",
    "确定([\u0391-\uFFE5]+)成交人为([\u0391-\uFFE5]+)",
    "确定([\u0391-\uFFE5]+)为该工程的中标单位",
    "确定\\s*([\\s\\S]+)\\s*为中标单位",
    "([\u0391-\uFFE5]+)报价最低，\\s*([\\s\\S]+)\\s*确定为该项目中标候选人",
    "经评审，([\u0391-\uFFE5]+)为成交人",
    "现予以公示：([\u0391-\uFFE5]+)为中标单位",
    "\\s*([\\s\\S]+)\\s*推荐为中标厂商",
    "结果为\\s*([\\s\\S]+)\\s*中标",
    "推荐本项目\\s*([\\s\\S]+)\\s*预中标单位",
    "确定\\s*([\\s\\S]+)\\s*在此项目为成交供应商",
    "确定\\s*([\\s\\S]+)\\s*为成交供应商",
    "确定中选人为\\s*([\\s\\S]+)\\s*，以上结果现予以公示",
    "采取随机摇球的方法进行遴选，\\s*([\\s\\S]+)\\s*为中标企业",
    "推荐综合得分最高的\\s*([\\s\\S]+)\\s*为成交人",
    "确定\\s*([\\s\\S]+)\\s*为采购对象",
    "确定本项目的中标人为\\s*([\\s\\S]+)\\s*。",
    "排名第一的\\s*([\\s\\S]+)\\s*为中标人",
    "([\u0391-\uFFE5]+)\\s*报价最低",
    "([\u0391-\uFFE5]+)\\s*为.{1,10}分标第一成交候选人",
    "推荐([\u0391-\uFFE5]+)\\s*等投标人为中标候选人",
    # "成交候选人名称联系人联系方式 中标金额公务用车 湖南润景",
    "：第一名([\u0391-\uFFE5]+)、",
    "推荐([\u0391-\uFFE5]+)为中标供应商",
    "一致同意([\u0391-\uFFE5]+)为中标单位",
    "确定\\s*([\\s\\S]+)\\s*的中标单位",
    "第一中标候选单位\\s*([\u0391-\uFFE5]+)\\s*为",
    "中标单位为：\\s*([\\s\\S]+)\\s*。",
    "招选及监督委员会一致评定：([\\s\\S]+)得分最高",
    "[\\s\\S]+的中标供应商：([\\s\\S]+)，",
    # "广州市白云区松洲粤远昌五金机电经营部2018-10-10成交成功",
    "确认([\\s\\S]+)为[\\s\\S]+第一中标候选单位",
    "([\\s\\S]{5,25}).{0,1}：.{0,1}你.{0,1}方.{0,1}于[\\s\\S]+，.{0,1}被.{0,1}确.{0,1}定.{0,1}为.{0,1}中.{0,1}标.{0,1}人",
    "([\\s\\S]{5,20}):[\\s\\S]{100,120}，现确定你单位为[\\s\\S]+的中标人",
    "([\\s\\S]{5,25})：[\\s\\S]+贵公司参与",
    "确定([\u0391-\uFFE5]{5,20})为[\\s\\S]{5,25}的中标单位",
    "与([\u0391-\uFFE5]{5,20})签订合同",
    "([\u0391-\uFFE5]{5,12})为本项目预成交单位",
    "([\u0391-\uFFE5]{5,20})最终以报价[\\s\\S]{5,30}中标",
    "该项目拟由([\u0391-\uFFE5]{5,20})提供",
    "([\u0391-\uFFE5]{5,20})：[\\s\\S]+你方于[\\s\\S]+被确定为中标人",
    "由([\u0391-\uFFE5]{5,20})供货",
    "([\u0391-\uFFE5]{5,20})为该项目中标单位",
    "确定中标人为:([\u0391-\uFFE5]{5,20})",
    "现确定([\u0391-\uFFE5]{5,30})[等]?[\\s\\S]+公司为[\\S\\s]+招标的中标人",
    "经采购人[\\s\\S]*确认，\\s*([\u0391-\uFFE5]{5,30})\\s*成为[\\s\\S]*的成交供应商",
    "中标信息\\s*([\u0391-\uFFE5]{5,20})\\s*中标价",
    '第一名：([\u0391-\uFFE5]{5,20})',
    '第二名：([\u0391-\uFFE5]{5,20})',
    '第三名：([\u0391-\uFFE5]{5,20})',
    # '成交供应商名称、联系地址及成交金额：[\\S\\s]*成交金额\(万元\)[\\s\\S]{10}',
]