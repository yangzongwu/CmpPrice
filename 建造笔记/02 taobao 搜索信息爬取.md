# 输入
* input:需要搜索的关键字
* n:需要罗列JD网站搜索结果排名靠前的个数
# 输出
* 抓取的是一长串不规则的字符串，里面包含json数据
* 需要对字符串进行整理，规范，提取出json,```strs.strip().split('\n')[0][16:-1]```
* 返回一个长度为n的列表，列表包含字典，字典包含商品的信息
# 注意
* 淘宝反爬机制比较多
* 抓取的文件都是动态加载的，尝试用selenium在登录滑块验证时一直无法通过
* 如下抓取的弊端时一段时间只能少量抓取，否则会被禁止掉
* 可以修改随机的cookie，headers，ip
```python
import requests
from lxml import etree
import json
import time

def tbSearch(input='python',n=10):
    cookie='thw=cn; UM_distinctid=17226824d596e0-0575a27ff0dfc5-d373666-100200-17226824d5a672; cna=B6scF9WLgnACAXANP9/aEdRn; _m_h5_tk=ce77126788aaaaf8c8f5f1d0e5357a30_1596783335113; _m_h5_tk_enc=428da61375cb4c464acdbc54c144dca3; sgcookie=EaRK2eZCRrSldICbEfYxl; uc3=lg2=V32FPkk%2Fw0dUvg%3D%3D&vt3=F8dBxG2jilDlMHlh1Nw%3D&nk2=GgoRmsJ6omland7Uu0E%3D&id2=UoWzW98vT5ar; lgc=yangzongwu1987; uc4=id4=0%40UO2kHgAg6TsN%2BKWISlPbWO6j3ug%3D&nk4=0%40GIauBIP1iExONbAq4CWbxfFxW35jq3iNHA%3D%3D; tracknick=yangzongwu1987; _cc_=V32FPkk%2Fhw%3D%3D; enc=1JhRCSWddtrcbgjSin4A4aEnQ1XzfBWYr5F6oHdh6JR7OYOL0jgtw9CZvimv9YfphJrN3W%2FMzAfhghlJ6iGK2g%3D%3D; mt=ci=9_1; hng=CN%7Czh-CN%7CCNY%7C156; v=0; cookie2=140665a3d151b870531e63bc455ce885; uc1=cookie14=UoTV6hxPRuJMwA%3D%3D; t=266326f334fa6d8c6fe398635c1ba24f; _tb_token_=eb3b5e37e4ebe; tfstk=clNCBFADWHxC2-ByTy_ZY5c8r2l5ZP8jP9i3RRl0uCGRhvaCiDRqcP-7E3dtHV1..; l=eBOSyk2qOrNIYM7kBOfZnurza77TpIRVguPzaNbMiOCPOV1p5VCPWZopNkY9CnGVnsgvR35e4jETB08UhPatCc1l1fc2cMpTdd8h.; isg=BLu7RzuKYO5Qt13gIkDsL41PSp8lEM8SOkx8ga14y7rRDNjuNeGGYO4GJqxCLCcK'
    url = 'https://s.taobao.com/search?q='+input+'&ie=utf8&sort=sale-desc'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36','cookie':cookie}
    page_text = requests.get(url,headers=headers).text
    tree = etree.HTML(page_text)
    good_json=tree.xpath('/html/head/script[8]//text()')[0].strip()
    good_json=good_json.split('\n')[0][16:-1]
    good_dic = json.loads(good_json)
    good_list=good_dic['mods']['itemlist']['data']['auctions']
    taobao_result=[]
    for good in good_list[:n]:
        try:
            time.sleep(1)
            good_name = good['raw_title']
            good_pic = good['pic_url'] + '_.webp'
            good_url = 'https:' + good['detail_url']
            good_price = good['view_price']
            comment_count = good['comment_count']
            good_comment_rate = (good['shopcard']['description'][0] + good['shopcard']['service'][0] +
                                 good['shopcard']['delivery'][0]) / 3
            detail_page_text = requests.get(good_url, headers=headers).text
            detail_page_tree = etree.HTML(detail_page_text)
            try:
                good_ISBN = detail_page_tree.xpath('//*[@id="J_AttrUL"]/li[2]/text()')[0]
            except:
                good_ISBN = None
            if good_ISBN and good_ISBN[0:4] != 'ISBN':
                try:
                    good_ISBN = detail_page_tree.xpath('//*[@id="J_AttrUL"]/li[3]/text()')[0]
                except:
                    good_ISBN = None
            if good_ISBN[0:4] == 'ISBN':
                good_ISBN = good_ISBN[8:]
            else:
                good_ISBN = None
            res = {
                'good_ISBN': good_ISBN,
                'good_name': good_name,
                'good_pic': good_pic,
                'good_price': good_price,
                'good_price_unit': good_price,
                'good_from': 'Taobao',
                'good_url': good_url,
                'good_comment_rate': good_comment_rate,
                'good_num_comment': comment_count,
            }
            taobao_result.append(res)
        except:
            continue
```