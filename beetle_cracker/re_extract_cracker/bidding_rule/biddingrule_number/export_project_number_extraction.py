# encoding: utf-8

import json

import click
import os
import re
import pymysql
import xlwt
from time import *


def handler_content_one(split_content):
    # 第一次处理
    # print('第一次处理前的值：',split_content)
    #split_content = ''.join(a_content.split())
    # 替换空格
    split_content = split_content.replace(" ", "")
    # 替换\n
    split_content = split_content.replace("\n", "")
    # 针对</p><p>3.项目名称这种情况特殊处理
    sub_one = re.compile(r'>[0-9].[\u4E00-\u9FA5A-Za-z_]')
    split_content = sub_one.sub('>', split_content)
    # 替换字符中的Html标签
    sub_two = re.compile(r'<([^>]*)>')
    split_content = sub_two.sub('', split_content)
    return split_content


def handler_content_two(result_content):
    # 第二次处理
    # print('第二次处理前的值:',result_content)
    start_index = 0
    end_index = len(result_content)
    #获取字符串中出现的数字
    str_num = re.findall('\d+', result_content)
    str_abc = re.findall('[A-Za-z]+', result_content)

    if len(str_num):
        temp_num = str_num[0]
        num_index = result_content.find(temp_num)
        if num_index != -1:
            start_index = num_index
    if len(str_abc):
        temp_abc = str_abc[0]
        str_index = result_content.find(temp_abc)
        if str_index != -1:
            if start_index == 0:
                start_index = str_index
            else:
                start_index = min(start_index, str_index)
    result_content = result_content[start_index:end_index]
    str_chinese = re.findall('[\u4e00-\u9fa5]+', result_content)
    if len(str_chinese):
        temp_chinese = str_chinese[0]
        chinese_index = result_content.find(temp_chinese)
        if chinese_index != -1:
            end_index = min(chinese_index, end_index)
            result_content = result_content[0:end_index]
    return result_content


def handler_content_three(result_content):
    # 替换标点符号
    # print('第三次处理前的值:',result_content)
    all_punc = '，。、【】[]“”：；;（）（〕《》‘’{}？！⑦()、%^℃：.?'
    result_content = result_content.translate(str.maketrans('', '', all_punc))
    # ID：这种情况进行特殊处理
    # m_idnex = result_content.find(':')
    # if m_idnex != -1:
    #     result_content = result_content[m_idnex:len(result_content)]
    # 替换
    temp_index = result_content.find("<")
    if temp_index != -1:
        result_content = result_content[0:temp_index]
    # http://这种情况进行处理
    h_idnex = result_content.find('http:')
    if h_idnex != -1:
        result_content = ' '
    # ID：这种情况进行特殊处理
    m_idnex = result_content.find(':')
    if m_idnex != -1:
        result_content = result_content[m_idnex+1:len(result_content)]
    # print('第三次处理后得值：',result_content)
    return result_content


def data_cleaning(result_content):
    # 进行最后的数据清洗，把带有特殊符号的编号去除
    search_result = re.findall('[，。：；“！“”".......、]', result_content)
    if len(search_result) or len(result_content) < 6:
        return True
    else:
        return False


def handler_contains_value(trans_dict_row):
    # 对具有包含关系的编号进行处理
    content = trans_dict_row['content']
    content_list = content.split('，')
    if len(content_list) > 1:
        for _ in content_list:
            if len(_) > 6:
                trans_dict_row['content'] = _
                break

    return trans_dict_row


def handler_excel(trans_dict, outpath_dir):
    # 创建Excel操作对象
    # 存储路径
    save_dir= os.path.join(outpath_dir,'projectNumberExtraction.xlsx')
    table_case_tile_list = [
        "contentid",
        "提取到的数据（多个以，隔开）"
    ]
    if os.path.exists('projectNumberExtraction.xlsx'):
        os.remove('projectNumberExtraction.xlsx')
        print('存在文件，删除文件成功！')
    # 使用xlwt模块创建一个Excel对象
    excel_file = xlwt.Workbook()
    # 在Excel文件里创建一个sheet_name
    sheet = excel_file.add_sheet('招标编号数据提取')
    # 在工作表的第一行写入标题
    a = 0
    for i in table_case_tile_list:
        sheet.write(0, a, i)
        a += 1
    # 从工作表第二行开始写入内容
    excel_num = 1
    for k, v in trans_dict.items():
        sheet.write(excel_num,0,k)
        sheet.write(excel_num, 1, v['content'])
        excel_num += 1

    excel_file.save(save_dir)
    print('导出完成')


