import requests
from bs4 import BeautifulSoup

URL = "https://randomword.com/"

def get_random_word():

    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        english_word = soup.find("div", id="random_word").text.strip().lower()
        engish_definition = soup.find("div", id="random_word_definition").text.strip().lower()
        return {
            "english_word": english_word, 
            "engish_definition": engish_definition
            }
    except Exception as e:
        print(e)

def word_game():
    print("Welcome to the Word Game!")
    while True:
        random_word = get_random_word()
        print(f"Definition: {random_word['engish_definition']}")
        user_input = input("Enter a word: ")
        if user_input.lower() == random_word["english_word"].lower():
            print("Correct!")
        else:
            print(f"Incorrect! The correct answer was {random_word['english_word']}")

        Choice = input("Do you want to play again? (y/n): ")
        if Choice.lower() != "y":
            break

word_game()