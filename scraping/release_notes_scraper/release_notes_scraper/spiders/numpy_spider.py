import scrapy


class NumpySpiderSpider(scrapy.Spider):
    name = "numpy_spider"
    allowed_domains = ["numpy.org"]
    start_urls = ["https://numpy.org"]

    def parse(self, response):
        pass
