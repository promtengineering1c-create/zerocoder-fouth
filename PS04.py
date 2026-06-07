from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
    
class ConsoleUI:
    __main_menu = {}
    __second_menu = {}
    def __init__(self):
        self.__main_menu = {
            "1": "Листать параграфы",
            "2": "Перейти на связнаную страницу",
            "3": "Выйти"
        }
        self.__second_menu = {
            "1": "Листать параграфы",
            "2": "Перейти к конкретной статье"
        }

    def get_query(self, number_of_menu = 0, first_query = True):
    
        if number_of_menu == 0:
            print("Добро пожаловать в viki помощник!")
            return input("Введите первоначальный запрос: ")
        elif number_of_menu == 1:
            if first_query:
                print("Вы странице по выбранной теме! Выберите действие:")
            else:
                print("Ошибочный ввод! Нужно ввести или 1 или 2 или 3!")  

            for key, value in self.__main_menu.items():
                print(f"{key}. {value}")
        else:   
            if first_query:
                print("Вы на нужной странице! Выберите действие:")
            else:
                print("Ошибочный ввод! Нужно ввести 1 или 2!")  
            
            for key, value in self.__second_menu.items():
                print(f"{key}. {value}")
        
        return self.check_query((first_query, input("Ваш выбор: ")), number_of_menu)
        

    def check_query(self, list, number_of_menu = 1):

        first_query = list[0]
        query = list[1]

        if query == "1" or query == "2" or query == "3" and number_of_menu == 1:
            return query
        elif first_query:
            self.get_query(number_of_menu, False)
        else:
            return False   

    URL = ""

class Provider:
    URL = ""
    def __init__(self):
        self.URL = 'https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'
        self.__driver = webdriver.Chrome()

    def send_start_query(self, query):
        driver = self.__driver
        driver.get(self.URL)

        assert "Википедия\xa0— свободная энциклопедия" in driver.title

        a = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "search-toggle")))
        a.click()
        
        search_intput = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "search")))
        search_intput.send_keys(query)
        search_intput.send_keys(Keys.RETURN)

    def get_paragraphs(self):

        driver = self.__driver  

        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        for paragraph in paragraphs:
            print(paragraph.text)
            input()

    def go_to_related_page(self, number_of_menu = 1):
        driver = self.__driver

        related_links = driver.find_elements(By.CSS_SELECTOR, "a[rel='mw:WikiLink']")

        if not related_links:
            print("Нет связанных страниц.")
            self.close()
            return
        
        hatnote = random.choice(related_links)

        link = hatnote.get_attribute("href")
        driver.get(link)  

        if number_of_menu == 2:
            input("Для завершения нажмите любую клавишу...")     

    def close(self):
        self.__driver.quit()

class WikiHelper:
    def __init__(self, provider, ui):
        self.provider = provider
        self.ui = ui
        self.__startquery = ""

    def send_query(self):
        self.__startquery = self.ui.get_query()
        self.provider.send_start_query(self.__startquery)

        query = self.ui.get_query(1)
        if query == False:
            return
        if query == "1":
            self.provider.get_paragraphs()
        elif query == "2":
            self.provider.go_to_related_page() 
            query = self.ui.get_query(2) 
            print(query)
            if query == False:
                return
            if query == "1":
                self.provider.get_paragraphs()
            elif query == "2":
                self.provider.go_to_related_page(2)
        else:
            self.provider.close()


provider = Provider()
ui = ConsoleUI()
helper = WikiHelper(provider, ui)

helper.send_query()    




