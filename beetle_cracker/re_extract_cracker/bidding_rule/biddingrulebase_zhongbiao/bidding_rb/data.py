#!/usr/bin/env python
# -*- coding: utf-8 -*-


target_keywords = [
    # "第\\s*一\\s*中\\s*标\\s*候\\s*选\\s*人(:|：|名\\s*称){1}",
    # "第\\s*一\\s*成\\s*交\\s*供\\s*应\\s*商\\s*候\\s*选\\s*人\\s*(:|：|名\\s*称){1}",
    # "第\\s*一\\s*中\\s*标\\s*人\\s*(:|：|名\\s*称){1}",
    # "第\\s*一\\s*中\\s*签\\s*候\\s*选\\s*人\\s*(:|：|名\\s*称){1}",
    # "第\\s*一\\s*中\\s*标\\s*排\\s*序\\s*人\\s*(:|：|名\\s*称|为){1}",
    # "第\\s*一\\s*成\\s*交\\s*候\\s*选\\s*人\\s*(:|：|名\\s*称){1}",
    # "第\\s*(一|1)\\s*名\\s*(:|：|名\\s*称)*",
    "一\\s*等\\s*奖\\s*(:|：|名\\s*称){1}",
    # "一\\s*中\\s*标\\s*候\\s*选\\s*人\\s*(:|：|名\\s*称){1}",
    "第\\s*一\\s*成\\s*交\\s*供\\s*应\\s*商\\s*(:|：|名\\s*称){1}",
    "推荐第一标段中标候选人：",
    "推荐第二标段中标候选人：",
    "第一成交候选单位为",
    "第一签约侯选人：",
    "第一中标候选人为",
    "排名第一的：",
    "第一中标（成交）候选人名称：",
    "第一次报价",
    "第一中标人为",
    "第\\s*一\\s*中\\s*标\\s*排\\s*序\\s*人(为|[:：\\s])",
    "第\\s*一\\s*中\\s*标\\s*候\\s*选\\s*人(:|：|名\\s*称){1}([:：\\s]|$)",
    "第\\s*一\\s*中\\s*标\\s*候\\s*选\\s*人\\s*为",
    "第一中标候选人\\s*投标人名称[：|\\s]*",
    "第一承包候选人",
    "第\\s*一\\s*承\\s*包\\s*候\\s*选\\s*人\\s*(:|：|名\\s*称|为)*",
    "第一候选人(:|：|名\\s*称)*",
    "第一中签人(:|：|名\\s*称)*",
    "第一中标侯选人为",
    "第一中标候选单位为：",
    "第\\s*[1一]\\s*候\\s*选\\s*人",
    "第\\s*一\\s*名([:：\\s]|$)",


    "成交供应商（承接主体）名称：",
    "中标（成交）供应商名称：",
    "推荐成交报价单位：",
    "最终确定的中标人是：",
    "推荐成交人：",
    "，推荐中标人为",
    "中标厂商：",
    '中标单位：? ',
    "拟中标供应商",
    "拟中标单位",
    '中选人名称：',
    "拟中选单位",
    "拟中标人",
    "拟中选人",
    "供应商（乙方）[：:]?",
    "拟定中标供应商",
    "拟定中标单位",
    "拟定中选单位",
    "拟定中标人",
    "拟定中选人",
    "竞得人（中标人）",
    "成交候选供应商",
    "承\\s*包\\s*单\\s*位：",
    "竞价单位：",
    "开票单位：",
    "供应商\\(乙方\\):",
    "联合体牵头方：",
    "预中标（成交）人名称：",
    "并经我单位确认的中标人是",
    "现将中标单位公示如下：",
    "推荐的候选谈判单位为：",
    "的中标人为：",
    
    "成交报价人名称：",
    "成交候选单位：",
    "本项目的成交供应商为",
    "中标侯选人：",
    "成交供应商名称：",
    "供应商名称： ",
    "中标供应商：",
    "中标供应商为：",
    "成交供应商：",
    "成交电商：",
    "[\\s\\S]+中标供应商是：",
    
    "成交服务商(:|：){1}",
    "中标施工方为",
    "包1的中选人为",
    "最终抽中的中选人是：",
    
    "中标单位为",
    "受让单位",
    
    #"第\\s*二\\s*中\\s*标\\s*候\\s*选\\s*人(:|：|名\\s*称|为)*",
    #"第二中标候选人\\s*投标人名称[：|\\s]*",
    #"第\\s*三\\s*中\\s*标\\s*候\\s*选\\s*人(:|：|名\\s*称|为)*",
    #"第三中标候选人\\s*投标人名称[：|\\s]*",
    
    #"第\\s*二\\s*承\\s*包\\s*候\\s*选\\s*人\\s*(:|：|名\\s*称|为)*",
    #"第\\s*三\\s*承\\s*包\\s*候\\s*选\\s*人\\s*(:|：|名\\s*称|为)*",
    "中\\s*标\\s*人\\s*(:|：|名\\s*称|为：){1}",
    "中\\s*标\\s*单\\s*位\\s*(:|：|名\\s*称){1}",
    #"供\\s*应\\s*商\\s*(:|：|名\\s*称|名\\s*单){1}",

    "供\\s*应\\s*商\\s*([:：\\s]|$)",
    "供\\s*应\\s*商\\s*(名\\s*称|名\\s*单){1}([:：\\s]|$)",

    "中\\s*标\\s*企\\s*业\\s*(:|：|名\\s*称){1}",
    # "成\\s*交\\s*单\\s*位\\s*(:|：|名\\s*称){1}",
    "成\\s*交\\s*供\\s*应\\s*商\\s*(:|：|名\\s*称){1}",
    "成\\s*交\\s*人\\s*(:|：|名\\s*称){1}",
    "中\\s*选\\s*企\\s*业\\s*(:|：|名\\s*称){1}",
    "供\\s*货\\s*商\\s*(:|：|名\\s*称){1}",
    # "投\\s*标\\s*单\\s*位\\s*(:|：|名\\s*称){1}",
    "乙\\s*方\\s*(:|：|名\\s*称){1}",
    "供\\s*应\\s*单\\s*位\\s*(:|：|名\\s*称){1}",
    "供\\s*应\\s*商\\s*\\(\\s*乙\\s*方\\s*\\)\\s*：",
    #"中\\s*标\\s*候\\s*选\\s*人\\s*(:|：|名\\s*称){1}",
    "拟\\s*中\\s*标\\s*人",
    "承\\s*包\\s*人\\s*(:|：|名\\s*称){1}",
    "中\\s*签\\s*单\\s*位\\s*(:|：|名\\s*称){1}",
    "中标应商名称：",
    "成交竞租人",
    "中标/中选单位:",
    "中标意向单位：",
    "中标人名单为：",
    "中选机构名称：",
    #"中\\s*选\\s*候\\s*选\\s*人\\s*(:|：|名\\s*称){1}",
    "中\\s*标\\s*\\(成交\\)\\s*单\\s*位\\s*(:|：|名\\s*称){1}",
    #"成\\s*交\\s*候\\s*选\\s*人\\s*(:|：|名\\s*称){1}",
    "中\\s*标\\s*（成交）\\s*供\\s*应\\s*商\\s*(:|：|名\\s*称){1}",
    "侯选/中标供应商：",
    "预成交结果：",
    "采购中标候选书商为：",
    "推荐中标供应商",
    "中标（成交）供应商",
    "自报价厂商：",
    "中标（成交）供应商（乙方）:",
    "设备的厂商：",
    "中选单位：",
    "承包单位名称：",
    "投标单位入围名单：",
    # "中标候选单位：",
    
    "最终确定中标人为：",
    "预中标候选人(:|：|名\\s*称)*",
    
    "拟中标（成交）人",
    "第二包供货候选单位：",
    
    "确定中标的监理机构为：",
    "成交企业：",
    #"第(1|2|4|3){1}包",
    "中标回收商：",
    #"成交候选单位",
    "供应商（全称）：",
    #"中标侯选人:",
    "中标人",
    '生产企业：',
    '乙方（供应商）：',
    # '成 交 单 位 ',
    '乙方签字:',
    '成交人：',
    '中标人：',
    '中选中介机构名称: ',
    '流入方名称',
    '[\\s\\S]+的成交供应商：',
    # '成交供应商：([\u4E00-\u9FA5]+)',
    '供应商:',
    '中标人名称',
    '成交人:',
    '中标供应商(?!(的))[:：\\s]',
    '中\\s*标\\s*供\\s*应\\s*商\\s*(为|是)[:：\\s]?',
    '中选机构名称[:：]* ',
    '竞拍结果[:：◆]*',
    '中标候选人第\\s*1\\s*名[：:]*',
    '中标方[：:]*',
    '成交单位名称：',
    '入围投标人',
    '成交单位：',
    '应答人名称',
    '中标单位公示如下：',

    "中\\s*选\\s*人[:：\\s]",
    "中\\s*标\\s*候\\s*选\\s*(人|单\\s*位)(名\\s*称|名\\s*单){1}([:：\\s]|$)",
    "成\\s*交\\s*单\\s*位([:：\\s]|$)",
    "中\\s*选\\s*公\\s*司",
    "中\\s*标\\s*公\\s*司([:：\\s]|$)",
    "成\\s*交\\s*公\\s*司[为]?([:：\\s]|$)",
    "成\\s*交\\s*侯\\s*选\\s*人([:：\\s]|$)",
    "成\\s*交\\s*侯\\s*选\\s*人(:|：|名\\s*称){1}",
    "中\\s*标\\s*侯\\s*选\\s*人[为]?([:：\\s]|$)",

    "预\\s*中\\s*标\\s*(企\\s*业|单\\s*位)",
]

