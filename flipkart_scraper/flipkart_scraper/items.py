import scrapy


class FlipkartScraperItem(scrapy.Item):
    product_name = scrapy.Field()
    product_features = scrapy.Field()
    product_price = scrapy.Field()
    category = scrapy.Field()
