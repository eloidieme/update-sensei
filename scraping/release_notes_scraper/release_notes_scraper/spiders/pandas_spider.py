import scrapy


class PandasSpiderSpider(scrapy.Spider):
    name = "pandas_spider"
    allowed_domains = ["pandas.pydata.org"]
    start_urls = ["https://pandas.pydata.org"]

    def parse(self, response):
        pass