para_formats = [
    "[\u0391-\uFFE5]+\\s*为第一中标候选人",
    "[\u0391-\uFFE5]+\\s*为第一中标人",
    "拟由[\u0391-\uFFE5]+\\s*中标",
    "确定[\u0391-\uFFE5]+\\s*为成交单位，",
    "推荐[\u0391-\uFFE5]+为第一中标（成交）候选供应商",
    "经评定[\u0391-\uFFE5]+\\s*确定为中标单位",
    "[\u0391-\uFFE5]+\\s*为拟成交单位",
    "由[\u0391-\uFFE5]+\\s*成交",
    "拟定由[\u0391-\uFFE5]+\\s*为中标单位",
    "[\u0391-\uFFE5]+\\s*为机关食堂承租人",
    "[\u0391-\uFFE5]+\\s*为第一中标排序人",
    "[\u0391-\uFFE5]+\\s*被确定为中标单位",
    "预确定[\u0391-\uFFE5]+\\s*为预中标人",
    "经评标委员会一致评定，[\u0391-\uFFE5]+\\s*确定为中标单位",
    "确定[\u0391-\uFFE5]+\\s*中标",
    "共同推荐[\u0391-\uFFE5]+\\s*为中标候选人。",
    "最终选定[\u0391-\uFFE5]+\\s*为中选供应商",
    "经过综合评价[\u0391-\uFFE5]+\\s*中标",
    "推荐[\u0391-\uFFE5]+\\s*中标人",
    "综合评审，[\u0391-\uFFE5]+为预中标单位",
    "故选择[\u0391-\uFFE5]+为中标单位",
    "故选择为中标单位",
    "确定第一中标候选人为[\u0391-\uFFE5]+",
    "询价开标现场中标单位为[\u0391-\uFFE5]+",
    "确定排名第一的[\u0391-\uFFE5]+为第一中标候选人",
    "本项目拟由[\u0391-\uFFE5]+为采购供应商",
    "第2的预中标单位：[\u0391-\uFFE5]+成为中标单位",
    "拟定[\\s\\S]+\\s*中标单位",
    "评标结果：[\\s\\S]+\\s*为中标单位",
    "经评定[\\s\\S]+\\s*为中标单位",
    "现拟定\\s*[\\s\\S]+为中标人",
    "最终确定该项目的中标单位为\\s*[\\s\\S]+。",
    "招投标会议综合评定：\\s*[\\s\\S]+为该项目拟中标人。",
    "拟定\\s*[\\s\\S]+项目的中标候选供应商。",
    "\\s*[\\s\\S]+为第一中标单位，",
    "\\s*[\\s\\S]+为第一中标候选人",
    "\\s*[\\s\\S]+为第二中标候选人",
    "\\s*[\\s\\S]+为第三中标候选人",
    "由\\s*[\\s\\S]{0,50}\\s*中标。",
    "经我公司综合评审，\\s*[\\s\\S]+\\s*确定该公司为本次中标单位",
    "招标结果为：\\s*[\\s\\S]+\\s*中标，",
    "\\s*[\\s\\S]+\\s*中标、中标价：",
    "经谈判拟与\\s*[\\s\\S]+\\s*成交，",
    "现变更为：\\s*[\\s\\S]+\\s*中标，",
    "由\\s*[\\s\\S]+\\s*以\\s*[\\s\\S]+\\s*元中标，",
    "综合评议，确定的中标候选单位是\\s*[\\s\\S]+\\s*。",
    "询价小组专家意见：\\s*[\\s\\S]+\\s*因此选该公司为最终供货商。",
    "招标小组采用综合评分法决定\\s*[\\s\\S]+\\s*第一顺位中标。",
    "已确定[\u0391-\uFFE5]+成交人为[\u0391-\uFFE5]+",
    "，确定[\u0391-\uFFE5]+为该工程的代理机构。",
    "，确定\\s*[\\s\\S]+\\s*为中标单位。",
    "，[\u0391-\uFFE5]+报价最低，\\s*[\\s\\S]+\\s*确定为该项目中标候选人，",
    "经评审，[\u0391-\uFFE5]+为成交人，",
    "，现予以公示：[\u0391-\uFFE5]+为中标单位。",
    "经过专家独立打分，\\s*[\\s\\S]+\\s*推荐为中标厂商。",
    "，结果为\\s*[\\s\\S]+\\s*中标。",
    "，推荐本项目\\s*[\\s\\S]+\\s*预中标单位。",
    "确定\\s*[\\s\\S]+\\s*在此项目为成交供应商，",
    "确定\\s*[\\s\\S]+\\s*为成交供应商。",
    "，确定中选人为\\s*[\\s\\S]+\\s*，以上结果现予以公示。",
    "采取随机摇球的方法进行遴选，\\s*[\\s\\S]+\\s*为中标企业。",
    "推荐综合得分最高的\\s*[\\s\\S]+\\s*为成交人，",
    "经审议\\s*，确定\\s*[\\s\\S]+\\s*为采购对象",
    "经评标委员会认真评审，确定本项目的中标人为\\s*[\\s\\S]+\\s*。",
    "符合招标文件要求且综合排名第一的\\s*[\\s\\S]+\\s*为中标人，",
    "[\u0391-\uFFE5]+\\s*报价最低",
    "[\u0391-\uFFE5]+\\s*为[A|B|C]+分标第一成交候选人，",
    "，推荐[\u0391-\uFFE5]+\\s*等投标人为中标候选人，",
    "成交候选人名称联系人联系方式 中标金额公务用车 湖南润景",
    "：第一名[\u0391-\uFFE5]+、",
    "推荐[\u0391-\uFFE5]+为中标供应商，",
    "一致同意[\u0391-\uFFE5]+为中标单位",
    "确定\\s*[\\s\\S]+\\s*的中标单位；",
    "，我局确定第一中标候选单位\\s*[\u0391-\uFFE5]+\\s*为",
    "，经我中心项目领导小组集体讨论议定，中标单位为：\\s*[\\s\\S]+\\s*。",
    "，经过招选及监督委员会一致评定：[\\s\\S]+得分最高",
    "[\\s\\S]+的中标供应商：[\\s\\S]+，",
    "广州市白云区松洲粤远昌五金机电经营部2018-10-10成交成功",
    "确认[\\s\\S]+为[\\s\\S]+第一中标候选单位",
    "[\\s\\S]{5,25} ： 你 方 于 [\\s\\S]+， 被 确 定 为 中 标 人",
    "[\\s\\S]{5,20}:[\\s\\S]{100,120}，现确定你单位为[\\s\\S]+的中标人",
    "[\\s\\S]{5,25}：[\\s\\S]+贵公司参与",
    "确定[\u0391-\uFFE5]{5,20}为[\\s\\S]{5,25}的中标单位",
    "与[\u0391-\uFFE5]{5,20}签订合同。",
    "[\u0391-\uFFE5]{5,12}为本项目预成交单位",
    "[\u0391-\uFFE5]{5,20}最终以报价[\\s\\S]{5,30}中标。",
    "该项目拟由[\u0391-\uFFE5]{5,20}提供（或承担）。",
    "[\u0391-\uFFE5]{5,20}：[\\s\\S]+你方于[\\s\\S]+被确定为中标人。",
    "比质比价，最低价中选， 由[\u0391-\uFFE5]{5,20}供货",
    "[\u0391-\uFFE5]{5,20}为该项目中标单位",
    "确定中标人为:[\u0391-\uFFE5]{5,20}",
    "经评标、公示，现确定[\u0391-\uFFE5]{5,30}[等]?[\\s\\S]+公司为[\\S\\s]+招标的中标人。",
    "经采购人[\\s\\S]*确认，\\s*[\u0391-\uFFE5]{5,30}\\s*成为[\\s\\S]*的成交供应商",
    "中标信息\\s*[\u0391-\uFFE5]{5,20}\\s*中标价",
    '第一名：[\u0391-\uFFE5]{5,20} ',
    '第二名：[\u0391-\uFFE5]{5,20} ',
    '第三名：[\u0391-\uFFE5]{5,20} ',
    '成交供应商名称、联系地址及成交金额：[\\S\\s]*成交金额\(万元\)[\\s\\S]{10}',
]

