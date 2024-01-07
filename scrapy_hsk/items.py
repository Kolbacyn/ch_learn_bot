import scrapy


class WordItem(scrapy.Item):
    """"""
    word = scrapy.Field()
    transcription = scrapy.Field()
    rus_translation = scrapy.Field()
    level = scrapy.Field()
