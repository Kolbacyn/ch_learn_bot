BOT_NAME = "scrapy_hsk"

SPIDER_MODULES = ["scrapy_hsk.spiders"]
NEWSPIDER_MODULE = "scrapy_hsk.spiders"

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   "scrapy_hsk.pipelines.WordToDBPipeline": 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