fuzzy_keywords = [
    "致(:|：){1}",
    "施工标：",
    "供方：",
    "承包商:",
    "承包人",
    "成交商",
    "监理标：",
    "一标段：",
    "排名1：",
    "二标段：",
    "设计单位",
    "中标商：",
    "响应单位",
    "确定中标的设计单位为：",
    "施工单位",
    "投标申请人",
    "预审的申请人名单： ",
    "通过资格预审的申请人名单：",
    "中标候选单位排序：",
    "参选人名称",
    "成交公司：",
    "服务商名称：",
    "推荐中标候选单位为：",
    "通过单位:",
    "中选单位：",
    "中标商",
    "中标人如下：",
    "采购的中标人为：",
    "被抽中的中选人是：",
    "中标供应商",
    "预中标结果如下：",
    "中标人公告如下：",
    "报\\s*价\\s*单\\s*位",
    "中\\s*标\\s*（\\s*成\\s*交\\s*）\\s*单\\s*位",
    "中\\s*标\\s*单\\s*位",
    # "投\\s*标\\s*人",
    "中\\s*标\\s*公\\s*司",
    # "供\\s*应\\s*商",
    "供\\s*应\\s*商\\s*名\\s*称",
    "供\\s*应\\s*单\\s*位",
    "中\\s*标\\s*企\\s*业",
    "成\\s*交\\s*供\\s*应\\s*商",
    "候\\s*选\\s*人",
    "候\\s*选\\s*供\\s*应\\s*商",
    "成\\s*交\\s*单\\s*位",
    "成\\s*交\\s*人",
    "成\\s*交\\s*社\\s*会\\s*资\\s*本",
    "承\\s*接\\s*单\\s*位",
    "中\\s*选\\s*企\\s*业",
    "投\\s*标\\s*单\\s*位",
    # "投\\s*标\\s*人\\s*名\\s*称",
    "供\\s*货\\s*商 ",
    '流入方名称'
    "第\\s*(一|1)\\s*名",
    "一\\s*等\\s*奖",
    "预\\s*审\\s*入\\s*围\\s*单\\s*位",
    "第\\s*一\\s*排\\s*序\\s*人",
    "由\\s*[\u0391-\uFFE5]+\\s*报价较低较低中标",
    "\\s*竞\\s*得\\s*人\\s*",
    "投\\s*标\\s*单\\s*位\\s*名\\s*称",
    "侯\\s*选\\s*单\\s*位",
    #"中标结果",
    "中标供应商如下：",
    # "单位名称",
    "最后确定中标单位为：",
    "确定成交供应商为：",
    "成交厂商：",
    "标段(一：|二：|三：|四：){1}",
    "(一|二|三|四){1}标段",
    "中\\s*标\\s*人",
    "包(一：|二：){1}",
    "中介服务使用单位：",
    "通过资格预审的单位名单如下：",
    "此次中选需供货单位为：",
    "预中标结果",
    "名单如下：",
    "投标企业",
    "成交回收商",
    "选定中介服务机构是",
    "\\s*标\\s*段\\s*(一|二|三){1}",
    "符合要求的供应商报价：",
    "企业名称",
    "第一：",
    "确定拟成交单位如下：",
    "确定中选人如下：",
    "确定中标单位为：",
    "中标信息：",
    "入围单位",
    "入围人",
    "制造商:",
    "项目采购单位",
    "的中选单位为：",
    "通过的投标单位如下：",
    "中选人",
    "供货单位:",
    "成交信息：",
    "企业名",
    "中标候选单位",
    "物资信息中标厂商",
    "比选结果：",
    "随机抽取选定施工单位为：",
    "采购成交结果",
    "最低有效竞价商品",
    "供货地点",
    "中标候选人为：",
    "配送企业：",
    "标/包1的中选人为",
    "土地使用权人:",
    "（乙方）(:|：){1}",
    "供应商名称",
    "中选中介服务机构",
    "中选承包商",
    "中介服务单位",
    "第一中标排序单位名称",
    "中选单位如下：[\\s\\S]+单位：",
    "送货单位",
    "品牌、生产厂家及国别",
    "入围投标人",
    "拟定资产处置单位如下：",
    "候选人名称",
    "拟中商人",
    "拟定中标人",
    "最终用户",
    "参与供应商",
    "竞拍单位",
    "成交人如下：",

    
    "供应商(?!(地址|的))",
]

