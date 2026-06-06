
class WordProvider:
    __english_word:  str
    __engish_definition: str
    __russian_word:  str
    __russian_definition: str

    def __init__(self):
        self.url = "https://randomword.com/"
        self.__english_word = ""
        self.__engish_definition = ""
        self.__russian_word = ""
        self.__russian_definition = ""
    async def translate_to_russian(self, text):
        from googletrans import Translator
    
        translator = Translator()
        return (await translator.translate(text, dest="ru")).text.strip().lower()
    def get_random_word(self):
        import requests
        from bs4 import BeautifulSoup
        import asyncio
    
        try:
            page = requests.get(self.url)
            soup = BeautifulSoup(page.content, "html.parser")
            self.__english_word = soup.find("div", id="random_word").text.strip().lower()
            self.__engish_definition = soup.find("div", id="random_word_definition").text.strip().lower()
            self.__russian_word = asyncio.run(self.translate_to_russian(self.__english_word))
            self.__russian_definition = asyncio.run(self.translate_to_russian(self.__engish_definition))
        except requests.exceptions.RequestException as e:
            print(e)
        except Exception as e:
            print(e)

    @property
    def english_word(self):
        return self.__english_word

    @property
    def english_definition(self):
        return self.__engish_definition
    
    @property
    def russian_word(self):
        return self.__russian_word
    @property
    def russian_definition(self):
        return self.__russian_definition

class WordGame:
    provider: WordProvider
    console: GameConsoleUI

    def __init__(self, provider, console):
        self.provider = provider
        self.console = console

    def new_game(self, language = "English"):
        new_console = self.console
        provider = self.provider
        new_console.welcome_message(language)
        while True:
            provider.get_random_word()
            user_answer = new_console.ask_user(provider.english_definition, provider.russian_definition, language)
            if self.check_answer(user_answer, language):
                new_console.answer_result(True, provider.english_word, language)
            else:
                new_console.answer_result(False, provider.russian_word, language)

            Choice = new_console.ask_play_again(language)
            if Choice != "y" and Choice != "д":
                break
    def check_answer(self, user_input, language = "English"):
        if language == "English":
            return user_input.lower() == self.provider.english_word.lower()
        else:
            return user_input.lower() == self.provider.russian_word.lower()


class GameConsoleUI:

    def welcome_message(self, language = "English"):
        if language == "English":
            print("Welcome to the Word Game!")
        else:
            print("Добро пожаловать в игру слов!")
    def ask_user(self, definition, russian_definition, language = "English"):
        if language == "English":
            print(f"Definition: {definition}")
            return input("Enter a word: ")
        else:  
            print(f"Значение слова: {russian_definition}")      
            return input("Введите слово: ")
    
    def ask_play_again(self, language = "English"):
        if language == "English":
            return input("Do you want to play again? (y/n): ").lower()
        else:
            return input("Хотите сыграть еще раз? (д/н): ").lower()
    
    def answer_result(self, is_correct, correct_word = "", language = "English"):
        if language == "English":
            if is_correct:
                print("Correct!")
            else:
                print(f"Incorrect! The correct answer was {correct_word}")
        else:
            if is_correct:
                print("Правильно!")
            else:
                print(f"Неправильно! Правильный ответ был {correct_word}")

new_game = WordGame(WordProvider(), GameConsoleUI())
new_game.new_game("")