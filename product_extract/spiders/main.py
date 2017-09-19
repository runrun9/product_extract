# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.selector import Selector
from product_extract.items import OutItem


# 入力データのクラス
class Input_data:
    def __init__(self, top_url, product_url, product_xpath, product_summary_xpath):
        self.top_url = top_url
        self.product_url = product_url
        self.product_xpath = product_xpath
        self.product_summary_xpath = product_summary_xpath

# urlの末尾がskip_listに含まれるものである場合Falseを返す
def url_check(skip_list, url):
    for x in skip_list:
        x = ".*" + x + "$"
        if re.match(x, url):
            return True
    return False

# spider
class MainSpider(scrapy.Spider):
    name = 'main'

    skip_list = ["pdf", "png", "zip", "jpg", "xlsx", "xls"]

    # print("製品カタログTOPのURL")
    # top_url = input(">> ")
    #
    # print("製品タイトルのxpath")
    # product_xpath = input(">> ")
    #
    # print("製品説明のxpath")
    # product_summary_xpath = input(">> ")

    top_url = "http://www.lion.co.jp/ja/products/"
    product_xpath = "/html/body/div[1]/article/div[2]/div[1]/section/h1"
    product_summary_xpath = "/html/body/div[1]/article/div[2]/div[1]/section/div[1]/div/p"

    product_xpath += "/text()"
    product_summary_xpath += "/text()"

    input_data = Input_data(top_url, None, product_xpath, product_summary_xpath)

    start_urls = []
    allowed_domains = []
    try:
        start_urls.append(input_data.top_url)
        allowed_domains.append(start_urls[0].split("/")[2])
        print("url ok")
    except:
        print("url errs")


    def parse(self, response):
        if Selector(response).xpath(self.input_data.product_xpath):
            item = OutItem()
            item["URL"] = response.url
            item["product_name"] = Selector(response).xpath(self.input_data.product_xpath).extract()[0]
            try:
                item["product_summary"] = Selector(response).xpath(self.input_data.product_summary_xpath).extract()[0]
            except:
                print("no summary")

            yield item

        else:
            next_page = Selector(response).xpath("//a/@href").extract()
            if next_page is not None:
                for url in next_page:
                    if not url_check(MainSpider.skip_list, url): # 末尾がpdfであるurlをはじく
                        url = response.urljoin(url)
                        yield scrapy.Request(url, callback=self.parse)
