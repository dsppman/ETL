    #!/usr/bin/env python
# -*- coding: utf-8 -*-


target_keywords = [
    "采\\s*购\\s*人\\s*[:：]",
    "招\\s*标\\s*单\\s*位\\s*(:|：|名\\s*称){1}",
    "招\\s*标\\s*单\\s*位\\s*(:|：|名\\s*称){1}",
    "招\\s*标\\s*组\\s*织\\s*机\\s*构\\s*(:|：|名\\s*称){1}",
    "采\\s*购\\s*单\\s*位\\s*(:|：|名\\s*称){1}",
    "发\\s*包\\s*单\\s*位\\s*(:|：|名\\s*称){1}",
    "甲\\s* 方\\s*(:|：|名\\s*称){1}",
    "采\\s*购\\s*人\\s*(:|：|名\\s*称){1}",
    "招\\s*标\\s*人\\s*(:|：|名\\s*称){1}",
    "\\s*采\\s*购\\s*人\\s*\\(\\s*甲\\s*方\\s*\\)\\s*：",
    "建设单位\\(招标人\\)",
    "委托单位名称：",
    "采购人联系方式名 称：",
    "业\\s*主\\s*单\\s*位\\s*(:|：|名\\s*称){1}",
    "招标（采购）人(:|：|名\\s*称){1}",
    "采购人/招标代理机构：",
    "询\\s*价\\s*人\\s*(:|：|名\\s*称){1}",
    "采\\s*购\\s*执\\s*行\\s*方\\s*(:|：|名\\s*称){1}",
    "招\\s* 标 \\s*方\\s*(:|：|名\\s*称){1}",
    "用户单位：",
    "招标\\(采购\\)人名称：",
    "建\\s*设\\s*单\\s*位\\s*：",
    "信息发布部门",
    "采 购 商：",
    "采购商",
    "招标（采购）人名称：",
    "招标组织部门：",
    "采购服务单位(:|：){1}",
    "采购人名称[:：]",
    "招标方：",
    "采购实施单位：",
    "该项目招标人为：",
    "询价书企业：",
    "合同主体单位",
    "项目法人",
    "工程询价单位：",
    "招商单位：",
    "发布部门：",
    "采购商：",
    "发布公司：",
    "招标公司名称：",
    "实际采购人为",
    "采购人为[:|：]?",
    "需 求 方：",
    "项目业主（全称）：",
    "委托抽取单位：",
    "招租方：",
    "招商人：",
    "采购人（全称）：",
    "招标监督单位：",
    "^单位：",
    "^名称：",
    "遴选人名称：",
    "公示单位：",
    "招\\s*标\\s*单\\s*位",
    "招\\s*标\\s*机\\s*构\\s*(:|：){1}",
    "招\\s*标\\s*机\\s*构\\s*",
    "招\\s*标\\s*部\\s*门",
    "招\\s*标\\s*组\\s织\\s机\\s*构",
    "招\\s*标\\s*人",
    "采\\s*购\\s*单\\s*位",
    "采\\s*购\\s*（招标）\\s*单\\s*位",
    "采\\s*购\\s*机\\s*构",
    "^采\\s*购\\s*人",
    "采\\s*购\\s*（招标）\\s*人",
    "采\\s*购\\s*方[^式]",
    "采\\s*购\\s*人",
    "采购人",
    "比\\s*选\\s*人",
    "项\\s*目\\s*业\\s*主",
    "集\\s*采\\s*机\\s*构",
    "询\\s*价\\s*单\\s*位",
    "询 \\s*价 \\s*人",
    "业\\s*主",
    "谈\\s*判\\s*人 ",
    "发\\s*包\\s*单\\s*位",
    "发\\s*包\\s*方",
    "发\\s*包\\s*人[:：]",
    "需\\s*求\\s*单\\s*位",
    "委\\s*托\\*s单\\s*位",
    "申\\s*购\\s*单\\s*位",
    "联\\s*系\\s*单\\s*位",
    "甲\\s*方",
    "建\\s*设\\s*单\\s*位",
    "约\\s*谈\\s*人",
    "建\\s*设\\s*（招标）\\s*单\\s*位",
    "建\\s*设\\s*项\\s*目\\s*单\\s*位",
    "需方：",
    "采购用户(:|：){1}",
    "项\\s*目\\s*单\\s*位",
    "委托单位",
    "发起单位：",
    "单 位：",
    "比价人",
    "采购用户:",
    "采购人联系人：",
    "集中采购机构：",
    "发布单位",
    "邀标人：",
    "批准单位:",
    "竞价单位：",
    "委托人",
    "采购组织",
    "招标人（公章）： ",
    "需求公司：",
    "组织单位",
    "招租人",
    "购买主体",
    # "发布人",
    "询价书名称(：)?",
    "转载时请注明出处：",
    "采购部门名称",
    "业主单位：",
    "交易单位：",
    "招标方案核准\\(备案\\)部门：",
    "项目业主为",
    "批准单位",
    "采购商信息",
    "项目实施机构：",
    "委托方",
    "询价人",
    "询价单位[:：]",
    "发布机构名称",
    "交易单位",
    "招标人名称：",
    "采购人信息：",
    "[采|釆]\\s*购\\s*人\\s*信\\s*息\\s*(:|：|名\\s*称){1}",
    "采购人[:：]",
    "医\\s*院\\s*(:|：|名\\s*称){1}",
    "转\\s*让\\s*方\\s*(:|：|名\\s*称){1}",
    '询价公告名称： ',
    '卖方[:：]',
    '招标人或代理机构[:：]',
    "采\\s*购\\s*方[:：]\n",
    "出租（让）方\\s*",
    "项目（法人）单位",
    "建设单位[:：\\s][^\(（)]",
    "所有权人[:：]?",
    "采\\s*购\\s*机\\s*构[:：]?\\s*\n",
    #"接收单位[:：]?",
    "招标人为\\s*[:：]?",
    "采购单位（含部门）[:：]?",
    "甲方\(采购人\)[:：]?",
    "采购公示名称[:：]?",
    "业主联系方式\\s*公司名称[:：]",
    "发布机构[:：]?",
    '招标人：',
    '发布机构：',
    '甲方：',
    '甲 方：',
    ' 发布公司：',
    '招标单位：'
    '比选人为',
    '评选人：',
    '比 选 人：',
    "比\\s*选\\s*人\\s*[:：]",
    '名称（盖章）',
    '需求公司:',
    # '招标组织：'

    "项\\s*目\\s*单\\s*位[:：\\s]",
    "项\\s*目\\s*业\\s*主[:：\\s]",
    "委\\s*托\\s*人[:：\\s]",
    "业\\s*主\\s*名\\s*称[:：\\s]",
    "业\\s*主\\s*单\\s*位[:：\\s]*",

    
    # todo: 
    "所\\s*属\\s*公\\s*司[:：\\s]",
]