black_words = [
    '类似业绩',
    '过去业绩',
    '相似业绩',
    '类似案例',
    '公司受',
    # '贵公司'
]

end_words = [
    '办公室',
    "中心",
    "协会",
    "地质队",
    "药房",
    "批发城",

    '医院',
    '保健院',
    '统计局',
    # '政府',
    '环境保护部',
    '技术学校',
    '船级社',
    '研究所',
    '有限公司',
    '有限责任公司',
    '交易中心',
    '化校园',
    '征拆办',
    '市中区',
    '总局',
    '城管局',
    '党校',
    '工会',
    '卫生院',
    '公安局',
    '制药厂',
    '管理局',
    '房管局',
    '学校',
    '科学中心',
    '体育局',
    '卫生局',
    '大学',
    '气象局',
    '组织服务中心',
    '财政局',
    '农机局',
    '中心站',
    '水务局',
    '中学',
    '学院',
    '档案局',
    '管理处',
    '车务段',
    '电子商行',
    '经营部',
    '戒毒所',
    '总公司',
    '教育局',
    # '商城',
    '公司',
    '铁路局',
    '集团',
    '合作社',
    '网格中心',
    '联合社',
    '电务段',
    '物流部',
    '小学',
    '设计院',
    '民政局',
    '指挥部',
    '林业局',
    '监局',
    '控制中心',
    '车站',
    '人民法院',
    '电脑店',
    '托代理机构',
    '博物馆',
    '电视台',
    '电厂',
    '技术中心',
    '经销处',
    '指导中心',
    # '本级 ',
    '直属处',
    '管理所',
    '机务段',
    '监测站',
    '住建委',
    '管理委员会',
    '建设局',
    '幼儿园',
    '发展中心',
    '电脑商行',
    '物流中心',
    '深圳中心',
    '广告中心',
    '创业基地',
    '建司',
    '事务所',
    '分所',
    '园林局',
    '敬老院',
    '管理站',
    '服务站',
    '培训中心',
    '分院',
    # '检察院',
    '管委会',
    '基地',
    '资源厅',
    '专营店',
    '酷泽西办公',
    '电信局',
    '电信',
    '油田',
    '资源局',
    '地质局',
    '咨询院',
    '改革局',
    '公安厅',
    '事业部',
    '加工点',
    '仲裁院',
    '园林花圃',
    '村委会',
    '销售中心',
    '办事处',
    '检测站',
    '图书馆',
    '联通',
    '福利院',
    '机关',
    '分局',
    '教育中心',
    '管理中心',
    '外事侨务办公室',
    '办公设备商行',
    '发展局',
    '管理部',
    '公路局办公室',
    '出版社',
    '商务局',
    '植物园',
    '园艺场',
    # '工业园',
    '维修中心',
    '贸易商行',
    '审计处',
    '工作部',
    '研究院',
    '广告装饰',
    '机动部',
    '委员会办公室',
    '工程队',
    '泵站',
    '桥家园',
    '农场',
    '保护局',
    '管理办公室',
    '机场高速',
    '防治站',
    '组织部',
    '销售部',
    '工作室',
    '法制报',
    '捐办公室',
    '家具行',
    '关爱中心',
    '联合会',
    '互助中心',
    '救援中心',
    # '监狱',
    '晨光科力普',
    '销毁中心',
    '配套办公室',
    '安置局',
    '施工队',
    '水利局',
    '事务局',
    '宝通科技',
    '供电局',
    '采购所',
    '经销部',
    '储备中心',
    '采购部',
    '采办部',
    '文化用品店',
    '政法委员会',
    '政法委',
    '开发中心',
    '建材商行',
    '税务局',
    '监理中心',
    '审计局',
    '执法大队',
    '开发局',
    '工程建设处',
    '渔业局',
    '国际饭店',
    '代办处',
    '管理服务局',
    '发行中心',
    '国营林场',
    '教育厅',
    '住房保障局',
    '督检测所',
    '用品商店',
    '技术交流中心',
    '办公厅',
    '专卖店',
    '监控中心',
    '党支部',
    '科技局',
    '地质大队',
    '测绘院',
    '资源勘查中心',
    '书店',
    '综治办',
    '警察大队',
    '交通局',
    '工程处',
    '血站',
    '大队',
    '活动中心',
    '监督处',
    '科技中心',
    '服务部',
    '教育办公室',
    '贝斯特',
    '路政局',
    '殡仪馆',
    '托养中心',
    '运输局',
    '中心医院',
    '小组办公室',
    '工程局',
    '信息中心',
    '计划生育局',
    '促进中心',
    '农业局',
    '社会保障局',
    '监察支队',
    '宾馆',
    '工程部',
    '测绘所',
    '航标',
    '环保局',
    '检测中心',
    '器材储运站',
    '保障办公室',
    '财政厅',
    '发改委',
    '司法局',
    '审批局',
    '租赁站',
    '信访局',
    '商贸',
    '商行',
    '中大永盛',
    '畜牧站',
    '搬迁工作办公室',
    '服务所',
    '私城',
    '勘察院',
    '工务段',
    '休养所',
    '运营中心',
    '村委',
    '旅游局',
    '农水局',
    '委机要局',
    '勘测局',
    '程建设办公室',
    '技术馆',
    '林场',
    '粮食局',
    '交易所',
    '畜牧局',
    '四川易达',
    '职中',
    '防空办公室',
    '出版局',
    '医疗中心',
    '专利局',
    '防治院',
    '卫生中心',
    '税局',
    '康复医院',
    '建设厅',
    '供应站',
    '矿',
    '煤矿',
    '宣传部',
    '书院',
    '地震局',
    '部队',
    '车会所',
    '房产局',
    '事务中心',
    '绿化局',
    '执法局',
    '民防局',
    '口岸办',
    '预警中心',
    '设计中心',
    '储备库',
    '保障部',
    '检验测试中心',
    '设备处',
    '技示范场',
    '开发办公室',
    '行政管理局',
    '亿维',
    '平苗圃',
    '改造办公室',
    '林业厅',
    '卫生厅',
    '监测所',
    '牧业局',
    '信用中心',
    '广西中心',
    '电视局',
    '印刷厂',
    '检疫总站',
    '文学馆',
    '监督局',
    '中心校',
    '琴行',
    '株式会社',
    '规划建设和住房保障局',
    '影视局',
    '服务社',
    # '人民政府',
    '信息化厅',
    '文化站',
    '团校',
    '警务站',
    '花木场',
    '设计研究院',
    '认证中心',
    '拍卖中心',
    # '采购中心',
    '苗圃',
    '特警支队',
    '交警支队',
    '管理段',
    '精品店',
    '项目部',
    '电器店',
    '建设管理局',
    '宣教局',
    '（侨务）局',
    '联防队',
    '招待所',
    '电脑行',
    '统建办公室',
    '检验所',
    '分中心',
    '合作联社',
    '学区',
    '警察支队',
    '后勤部',
    '分公司',
    '采购办',
    '电脑城',
    '医疗机构',
    '团',
    '美术馆',
    '寝园',
    '测试所',
    '交通站',
    '保障中心',
    '印务中心',
    '家私',
    '服务店',
    '联社',
    '技术协会',
    '供保中心',
    '监督所',
    
    '车船队',
    '调查队',
    '日报社',
    '工务局',
    '大印电脑',
    '城建局',
    '防检查站',
    '西部中心',
    '开发试验区',
    '警察局',
    '联校',
    '安监站',
    '广播电台',
    '中心完小',
    '机械厂',
    '润景',
    '公路局',
    '特教中心',
    '装备中心',
    '陵园',
    '监测中心',
    '事业局',
    '检测所',
    '文印部',
    '一三一八单位',
    '招商局',
    '水利厅',
    '代建局',
    '党政办',
    '设备中心',
    '市容局',
    '交警队',
    '市直行政事业单位',
    '商场',
    '超市',
    '斑竹园镇',
    '公路管理署',
    '检定测试院',
    '规划局',
    '地质队',
    '服务队',
    '环卫局',
    '检测院',
    '消防支队',
    '建设处',
    '土地房屋局',
    '县教委',
    '养护站',
    '海事局',
    '市政工程维修处',
    '武装部',
    '农牧局',
    '民政厅',
    '粮油日杂商店',
    '派出所',
    '监测院',
    '工业和信息化局',
    '信息化局',
    '国民经济和社会信息化推进中心',
    '资讯中心',
    '海关总署',
    '海关',
    '原料部',
    '结核病防治所',
    '商务中心',
    '烈士纪念馆',
    '就业服务局',
    '解放街道',
    '中心支行',
    '市政工程建设维护中心',
    '消防站',
    '卫生保健中心',
    '区属单位',
    '系统宣传中心',
    '经济贸易局',
    '国营第一牧场',
    '五金机电商店',
    '采购办公室',
    '通电部',
    '勘查局',
    '国土规建局',
    '整理中心',
    '股份',
    '动物园',
    '出租站',
    '纪念馆',
    '广电局',
    '科技总汇',
    '兽医局',
    '本级事业财务',
    '推广站',
    '辅导中心',
    '文印中心',
    '评估中心',
    '住建局',
    '勘查院',
    # '移民局',
    '文具店',
    '工商局',
    '修理厂',
    '门诊部',
    '研发中心',
    '文化厅',
    '计划股',
    '保护中心',
    '防治中心',
    '监察局',
    '生活馆',
    '配件店',
    '家具店',
    '家居店',
    '接待处',
    '海军某部',
    '服务局',
    '十三分部',
    '矫治所',
    '银行',
    '总队',
    '洞井街道',
    '监督站',
    '化工',
    '文化馆',
    '水文局',
    '体育馆',
    '发展合作署',
    '商店',
    '促进局',
    '急救中心',
    '经营中心',
    '福利中心',
    '血液中心',
    '处理中心',
    '公用局',
    '农技中心',
    '批发中心',
    '供应部',
    '风电场',
    '家电城',
    '物贸中心',
    '应用中心',
    '防雷中心',
    '台网中心',
    '实验局',
    '文化局',
    '装备站',
    '分社',
    '填埋场',
    '水利水电局',
    '展销部',
    '能源局',
    '康复中心',
    '训练中心',
    '红十字会',
    '科技部',
    '报社',
    '设计室',
    '电器城',
    '文物局',
    '管理署',
    '制作中心',
    '办公用品总汇',
    '咨询中心',
    '农林局',
    '推广中心',
    '研究中心',
    '社保局',
    '一局',
    '体校',
    '新闻中心',
    '电器行',
    '维护店',
    '调查中心',
    '居委会',
    '（拘留）所',
    '眼病防治所',
    '公园',
    '指导所',
    '市属单位',
    '公路处',
    '热电中心',
    '配送中心',
    '登记中心',
    '经济局',
    '网络中心',
    '体育中心',
    '司法厅',
    '联合总社',
    '社服中心',
    '设备科',
    '文体局',
    '处理站',
    '消防局',
    '促进会',
    '家具城',
    '水利所',
    '博物院',
    '工作站',
    '监察所',
    '检疫局',
    '调查院',
    '二厂',
    '纪委',
    '供热中心',
    '分园',
    '保护厅',
    '改善中心',
    '分行',
    '十八局',
    '南蒲所',
    '合作经济社',
    '销售店',
    '能源部',
    '少年宫',
    '环卫处',
    '运输厅',
    '实验室',
    '垦殖场',
    '基金会',
    '研究会',
    '行政服务大厅',
    '艺术馆',
    '信息港中心',
    '工作局',
    '康仙庄乡',
    '水产局',
    '法院',
    '整治局',
    '采办中心',
    '体育厅',
    '教学中心',
    '研究室',
    '环境局',
    '新体局',
    '农牧厅',
    '设备店',
    '技术局',
    '产权局',
    '计划经营科',
    '支付中心',
    '安置中心',
    '执法中心',
    '指挥中心',
    '建设中心',
    '茶场',
    '干部局',
    '村分站',
    '农业农村局',
    '社区',
    '村',
    '商务厅',
    '原种场',
    '曹庵镇',
    '艺术中心',
    '磁山镇',
    '重点办',
    '镇本级',
    '计划处',
    '检验中心',
    '土肥站',
    '建设站',
    '园区办',
    '储备局',
    '监测总站',
    '规划院',
    '审核中心',
    '社会保险局',
    '安全中心',
    '统战部',
    '处理厂',
    '水厂',
    '净水厂',
    '水泵厂',
    '发改局',
    '卷烟厂',
    '加工厂',
    '器材厂',
    '编码所',
    '教育所',
    '罐头厂',
    '炼铁厂',
    '灯具厂',
    '板材厂',
    '旅游厅',
    '围垦局',
    '经济合作社',
    '教体局',
    '农业厅',
    '整治中心',
    '研究生院',
    '扶贫办',
    '剧院',
    '处理场',
    '信息局',
    '九江',
    '河务局',
    '考试中心',
    '预报台',
    '勘测院',
    '电视总台',
    '中队',
    '广新局',
    '通讯社',
    '财政所',
    '农务局',
    '人大办',
    '监管中心',
    '渔业厅',
    '农工部',
    '监察队',
    '管理总站',
    '疗养院',
    '绿化处',
    '考试院',
    '引航站',
    '南支队',
    '北支队',
    '经理部',
    '林业站',
    '口岸局',
    '城建处',
    '卫计委',
    '职教中心',
    # '镇人民政府',
    # '镇',
    '兽医中心',
    '检疫站',
    '修缮队',
    '气象中心',
    '招标投标中心',
    '粮库',
    '养护中心',
    '监察中心',
    '植检站',
    '测绘局',
    '群众工作中心',
    '管教所',
    '编研中心',
    '消防队',
    '健身中心',
    # '科技园',
    '监督中心',
    '打印部',
    '门市',
    '字行',
    '文印',
    '器材店',
    '家俱城',
    '健康局',
    '油厂',
    '救援支队',
    '媒体中心',
    '管教所',
    '医疗保障局',
    # '委员会',
    # '本级',
    '卫生所',
    '执业点',
    '南院',
    '抢救中心',
    '护理院',
    '医务室',
    '机械组',
    '就业局',
    '会计师协会',
    '电力',
    '试验站',
    '铝业',
    '营业部',
    '驰宏',
    '自动化',
    '派驻组',
    '计划部',
    '应急局',
    '工务中心',
    '营销部',
    '市场部',
    '材料部',
    '物美',
    '冶炼厂',
    '考核中心',
    '高中',
    '科创园',
    '总站',
    '物资部',
    '某单位',
    '孵化园',
    '机场',

    
    # todo:
    "店",
    "厂",
    "广场",
]


end_words_re = [
    "[一二三四五六七八九十]+院",
    "[一二三四五六七八九十]+队",
]


key_words_A = [
    '招标公告',
    '采购预告',
    '招标预告',
    '招标二次公告',
    '采购二次公告',
    '答疑澄清',
    '澄清公告',
    '答疑公告',
    '补疑公告',
    '补遗公告',
    '招标补遗',
    '项目补遗',
    '答疑补遗',
    '竞买预告',
    '预告公告',

]

key_words_B = [
    '中标',
    '单一来源',
    '成交',
    '结果',
    '候选',
    '合同',
    '确认',
    '开标',
    '中选',

]

key_words_C = [
    '单一来源',

]

key_words_D = [
    '采购公告',
    '询价公告',
    '磋商公告',
    '竞争性谈判',

]

key_words_E = [
    '变更公告',

]

key_words_F = [
    '招标文件',
    '采购文件',
    '标书',
    '询价文件',
    '磋商文件',
    '报名时间',
    '资格要求',
    '资质要求',
    '报名截止时间',

]

