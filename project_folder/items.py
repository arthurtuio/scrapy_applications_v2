# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class ProjectFolderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class DemoDownloaderItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()

    def file_path(self, request, response=None, info=None):
        file_name: str = request.url.split("/")[-1]
        return file_name
