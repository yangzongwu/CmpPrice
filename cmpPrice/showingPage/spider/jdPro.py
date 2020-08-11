import requests
from lxml import etree
import json

def jdSearch(input='python',n=10):
    url='https://search.jd.com/Search?keyword='+str(input)+'&psort=3&click=0'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    try:
        page_text = requests.get(url, headers=headers).text
        tree = etree.HTML(page_text)
        li_list = tree.xpath('//*[@id="J_goodsList"]/ul/li')
    except:
        li_list=[]
    jd_result=[]
    for li in li_list[:n]:
        try:
            good_url = 'https:' + li.xpath('./div/div/a/@href|./div/div/div[2]/div/div/a/@href')[0]
            good_name = li.xpath('./div/div[4]/a/em/text()|./div/div/div[2]/div/div[4]/a/em/text()')[0].strip()
            good_pic = 'https:' + li.xpath('./div/div[1]/a/img/@src|./div/div/div[2]/div/div[1]/a/img/@src')[0]
            good_price_unit = li.xpath('./div/div[3]/strong/em/text()|./div/div/div[2]/div/div[3]/strong/em/text()')[0]
            good_price = li.xpath('./div/div[3]/strong/i/text()|./div/div/div[2]/div/div[3]/strong/i/text()')[0]
            id = good_url[:-5].split('/')[-1]
        except:
            try:
                good_url = 'https:' + li.xpath('./div/div/a/@href|./div/div/div[2]/div/div/a/@href')[0]
                good_name = li.xpath('./div/div[3]/a/em/text()|./div/div/div[2]/div/div[3]/a/em/text()')[0].strip()
                good_pic = 'https:' + li.xpath('./div/div[1]/a/img/@src|./div/div/div[2]/div/div[1]/a/img/@src')[0]
                good_price_unit = \
                li.xpath('./div/div[2]/strong/em/text()|./div/div/div[2]/div/div[2]/strong/em/text()')[0]
                good_price = li.xpath('./div/div[2]/strong/i/text()|./div/div/div[2]/div/div[2]/strong/i/text()')[0]
                id = good_url[:-5].split('/')[-1]
            except:
                continue

        try:
            new_url = good_url
            detail_page = requests.get(new_url, headers=headers).text
            tree = etree.HTML(detail_page)
            good_ISBN = tree.xpath('//*[@id="parameter2"]/li[2]/text()')[0]
        except:
            good_ISBN=None
        if good_ISBN and good_ISBN[0:4] != 'ISBN':
            try:
                good_ISBN = tree.xpath('//*[@id="parameter2"]/li[3]/text()')[0]
            except:
                good_ISBN = None

        if good_ISBN and good_ISBN[0:4] == 'ISBN':
            good_ISBN = good_ISBN[5:]
        else:
            good_ISBN = None

        new_url='https://club.jd.com/comment/productPageComments.action?productId='+id+'&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
        try:
            detail_page = requests.get(new_url, headers=headers).text
            comment_dic = json.loads(detail_page)
            good_num_comment = comment_dic['productCommentSummary']['commentCountStr']
            good_comment_rate = comment_dic['productCommentSummary']['goodRate']
            good_comment_rate = str(round(good_comment_rate * 100, 1)) + '%'
        except:
            good_comment_rate=None
            good_num_comment=None
        res={
            'good_ISBN': good_ISBN,
            'good_name':good_name,
            'good_pic':good_pic,
            'good_price':good_price,
            'good_price_unit':good_price_unit,
            'good_from':'JD',
            'good_url':good_url,
            'good_comment_rate':good_comment_rate,
            'good_num_comment':good_num_comment,
        }
        jd_result.append(res)
    return jd_result