param_formats_v1 = [
    # 注意词条顺序, 匹配到一个后即终止

    "受\\s*([^，？。！\\s]*?)委托",
    "由\\s*([^，？。！\\s]*?)委托",

    
    # todo: 精简
    "([^，？。！\\s]*?)将[^，？。！]*?进行[^，？。！]*?招投标",
    "([^，？。！\\s]*?)定于[^，？。！]*?进行[^，？。！]*?招投标",
    "([^，？。！\\s]*?)就[^，？。！]*?进行[^，？。！]*?招投标",
    "([^，？。！\\s]*?)将[^，？。！]*?进行[^，？。！]*?招标",
    "([^，？。！\\s]*?)定于[^，？。！].*?进行[^，？。！]*?招标",
    "([^，？。！\\s]*?)就[^，？。！]*?进行[^，？。！]*?招标",
    "([^，？。！\\s]*?)将[^，？。！]*?进行.*?交易",
    "([^，？。！\\s]*?)定于[^，？。！]*?进行[^，？。！]*?交易",
    "([^，？。！\\s]*?)就[^，？。！]*?进行[^，？。！]*?交易",
    "([^，？。！\\s]*?)定于[^，？。！]*?进行[^，？。！]*?招租",

    
    "([^，？。！\\s]*?)对[^，？。！]*?采购",
    #"([^\\s]*?)对[^，？。！]*?项目",

    "([^，？。！\\s]*?)\"[^，？。！]*?项目[^，？。！]*?采购",
    "([^，？。！\\s]*?)\"[^，？。！]*?项目[^，？。！]*?招标",
    "([^，？。！\\s]*?)\“[^，？。！]*?项目[^，？。！]*?采购",
    "([^，？。！\\s]*?)\“[^，？。！]*?项目[^，？。！]*?招标",
]


