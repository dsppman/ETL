target_keywords = [
    #"招\\s*标\\s*单\\s*位\\s*(:|：|名\\s*称){1}",
    "(采\\s*购\\s*|招\\s*标\\s*)?代\\s*理\\s*机\\s*构\\s*(信\\s*息\\s*)?(:|：|名\\s*称|全\\s*称){1}",
    "(采\\s*购\\s*|招\\s*标\\s*)?代\\s*理\\s*(信\\s*息\\s*)?(:|：|名\\s*称|全\\s*称){1}",
    "代\\s*理\\s*机\\s*构\\s*信\\s*息\\s*（如有）\\s*(:|：|名\\s*称|全\\s*称){1}",
    '代理机构(:|：){1}',
    '招标代理(:|：){1}',
    '招标代理',
    '代理',
    '代理机构: '
    '联系人（代理机构）(:|：){1}',
    '代理机构全称:',
    '招标代理机构全称：'
    '招标代理机构',
    '代理单位',
    '代理人',
    '代理公司',
    '委托机构',
    '委托公司',
    '业主/代理单位：'
    '委托单位',
    '询价代理',
    '磋商代理',
    '竞价代理',
    '代理中介',
    '服务中介',
    '招标机构:',
    # '采购代理机构:',
    '代理机构联系方式：',
    # '\\s*代理机构\\s*[:|：]?[为]?',
    # '\\s*招标代理\\s*[:|：]?[为]?'

]

para_formats = [
    "[\u0391-\uFFE5]{4,20}（招标人建设单位）",
    #"受\\s*[\\s\\S]{3,40}委托",
    "委托[,，]?\\s*[\u0391-\uFFE5]{4,20}\\s*以\\s*[\u0391-\uFFE5]{4,20}\\s*方式",
    "[\u0391-\uFFE5]{4,20}\\s*（招标代理）受\\s*[\u0391-\uFFE5]{4,20}\\s*（采购人）委托",
    "[\u0391-\uFFE5]{4,20}\\s*受委托",
    "由\\s*[\u0391-\uFFE5]{4,20}\\s*组织招标",
]

fuzzy_keywords = [
    #'发布人', 
    #'发布单位', 
    #'发布公司', 
    #'单位名称', 
    #'公司名称', 
    #'单位', 
]

similar_words = [
    '采购管理中心',
    '采购中心',
    '交易中心',
    '招标中心',
    '代理中心',
    '咨询中心',
    '招投标中心',
    '招标有限责任公司',
    '招标有限公司',
    '招投标管理有限公司',
    '招投标有限公司',
    '代理有限责任公司',
    '代理有限公司',
    '项目管理服务有限公司',
    '项目管理有限公司',
    '工程管理有限公司',
    '咨询集团有限公司',
    '咨询服务有限公司',
    '咨询有限公司',
    '事务所'
]

black_words = [
    '中标',
    '供应商',
    '成交',
    '中选',
    '承包',
    '乙方',
    '竞拍',
    '竞价',
    '询价',
    '磋商',
    '入围',
    '生产',
    '选取',
]

end_words = [
    '公司', 
    '集团',  
    '招标办', 
    '分中心',
    '采购中心', 
    '物资中心', 
    '集采中心', 
    '办公室', 
    '采购部', 
    '采办部', 
    '交易中心',
    '招（投）标公司',
    '咨询(北京)有限公司',
    '代理中心',
    '交易科',
    '服务中心',
    
]