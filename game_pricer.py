#! python3
from html.parser import HTMLParser
from pprint import pprint
import json
import os
import requests
from tkinter import filedialog as fd 

#Functionality of this program includes:
#Feeding it a name of a game (string) and getting back the grey market place value
#Feeding it a file of names of games and getting back the grey market place value in another file.
#Have the file be in a speicfic format and be able to order by lowest to higest and vice versa
file_games = ''
file_tg = 'files/tracking_games.json'
file_g2a = 'files/g2a_data.json'
have_games_file = 'files/have_games.txt'
sell_games_file = 'files/sell_games.txt'

class GGdotDealsHTMLParser(HTMLParser):
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        return super().handle_starttag(tag, attrs)

def list_tracked_games():
    #Program opens file that keeps track of what games are being track and file with data of games
    file_games = ''
    try:
        file_games = fd.askopenfilename()
        file = open(file_games)
        print("Opened "+ file_games)
        contents = file.read()
        print("You are currently tracking:\n" + contents)
    except:
        print("You have not selected a file or it does not exist.")

def game_to_lowest_grey_markerplace_value(game):
    game = game.replace(" ","-")
    r = requests.get("https://gg.deals/game/"+game)
    if (r.raise_for_status()):
        game = game.replace("-","+")
        r = requests.get("https://gg.deals/games/",params = {'title': game})
    #once game page has been found
    print(r.text)
        


def update_data():
    print("data")

def create_chart():
    with open(have_games_file,r) as haveGF:
        print('reading file')
    print("Done")

def main():
    userRunning = True
    while (userRunning):
         print("\n----------------------------------------------------------------------------------------\nWhat would you like to do?\n")
         print("1. Convert text file of games to include lowest grey market place value.\n2. See the lowest grey marketplace value of a game")
         print("3. Create chart\n4. Quit program")
         user_input = input()
         if user_input == "1":
            list_tracked_games()
         if user_input == "2":
            game = input("What's the name of the game?\n")
            game_to_lowest_grey_markerplace_value(game)
         if user_input == "3":
            pass;
            create_chart()
         if user_input == "4":
            userRunning = False

if __name__ == "__main__":
    main()
