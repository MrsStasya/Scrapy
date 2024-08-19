# Category //div[@class="zb0Hu atI7H"]/a/@href
# Название img будет по первой строке после /
# img //*div[@class = "JM3zT"]/a/@href
# 

import scrapy
import os

class UnsplashImageItem(scrapy.Item):
  img_url = scrapy.Field()
  img_folder = scrapy.Field()
  img_name = scrapy.Field()
  img_category = scrapy.Field()
 
class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    start_urls = ["https://unsplash.com"]

 # Извлекаем изображение
    def parse(self, response):
        for image_page in response.xpath('//div[@class = "JM3zT"]/a/@href').extract():
            yield scrapy.Request(response.urljoin(image_page), self.parse_image_page)
    
    
    def parse_image_page(self, response):
        full_image_url = response.xpath('//*[contains(@class, "fullImageLink")]/a/@href').extract_first()
        if full_image_url:
            yield scrapy.Request(response.urljoin(full_image_url), self.save_image)
            img_name = response.url.split('/')[-1]
            img_url = full_image_url
            img_category = response.xpath('//div[@class="zb0Hu atI7H"]/a/text()').extract()
            scraped_data = zip(img_name,img_url, img_category)
            for item in scraped_data:
                data = {
                'Name': item[0],
                'URL': item[1],
                'Category':item[2]
                }
            yield data
  
    
    # filename - получаем имя файла изображения. Функция with open - сохраняем изображение в папку images
    def save_image(self, response):
        filename = response.url.split('/')[-1]
        with open(f'images/{filename}', 'wb') as f:
            f.write(response.body)        

   