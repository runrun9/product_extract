import scrapy


class OutItem(scrapy.Item):
    URL = scrapy.Field()
    product_name = scrapy.Field()
    product_summary = scrapy.Field()
    depth = scrapy.Field()
    back_urls = scrapy.Field()
    pass
