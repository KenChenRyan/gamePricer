#! python3
from html.parser import HTMLParser
#import json
#will have to modify some file names to include / or \ depending on the
#OS the user is running
import os
import requests
from bs4 import BeautifulSoup
from tkinter import filedialog as fd 

def test():
    game = "Borderlands 3"
    ggdotdealspage = "files/borderlands3GGDeals.html"
    game_to_lowest_grey_markerplace_value(game,ggdotdealspage)

def convert_games_file_to_json():
    #Function converts text file of games to include lowest grey market place value
    file_games_name = ''
    file_games = ''
    json_games_data = 'files/game_data.json'
    try:
        file_games_name = fd.askopenfilename()
        file_games = open(file_games_name,"r")
    except:
        print("You have not selected a file or it does not exist.")
    if file_games:
        if(os.path.exists(json_games_data)):
            os.remove(json_games_data)
        json_file = open(json_games_data,"a")
        json_file.write('[\n')
        beginning = True
        for line in file_games:
            line = line.strip()
            print(line)
            if not beginning:
                json_file.write(',\n')
            else:
                beginning = False
            json_file.write('{"game":"'+line+'", "price":'+game_to_lowest_grey_markerplace_value(line)+'}')
        json_file.write('\n]')
        json_file.close()


def game_to_lowest_grey_markerplace_value(game,ggdotdealshtml=''):
    #if function execution is not called in a test case
    #(if there is a lack of previously downloaded HTML file)
    #should be done with lxml instead of html.parser for speed purposes
    parser = 'html.parser'
    if (not ggdotdealshtml):
        soup = ''
        game = game.replace(" ","-")
        r = requests.get("https://gg.deals/game/"+game)
        #if page of game has been found right away
        if (not (r.raise_for_status())):
            print("Game found right away")
            gamePageFound = True
            soup = BeautifulSoup(r.text,parser)
        else:
            game = game.replace("-","+")
            r = requests.get("https://gg.deals/games/",params = {'title': game})
            gamePageFound = True
            soup = BeautifulSoup(r.text,parser)
    else:
        gamePageFound = True
        with open(ggdotdealshtml, encoding="utf8") as fp:
            soup = BeautifulSoup(fp,parser)
    #if the page of the game has been found
    if gamePageFound:
        game_card = soup.body.find('div', class_ = "main-content").find('div',id="page").find('div',id="game-card")
        price = game_card.find('div').find('div').find('div', class_='col-right').find('div').find('div',class_="header-game-prices-tabs-content").find('div').find('div').find('div',class_="best-deal").find('a').find('span').text
        while not price[0].isnumeric():
            price = price[1:]
    return price


def update_data():
    json_games_with_data = ''
    try:
        json_games_with_data = fd.askopenfilename()
        file = open(json_games_with_data)
        print("Opened "+ json_games_with_data)
        contents = json_games_with_data.read()
        print("You are currently tracking:\n" + contents)
    except:
        print("You have not selected a file or it does not exist.")

def create_table():
    json_games_with_data = ''
    try:
        json_games_with_data = fd.askopenfilename()
        file = open(json_games_with_data)
        print("Opened "+ json_games_with_data)
        contents = json_games_with_data.read()
        print("You are currently tracking:\n" + contents)
    except:
        print("You have not selected a file or it does not exist.")
    #I don't know if I will use the code below
    with open(json_games_with_data,"r") as file:
        print('reading file')
    print("Done")

def main():
    userRunning = True
    while (userRunning):
        print("\n----------------------------------------------------------------------------------------\nWhat would you like to do?\n")
        print("1. Convert text file of games to include lowest grey market place value.\n2. See the lowest grey marketplace value of a game")
        print("3. Create table\n4. Quit program\n5. Test routine")
        user_input = input()
        if user_input == "1":
            convert_games_file_to_json()
        if user_input == "2":
            game = input("What's the name of the game?\n")
            game_to_lowest_grey_markerplace_value(game)
        if user_input == "3":
            create_table()
        if user_input == "4":
            userRunning = False
        if user_input == "5":
            test()    

if __name__ == "__main__":
    main()
