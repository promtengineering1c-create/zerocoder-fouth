class Provider:
    __data:  list

    def __init__(self):
        self.__data = []

    @property
    def get_data(self):
        if not self.__data:
            self.scrape()
        return self.__data
    
    def scrape(self):
        import requests
        from bs4 import BeautifulSoup
        from urllib.parse import urljoin

        URL = "https://www.divan.ru/blagoveshchensk/category/svet"
        response = requests.get(URL)
        page = BeautifulSoup(response.text, 'html.parser')

        products = page.find_all('div', class_='ProductCardMain-module__4dYtKq__card')

        for product in products:
            name = product.find('div', class_='ProductName').text.strip()
            price = product.find('meta', itemprop="price").get('content').strip()
            link = urljoin(URL, product.find('a').get('href')) 
            
            self.__data.append([name, price, link])

class Saver_CSV:
    def save(self, list, filename):
        import csv
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file, delimiter=';')        
            csv_writer.writerow(['Название','Цена','Ссылка'])  
            csv_writer.writerows(list)
                
            
class Parser:
    def __init__(self, provider, saver):
        self.__provider = provider
        self.__saver = saver

    def parse(self, filename):
        self.__saver.save(self.__provider.get_data, filename)

parser = Parser(Provider(), Saver_CSV())
parser.parse('ligthpars.csv')