para_formats = [
    "[\u0391-\uFFE5]{4,20}（招标人建设单位）",
    "受\\s*[\\s\\S]{3,40}委托",
    "由\\s*[\\s\\S]{3,40}委托",
    "由\\s*[\u0391-\uFFE5]{4,20}\\s*委托",
    "由\\s*[\u0391-\uFFE5]{4,20}\\s*组织的",
    "国投钦州发电有限公司对（进口）FAG轴承 采购",
    "[\u0391-\uFFE5]{4,20}\\s*拟建的",
    "由\\s*[\u0391-\uFFE5]{4,20}\\s*建设的",
    "[\u0391-\uFFE5]+\\s*采购已采购完毕",
    "经\\s*[\u0391-\uFFE5]+\\s*评标委员会评议并经审批同意",
    "由我司[\u0391-\uFFE5]+\\s*举行的[\u0391-\uFFE5]+\\s*采购项目",
    "由\\s*[\\s\\S]{4,20}进行的\\s*[\\s\\S]+采购项目已经结束",
    "\\s*[\\s\\S]+项目\\s*[\\s\\S]+预中标候选人公示",
    "\\s*[\\s\\S]+保险中标公示",
    "\\s*[\u0391-\uFFE5]+\\s*完成了\\s*[\\s\\S]+的招标工作，",
    "关于\\s*[\\s\\S]+谈判采购项目成交通知书的通知",
    "\\s*[\\s\\S]+评标结果如下，",
    "在\\s*[\u0391-\uFFE5]+组织的下列货物的询价采购中，",
    "，招标人为\\s*[\u0391-\uFFE5]+，",
    "[\u0391-\uFFE5]+在\\s*[\\s\\S]+采用网上直购的方式采购商品",
    "根据[\u0391-\uFFE5]+关于\\s*[\\s\\S]+的评审意见",
    ",\\s*[\u0391-\uFFE5]+采购管理办公室谨对积极参与本项目投标的供应商表示衷心的感谢",
    "[\u0391-\uFFE5]+就\\s*[\\s\\S]+采购在\\s*[\\s\\S]+进行了网上电子询比，",
    "现[\u0391-\uFFE5]+邀请合格的潜在投标人参加工程的投标",
    "[\u0391-\uFFE5]+（以下简称“采购人”）",
    "[\u0391-\uFFE5]{5,20}\\(以下简称\"采购人\"\\)",
    "[\u0391-\uFFE5]+\\s*-\\s*竞价结果详情",
    "[\u0391-\uFFE5]+在平台上已完成评标工作",
    "[\u0391-\uFFE5]+的2018年徐工挖机企业宣传片（中英）策划及制作正在进行招标,",
    "[\\s\\S]+由我单位组织的[\u0391-\uFFE5]+的[\\s\\S]+项目采购",
    "中铁隧道集团三处有限公司南通市轨道交通1号线03标",
    "[\\s\\S]+智慧校园的在线询价结果",
    "对[\\s\\S]{5,30}进行公开招标，",
    "[\\s\\S]+的[\\s\\S]+正在进行询比价",
    "[\\s\\S]+组织以下采购需求",
    "石家庄良村热电有限公司雨水泵配件询价单询价结果通知书",
    "[\\s\\S]+。招标人（项目业主）为[\\s\\S]+",
    "[\\s\\S]+新建项目代理比选",
    "关于[\\s\\S]{5,20}采购公示",
    "[\\s\\S]{5,20} ：[\\s\\S]+你单位申请采购的下列物品符合定点采购要求，请按规定程序采购。",
    "接 到 本 通 知 书 后 [\\s\\S]+与 我 方 签 订 [\\s\\S]{0,20} 合 同",
    "[\\s\\S]{5,20}的[\\s\\S]{5,50}正在进行询比",
    "你单位收到中标通知书后，[\\s\\S]+与招标人签订合同",
    "[\\s\\S]{5,20}正进行询比价采购，",
    "就[\\s\\S]{5,20}项目进行国内公开招标",
    "[\\s\\S]{5,20}- 竞价公告",
    "[\\s\\S]{5,20}的[\\s\\S]+正在(询比价|进行竞价)",
    "[\\s\\S]{5,20}就[\\s\\S]+进行比价采购",
    "竞价结果详细\\(\\d{11}\\)----[\\s\\S]{5,20}",
    "[\\s\\S]{5,20}的[\\s\\S]{5,20}正在进行",
    "[\\s\\S]{5,25}就[\\s\\S]{5,50}进行招标采购",
    "[\\s\\S]{5,20}对[\\s\\S]{5,50}进行采购寻源",
    "[\\s\\S]{5,20}的[\\s\\S]{5,50},现公开邀请合格投标人参加报价。",
    "[\\s\\S]{5,20}就[\\s\\S]{5,30}已依照固定价比选方式，",
    "根据法律、法规、规章和招标文件的规定，[\\s\\S]{5,20}的",
    "需要开发票，[\\s\\S]{5,20}",
    "神华蒙西煤化股份有限公司计划于[\\s\\S]{5,15}开展[\\s\\S]{5,15}在线竞价销售",
    "，勘察现场后统一交流，地点为[\u0391-\uFFE5]{5,10}",
    "对[\u0391-\uFFE5]{4,20}安徽创新馆项目配电箱进行公开询价采购。",
    "[\u0391-\uFFE5]{4,20} 拟对",
    "[\u0391-\uFFE5]{4,20}定于[\\s\\S]{5,50}进行招投标",
    "[\u0391-\uFFE5]{4,30}正在进行招标",
    " 请你方在接到本通知书后的30日内到 [\u0391-\uFFE5]{4,30}与我方签合同。",
    "[\u0391-\uFFE5]{4,30}拟采购",
    "关于[\\s\\S]{5,50}征求意见公示",
    "[\u0391-\uFFE5]{4,30}就[\\s\\S]{5,50}进行了网上电子招标",
    "本招标项目招标人为[\u0391-\uFFE5]{4,30}",
    "关于[\\s\\S]{5,50}项目招标公告 ",
    "\\s*如对以上公示有疑问，请在三个工作日内以书面形式与[\u0391-\uFFE5]{4,30}联系。 ",
    "[\u0391-\uFFE5]{4,30}拟[就|在]{1}",
    "[\u0391-\uFFE5]{4,30}现就[\\s\\S]{4,30}进行磋商方式采购",
    "[\u0391-\uFFE5]{4,30}就[\\s\\S]{5,50}进行了询比价采购，",
    "为满足[\u0391-\uFFE5]{4,30}的发展需要，",
    "[\u0391-\uFFE5]{4,30}就[\\s\\S]{5,50}进行询比价采购,现公开邀请合格投标人进行网上电子报价。",
    "屏山县人力资源和社会保障局 关于[\\s\\S]{5,50}的公示",
    "[\\s\\S]{4,50}发布了中标候选人公示",
    "项目业主为[\u0391-\uFFE5]{4,20}",
    "[\u0391-\uFFE5]{4,20}（建设单位）",
    #"\\s*请与[\u4e00-\u9fa5]{4,20}联系",
    "[\u0391-\uFFE5]{4,20}建设的",
    "为加强[\u0391-\uFFE5]{4,20}管理，",
    "为[\u0391-\uFFE5]{4,20} 公开选取",
    "[\u0391-\uFFE5]{4,50}在[\\s\\S]{3,5}市中区政务服务中心开标",
    "为[\u0391-\uFFE5]{4,50} 公开选取工程设计中介服务机构",
    "[\\s\\S]+已如期开标",
    "[\u0391-\uFFE5]{4,50} 对下列采购项目",
    "[\u0391-\uFFE5]{4,30}定于",
]

