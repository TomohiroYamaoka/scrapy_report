# -*- coding: utf-8 -*-
import scrapy
from amazon_project.items import AmazonItem

class AmazonProductSpider(scrapy.Spider):
  name = "amazon"
  allowed_domains = ["amazon.com"]
  start_urls=["https://www.amazon.co.jp/%E3%80%90Amazon-co-jp-Business%E4%BB%98%E3%81%8D%E3%80%91Dell-%E3%83%A2%E3%83%90%E3%82%A4%E3%83%AB%E3%83%8E%E3%83%BC%E3%83%88%E3%83%91%E3%82%BD%E3%82%B3%E3%83%B3-i5-1035G1-MI554A-ANHBC/dp/B08C9WJ8B1/ref=sr_1_11?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=amazon&qid=1606802040&sr=8-11#customerReviews"]
  
  #Use working product URL below
  def parse(self, response):
        item_name = response.css(".product-title>h1.a-size-large>a.a-link-normal::text").get()
        for all_date in response.css(".review>.a-row>.celwidget"):
            yield AmazonItem(
                name=all_date.css("span.a-profile-name::text").get(),
                title = all_date.css(".review-title>span::text").get(),
                star = int(all_date.css(".a-icon-star>span::text").get()[-3:-2]),
                date = all_date.css(".review-date::text").get()[0:10],
                review = ','.join(all_date.css(".review-text-content>span::text").getall()),
            )
        next_page_link = response.css("li.a-last>a::attr(href)").extract_first()
        
        if next_page_link is None:
            return

        next_page_link = response.urljoin(next_page_link)
        yield scrapy.Request(next_page_link, callback=self.parse)

