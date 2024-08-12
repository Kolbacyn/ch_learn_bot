import scrapy


class WordItem(scrapy.Item):
    """WordItem class for storing word data in the database."""
    word = scrapy.Field()
    transcription = scrapy.Field()
    rus_translation = scrapy.Field()
    level = scrapy.Field()