fuzzy_keywords = [
    #"项目名称",
    "项目采购名称",
    #"标段名称",
    #"招标项目",
    "工程名称",
    "询价名称",
    "标包名称",
    "采购单名称",
    "询价单名称",
    "发\\s*布\\s*人[:：\\s]",
    "所\\s*需\\s*工\\s*厂[:：\\s]",
]


end_words = [
    
    # todo:
    "局",

    '医院',
    '保健院',
    '统计局',
    '政府',
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
    '管理局',
    '房管局',
    '学校',
    '科学中心',
    '体育局',
    '卫生局',
    '大学',
    '气象局',
    '服务中心',
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
    #'商城',
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
    #'本级 ',
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
    '检察院',
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
    '工业园',
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
    '监狱',
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
    '人民政府',
    '信息化厅',
    '文化站',
    '团校',
    '警务站',
    '花木场',
    '设计研究院',
    '认证中心',
    '拍卖中心',
    '采购中心',
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
    '办公室',
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
    '移民局',
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
    '农业农村厅',
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
    '镇人民政府',
    '镇',
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
    '科技园',
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
    '委员会',
    #'本级',
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
    '洗浴中心',
    '救护中心',
    '运动中心',
    '绿化中心',
    '数据中心',
    '养护所',
    '保护站',
    '维护中心',
    "某部队",
    '某部',
    '分校',
    '本级行政',
    '街道办事处',
    '中心血库',
    '产业局',
    '管理有限公司',
    '救护队',
    '器具中心',
    "电厂",
]
