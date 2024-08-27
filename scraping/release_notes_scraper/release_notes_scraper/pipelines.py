# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MarkdownExportPipeline:
    def open_spider(self, spider):
        self.file = open(f"{spider.name}_deprecations.md", "w")
        self.file.write(f"# {spider.name.split('_')[0].capitalize()} Deprecations\n\n")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.file.write(f"## {item['version']}\n\n")
        for dep in item['deprecations']:
            self.file.write(f"- {dep}\n")
        self.file.write("\n")
        return item
