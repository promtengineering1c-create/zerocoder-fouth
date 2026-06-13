import scrapy
from bs4 import BeautifulSoup


class Lightpars1Spider(scrapy.Spider):
    name = "lightpars1"
    allowed_domains = ["https://divan.ru"]
    start_urls = ["https://www.divan.ru/blagoveshchensk/category/svet"]

    def parse(self, response):

        with open("lightpars1.txt", "w", encoding="utf-8") as file:
            file.write('')

        soup = BeautifulSoup(response.text, 'html.parser')
        with open("lightpars1.txt", "a", encoding="utf-8") as file:
            file.write(soup.find('div', class_='ProductCardMain-module__4dYtKq__card').prettify())
        
           
            
        # with open("lightpars1.txt", "a", encoding="utf-8") as file:
        #     # for product in response.css('div.ProductCardMain-module__4dYtKq__card'):
        #     yield file.write(str(f'-----------------------------------------------\n{response.css("div.ProductCardMain-module__4dYtKq__card").get()}'))
                