"""
#新内容库导出数据
227288343:ZRZZBDL-HB-20210602
227288343:ZRZZBDL-HB-20210602
227288342:WSCG0100013017961557A07EE1
227288341:MXLJXQ-2021002
227288340:GSHD2021YG-022
227288339:WSCG03000130179115BFBC64DD
227288338:WSCG03000230178716A31400F7
227288337:WSCG03000130179215C25B0305
227288335:WSCG03000130178536802ACD4
227288334:WSCG030001301786368040248
227288333:WSCG18000130178015A8D25D56
227288332:WSCG0100013017791556E64206
227288326:256471214
227288326:256471214
227288324:348580747
227288324:348580747
227288322:WSCG05000430176532DC683F4
227288321:WSCG14000830176633CEBBA3F
227288320:WSCG193017761680013403
227288319:WSCG19301775168000FA82
227288318:WSCG193017731680008C56
227288317:WSCG05000430176132D1B7D9F
227288316:WSCG193017741680013BCE
227288314:WSCG1930176837432CA17
227288313:WSCG193017771680016A55
227288312:WSCG03000630176935B733A6B
227288310:WSCG03000130175915C25AE283
227288309:WSCG0100143017631728F52D9C
227288308:WSCG03000230175616A313FF40
227288307:WSCG0100143017641728F546C0
227288306:WSCG0100143017621728F52A67
227288305:WSCG03000230175716A31A6312
227288304:255851214
227288304:255851214
227288288:370213051050202100017
227288288:370213051050202100017
227288287:370213051050202100018
227288287:370213051050202100018
227288286:CSKHBJ2021061308
227288285:CSKHBJ2021061310
227288284:CSKHBJ2021061309
227288279:1116479000007948719
227288279:1116479000007948719
227288277:1677761000007948808
227288277:1677761000007948808
227288275:1612900000007922684
227288275:1612900000007922684
227288273:1116479000007948810
227288273:1116479000007948810
227288271:1163660000007948412
227288271:1163660000007948412
227288270:1116479000007948720
227288270:1116479000007948720
227288268:1655304000007948729
227288268:1655304000007948729
227288266:1116479000007948717
227288266:1116479000007948717
227288265:1849987000007948552
227288265:1849987000007948552
227288264:1116479000007948809
227288264:1116479000007948809
227288260:1345737000007948818
227288260:1345737000007948818
227288259:1390710000007941158
227288259:1390710000007941158
227288257:1823584000007948734
227288257:1823584000007948734
227288256:1163660000007948416
227288256:1163660000007948416
227288254:1116479000007948716
227288254:1116479000007948716
227288246:1709635000007948742
227288246:1709635000007948742
227288244:1390710000007941204
227288244:1390710000007941204
227288242:1709635000007948743
227288242:1709635000007948743
227288240:1509978000007939336
227288240:1509978000007939336
227288239:1495886000007948333
227288239:1495886000007948333
227288237:1253163000007946121
227288237:1253163000007946121
227288234:1470530000007921630
227288234:1470530000007921630
227288233:1509978000007938781
227288233:1509978000007938781
227288232:1458909000007918145
227288232:1458909000007918145
227288231:1175507000007948849
227288231:1175507000007948849
227288230:1329098000007948539
227288230:1329098000007948539
227288229:1687880000007941574
227288229:1687880000007941574
227288226:1470530000007922040
227288226:1470530000007922040
227288225:1398935000007863761
227288225:1398935000007863761
227288223:1422978000007948779
227288223:1422978000007948779
227288222:1075609000007944798
227288222:1075609000007944798
227288221:1408290000007922916
227288221:1408290000007922916
227288219:1843882000007948754
227288219:1843882000007948754
227288217:1221183000007882705
227288217:1221183000007882705
227288213:1445024000007948797
227288213:1445024000007948797
227288209:1926811000007862876
227288209:1926811000007862876
227288208:1221183000007882999
227288208:1221183000007882999
227288204:1445024000007948796
227288204:1445024000007948796
227288203:1575670000007894315
227288203:1575670000007894315
227288202:1196945000007909473
227288202:1196945000007909473
227288200:1571017000007948910
227288200:1571017000007948910
227288199:1081670000007891074
227288199:1081670000007891074
227288196:1685348000007938252
227288196:1685348000007938252
227288193:1634291000007936962
227288193:1634291000007936962
227288191:1697291000007948783
227288191:1697291000007948783
227288187:WSCG0300093017493929C313B
227288186:WSCG01001530175315CBA34271
227288184:WSCG0300093017523923DEF20
227288183:WSCG03000930175039235BA2A
227288182:WSCG03000930175139239751D
227288181:WSCG030009301746392943276
227288180:WSCG020001301744170A2C46CE
227288179:WSCG05000430175532DC553E7
227288178:WSCG02000130175417406EBA74
227288176:WSCG02000130174817082081F5
227288175:WSCG0300093017453929C2174
227288174:WSCG05000430174232B11D751
227288173:WSCG16000130173828A8EBFFE
227288172:WSCG030009301747392368F27
227288171:WSCG020001301743170A2CBBF2
227288170:WSCG19301734156B62CC4E
227288169:WSCG19301741156C9F2CFC
227288168:WSCG0500023017362AFE5173B
227288166:032561596
227288166:032561596
227288163:491791122
227288163:491791122
227288158:371831627
227288158:371831627
227288152:ZJYC-20210615
227288152:ZJYC-20210615
227288150:SDGP370100202101027719
227288150:Z3701132021061939715
227288149:SDGP371300202101017453
227288149:32111371320210701
227288148:21061987942492
227288148:21061987942492
227288147:21061957964290
227288147:21061957964290
227288146:21061906333902
227288146:21061906333902
227288144:21061971539822
227288144:21061971539822
227288143:21061914421553
227288143:21061914421553
227288142:21040274566817
227288142:21040274566817
227288138:370213051050202100019
227288138:370213051050202100019
227288135:WSCG1300133017282EC749982
227288134:WSCG0500023017312A5A1736E
227288133:WSCG1300133017272EC73BE4C
227288132:WSCG0500013017261643A4EA7C
227288131:WSCG180001301729161D754D52
227288128:1115683000007948051
227288128:1115683000007948051
227288012:S20210610010
227288012:S20210610010
227288008:2021-06-276
227288008:2021-06-276
227288005:446750957
227288005:446750957
227288004:415254281833
227288004:415254281833
227288003:404146601833
227288003:404146601833
"""



