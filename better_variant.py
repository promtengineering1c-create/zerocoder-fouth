import requests
from bs4 import BeautifulSoup

class WordGame:
    def __init__(self):
        self.url = "https://randomword.com/"

    def get_random_word(self):
        try:
            page = requests.get(self.url)
            soup = BeautifulSoup(page.content, "html.parser")
            english_word = soup.find("div", id="random_word").text.strip().lower()
            engish_definition = soup.find("div", id="random_word_definition").text.strip().lower()
            return {
                "english_word": english_word, 
                "engish_definition": engish_definition
                }
        except Exception as e:
            print(e)

    def word_game(self):
        print("Welcome to the Word Game!")
        while True:
            random_word = self.get_random_word()
            print(f"Definition: {random_word['engish_definition']}")
            user_input = input("Enter a word: ")
            if user_input.lower() == random_word["english_word"].lower():
                print("Correct!")
            else:
                print(f"Incorrect! The correct answer was {random_word['english_word']}")

            Choice = input("Do you want to play again? (y/n): ")
            if Choice.lower() != "y":
                break

next_game = WordGame()
next_game.word_game()
