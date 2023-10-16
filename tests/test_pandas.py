import unittest
import pandas as pd

class MyTestCase(unittest.TestCase):
    fake_bidding = {'id': '0000044d89c6467e8a0db5ca22eabf18', 'hash': '70633ece6239dec6023166b75fb5e249',
                    'source_id': 4241,
                    'type': 0, 'category': 0, 'title': '二氧化碳（液态）采购公告', 'public_time': 1694620800,
                    'industry': 0,
                    'province_id': 32, 'city_id': 0, 'source_url': 'http://www.shzbpt.com:80/wxzbgg/30605.jhtml',
                    'section': '公告信息',
                    'snapshot': '<div class="Content" > \n  \n  \n  <p ><strong>新疆神火煤电有限公司 </strong>\xa0<span>\xa0</span><span class="bookmark" contenteditable="false" editype="text" name="xmxx_xmmc"  value="项目信息.项目名称">二氧化碳（液态）</span>\xa0<span>\xa0</span><span class="bookmark" contenteditable="false" editype="text" name="xmxx_zbbh"  value="项目信息.招标编号">XJSH-20230913-016</span>\xa0<strong>采购公告</strong></p> \n  <p>\xa0 新疆神火煤电有限公司关于\xa0<span>\xa0</span><span class="bookmark" contenteditable="false" editype="text" name="xmxx_xmmc"  value="项目信息.项目名称">二氧化碳（液态）</span>\xa0<span>\xa0</span><span class="bookmark" contenteditable="false" editype="text" name="xmxx_zbbh"  value="项目信息.招标编号">XJSH-20230913-016</span>\xa0 ，网上报价公告如下：\xa0</p> \n  <p>1、网上报价招标物资明细如下：</p> \n  <p><span>\xa0</span></p> \n  <p >•二氧化碳（液态）</p> \n  <table border="1" cellpadding="0" cellspacing="0" width="90%"> \n   <thead> \n    <tr> \n    </tr> \n    <tr> \n     <th >物料编码</th> \n     <th >物料名称</th> \n     <th >规格</th> \n     <th >型号</th> \n     <th >采购数量</th> \n     <th >计量单位</th> \n     <th >备注</th> \n     <th >成交数量</th> \n    </tr> \n   </thead> \n   <tbody> \n    <tr> \n     <td>2907020020002</td> \n     <td>二氧化碳</td> \n     <td>纯度≥99.9%</td> \n     <td>液态</td> \n     <td>6000</td> \n     <td>千克</td> \n     <td>新疆煤电电力库存组织(08月)新疆煤电电力公司_运行分厂_运行二班6000. ;</td> \n     <td>\xa0</td> \n    </tr> \n   </tbody> \n  </table> \n  <p><br> \xa0</p> \n  <p>\xa0</p> \n  <p>2、报名截止时间：<span>\xa0</span><span class="bookmark" contenteditable="false" editype="text" name="xmxx_bmjzsj"  value="项目信息.报名截止时间">2023年09月18日 17:30:00</span>\xa0\xa0 ；报价截止时间：\xa0<span>\xa0</span><span class="bookmark" contenteditable="false" editype="text" name="xmxx_kbsj"  value="项目信息.开标时间">2023年09月18日 17:30:00</span>\xa0</p> \n  <p>3、电子采购平台操作手册详见“门户网站-文件下载”</p> \n  <p>4、联系方式</p> \n  <p>业务联系电话 ：<span>\xa0</span><span class="bookmark" contenteditable="false" editype="text" name="xmxx_lxdh"  value="项目信息.联系电话">0994-6852206</span>\xa0</p> \n  <p>联系人：供应部</p> \n  <p>注意：平台操作事宜联系：0370-6062618</p> \n  <p ><span>\xa0</span><span class="bookmark" contenteditable="false" editype="text" name="xmxx_nowTimeStr"  value="项目信息.当前日期">二○二三年九月十三日</span>\xa0</p>  \n \n\n<br>\n\t\t</div>',
                    'extend': '', 'archives': '[]', 'version': 0, 'create_time': 1694662549, 'id2': 95509805}

    def test_re_parse(self):
        df = pd.DataFrame(self.fake_bidding, index=["public_time"])
        print(df.to_dict(orient='records', index=True))

        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