@click.command()
@click.option('--outpath_dir')
@click.option('--start')
@click.option('--end')
def main(outpath_dir, start, end):
    # print('outpath_dir：',outpath_dir)
    # print('size：',size)
    host = 'rm-2ze48a7s45aj1vrwsuo.mysql.rds.aliyuncs.com'
    user = 'tjdata'
    password = 'tjdata1-1'
    data_name = 'bigdata'
    begin_time = time()
    # 打开数据库连接
    db = pymysql.connect(host=host, user=user, password=password, db=data_name, port=3306)
    # 使用cursor（）获取操作游标
    cur = db.cursor()
    # 查询操作
    sql = "select contentid, content from allcontet order by contentid desc limit %s , %s" % (start, end)
    #print('spl:',sql)
    #sql = "select contentid, content from getcodedata limit %s , %s" % (start, end)
    # sql = "select contentid, content from allcontet where contentid = 227288324"
    try:
        cur.execute(sql)
        results = cur.fetchall()
    except Exception as e:
        raise e
    finally:
        db.close()
    one_time = time()
    print('数据库查询使用了:',int(one_time - begin_time))

    keyword_map = [
        u'采购单编号',
        u'项目编号',
        u'招标编号',
        u'询价单编号',
        u'标段编号',
        u'交易编号',
        u'合同号（订单号）',
        u'采购编号',
        u'项目标号',
        u'发包编号',
        u'公告编号',
        u'合同编号',
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
        u'编号',
    ]
    trans_dict = dict()
    for row in results:
        content = row[1]
        search_num = 0
        for keyword in keyword_map:
            num = content.count(keyword)
            if num == 1:
                search_num += 1
                start_index = content.find(keyword)
                if keyword == '编号':
                    if content[start_index - 2:start_index + 2] == '注册编号':
                        continue
                record_index = start_index
                if start_index != -1:
                    # 首先对注册编号匹配进行剔除
                    if keyword == '编号':
                        if content[start_index - 2:start_index + 2] == '注册编号':
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
                            continue
                    end_index = start_index +70
                    result_content = content[record_index: end_index]
                    result_content = handler_content_one(result_content)
                    result_content = handler_content_two(result_content)
                    result_content = handler_content_three(result_content)
                    # 在最后进行一次数据的清晰，把含有不规则符号的字符串去掉
                    is_need = data_cleaning(result_content)
                    if is_need:
                        result_content = ' '
                    if row[0] in trans_dict.keys():
                        if result_content not in trans_dict[row[0]]['repeat']:
                            old_content = trans_dict[row[0]]['content']
                            if result_content != ' ':
                                trans_dict[row[0]]['repeat'].append(result_content)
                                if old_content != '':
                                    trans_dict[row[0]]['content'] = old_content + "，" + result_content
                                else:
                                    trans_dict[row[0]]['content'] = result_content
                    else:
                        repeat_list = list()
                        if result_content != ' ':
                            repeat_list.append(result_content)
                            trans_dict[row[0]] = {
                                'content': result_content,
                                'repeat':repeat_list
                            }
                        else:
                            trans_dict[row[0]] = {
                                'content': '',
                                'repeat': repeat_list
                            }
                    # show_content = str(row[0])  + ':' + result_content
                    # print(show_content)
            else:
                while num>0:
                    search_num += 1
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
                                num -= 1
                                continue
                        end_index = record_index + 70
                        result_content = content[record_index: end_index]
                        result_content = handler_content_one(result_content)
                        result_content = handler_content_two(result_content)
                        result_content = handler_content_three(result_content)
                        # 在最后进行一次数据的清晰，把含有不规则符号的字符串去掉
                        is_need = data_cleaning(result_content)
                        if is_need:
                            result_content = ' '
                        if row[0] in trans_dict.keys():
                            if result_content not in trans_dict[row[0]]['repeat']:
                                old_content = trans_dict[row[0]]['content']
                                if result_content != ' ':
                                    trans_dict[row[0]]['repeat'].append(result_content)
                                    if old_content != '':
                                        trans_dict[row[0]]['content'] = old_content + "，" + result_content
                                    else:
                                        trans_dict[row[0]]['content'] =  result_content
                        else:
                            repeat_list = list()
                            if result_content != ' ':
                                repeat_list.append(result_content)
                                trans_dict[row[0]] = {
                                    'content': result_content,
                                    'repeat': repeat_list
                                }
                            else:
                                trans_dict[row[0]] = {
                                    'content': '',
                                    'repeat': repeat_list
                                }
                        # show_content = str(row[0])  + ':' + result_content
                        # print(show_content)
                    content = content[end_index:len(content)]
                    num -= 1
        if search_num == 0:
            trans_dict[row[0]] = {
                'content': '无匹配关键词，无法提取'
            }
        else:
            # 对包含关系的编号进行特殊处理
            #print(trans_dict[row[0]])
            trans_dict[row[0]] = handler_contains_value(trans_dict[row[0]])

    two_time = time()
    print('数据处理使用了：',int(two_time - one_time))
    # print(json.dumps(trans_dict,ensure_ascii=False))
    handler_excel(trans_dict, outpath_dir)




if __name__ == '__main__':
    main()
