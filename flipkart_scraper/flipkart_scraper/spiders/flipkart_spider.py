import scrapy
from ..items import FlipkartScraperItem
import sys
from flipkart_scraper import type_list

class FlipkartSpiderSpider(scrapy.Spider):
    name = 'flipkart_spider'
    allowed_domains = ['flipkart.com']
    page_number = 2
    product_type_list = type_list.product_type_list
    url_count = 1
    start_urls = [f'https://www.flipkart.com/search?q={product_type_list[0]}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1']
    
    def get_data(response):
        product_name = response.css('._2WkVRV')
        if len(product_name) == 0:
            product_name = response.css('.s1Q9rs')
        product_features = response.css('.IRpwTa')

        if len(product_features) == 0:
            product_features = response.css('._3Djpdu')

        elif len(product_features) == 0:
            product_features = response.css('._3eWWd-')
        product_price = response.css('._30jeq3')
        
        return [product_name, product_features, product_price, product_name]

    def parse(self, response):
        items = FlipkartScraperItem()
        data = FlipkartSpiderSpider.get_data(response)
        items['product_name'] = data[0].css('::text').extract() if data[0]  else None
        items['product_features'] = data[1].css('::text').extract() if data[1] else None
        items['product_price'] = data[2].css('::text').extract() if data[2] else None
        items['category'] = FlipkartSpiderSpider.product_type_list[FlipkartSpiderSpider.url_count - 1]
        
        if (items['product_name'] == None and items['product_price'] == None):
            if (FlipkartSpiderSpider.url_count == len(FlipkartSpiderSpider.product_type_list)):
                sys.exit()
            FlipkartSpiderSpider.page_number = 2
            product_type = FlipkartSpiderSpider.product_type_list[FlipkartSpiderSpider.url_count]
            FlipkartSpiderSpider.url_count += 1
            yield scrapy.Request(f'https://www.flipkart.com/search?q={product_type}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page=1', callback=self.parse)
            
        if (items['product_name'] != None):
            yield items

        index = (response.url).index('&page')
        substr = response.url[:index]
        next_page = substr + '&page=' + str(FlipkartSpiderSpider.page_number)
        FlipkartSpiderSpider.page_number += 1
        yield response.follow(next_page, callback=self.parse)