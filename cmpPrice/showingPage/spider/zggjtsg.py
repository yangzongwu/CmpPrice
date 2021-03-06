from selenium import webdriver
from time import sleep
from lxml import etree
from selenium.webdriver.chrome.options import Options


def bookdetails(ISBN):
    try:
        option = Options()
        option.add_argument('--headless')
        bro = webdriver.Chrome(executable_path='./chromedriver.exe', options=option)
        url = 'http://opac.nlc.cn/F/N5QRKMT1IE9P17JM85Y58IP3CT4P5T5YQPA2KC1ERU5DG5YS5E-36940?find_code=ISB&request=&local_base=NLC01&func=find-b'
        bro.get(url)
        btn = bro.find_element_by_xpath('//*[@id="all_base"]')
        btn.click()
        btn = bro.find_element_by_xpath('//*[@id="find_code"]/option[16]')
        btn.click()
        isbn = bro.find_element_by_id('reqterm')
        isbn.send_keys(ISBN)
        btn = bro.find_element_by_xpath('//*[@id="indexpage"]/form/div[2]/input')
        btn.click()
        sleep(0.1)
        page_text = bro.page_source
        tree = etree.HTML(page_text)
        name_author = tree.xpath('//*[@id="td"]/tbody/tr[4]/td[2]/a/text()')[0]
        [name, author] = name_author.split('/')
        tmp = tree.xpath('//*[@id="td"]/tbody/tr[5]/td[1]//text()')[0].strip()
        if tmp == '出版项':
            publisher = tree.xpath('//*[@id="td"]/tbody/tr[5]/td[2]/a/text()')[0]
        else:
            publisher = tree.xpath('//*[@id="td"]/tbody/tr[6]/td[2]/a/text()')[0]
        abstract = tree.xpath('//*[@id="td"]/tbody/tr[10]/td[2]/text()')[0]
        name, author, publisher, abstract = name.strip(), author.strip(), publisher.strip(), abstract.strip()
        if '=' in name:
            name = name.split('=')[0]
        bro.quit()
    except:
        [name, author, publisher, abstract] = [None, None, None, None]
    return [name, author, publisher, abstract]
