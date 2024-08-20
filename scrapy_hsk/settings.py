BOT_NAME = "scrapy_hsk"

SPIDER_MODULES = ["scrapy_hsk.spiders"]
NEWSPIDER_MODULE = "scrapy_hsk.spiders"

ROBOTSTXT_OBEY = True

# ITEM_PIPELINES = {
#    "scrapy_hsk.pipelines.WordToDBPipeline": 300,
#    "scrapy_hsk.pipelines.SentencePipepine": 400,
# }

SPIDER_MIDDLEWARES = {
    "scrapy_hsk.middlewares.ScrapyHskSpiderMiddleware": 544,
}

# REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

FEED_EXPORT_ENCODING = "utf-8"

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
