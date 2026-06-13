import scrapy
from bs4 import BeautifulSoup


class Lightpars1Spider(scrapy.Spider):
    name = "lightpars1"
    allowed_domains = ["https://divan.ru"]
    start_urls = ["https://www.divan.ru/blagoveshchensk/category/svet"]

    def parse(self, response):

        # with open("lightpars1.txt", "w", encoding="utf-8") as file:
        #     file.write('')

        # soup = BeautifulSoup(response.text, 'html.parser')
        # with open("lightpars1.txt", "a", encoding="utf-8") as file:
        #     file.write(soup.find('div', class_='ProductCardMain-module__4dYtKq__card').prettify())
        
           
        products = response.css('div.ProductCardMain-module__4dYtKq__card') 
        for product in products:   
            yield {
                'name': product.css('div.ProductName::text').get(),
                'price': product.css('meta[itemprop="price"]::attr(content)').get(),
                'link': response.urljoin(product.css("a").attrib["href"]),
                }    
