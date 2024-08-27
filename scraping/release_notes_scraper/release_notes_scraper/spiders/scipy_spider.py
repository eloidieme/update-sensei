import scrapy


class ScipySpiderSpider(scrapy.Spider):
    name = "scipy_spider"
    allowed_domains = ["scipy.org"]
    start_urls = ["https://scipy.org"]

    def parse(self, response):
        pass
