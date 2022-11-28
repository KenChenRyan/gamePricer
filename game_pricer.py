#! python3
from html.parser import HTMLParser
import json
#will have to modify some file names to include / or \ depending on the
#OS the user is running
import os
import requests
from bs4 import BeautifulSoup
from tkinter import filedialog as fd
from tabulate import tabulate

def test():
    test_case = 1
    match test_case:
        case 0:
            print("Testing Borderlands 3")
            game = "Borderlands 3"
            ggdotdealspage = "files/borderlands3GGDeals.html"
            if not os.path.exists(ggdotdealspage):
                print(game_to_lowest_grey_markerplace_value(game))
            else:
                print(game_to_lowest_grey_markerplace_value(game,ggdotdealspage))
        case 1:
            #game = "Donuts'n'justice"
            game = "Borderlands 4"
            print("Looking for "+game)
            print(game_to_lowest_grey_markerplace_value(game))

def convert_games_file_to_json():
    #Function converts text file of games to include lowest grey market place value
    file_games_name = ''
    file_games = ''
    json_games_data = 'files/game_data.json'
    file_games_ext = ''
    try:
        file_games_name = fd.askopenfilename()
        file_games_ext = os.path.splitext(file_games_name)[1]
        file_games = open(file_games_name,"r")
        print
    except:
        print("You have not selected a file or it does not exist.")
    if file_games:
        if(os.path.exists(json_games_data)):
            os.remove(json_games_data)
        json_file = open(json_games_data,"a")
        json_file.write('{\n"games": [\n')
        beginning = True
        print(file_games_ext)
        if(file_games_ext == '.txt'):
            for line in file_games:
                line = line.strip()
                print(line)
                if not beginning:
                    json_file.write(',\n')
                else:
                    beginning = False
                json_file.write('{"game":"'+line+'", "price":'+game_to_lowest_grey_markerplace_value(line)+'}')
        else:
            print("Your file format is not recognized")
        json_file.write('\n]\n}')
        json_file.close()


def game_to_lowest_grey_markerplace_value(game,ggdotdealshtml=''):
    #first if statement execution is not called in a test case
    #(where the HTML page is provided before hand)
    
    #should be done with lxml instead of html.parser for speed purposes
    parser = 'html.parser'
    if (not ggdotdealshtml):
        price = ''
        soup = ''
        #boolean for if the game will not be found in the search page
        originalGameString = game
        game = game.replace(" ","-")
        r = requests.get("https://gg.deals/game/"+game)
        #if page of game has not been found right away
        if (r.status_code == 404):
            gamePageFound = False
            game = originalGameString.replace(" ","+")
            r = requests.get("https://gg.deals/games/",params = {'title': game})
            soup = BeautifulSoup(r.text,parser)
            listOfGames = soup.body.find('div', class_='main-content').find('div', id ='page').find('div', class_='games-box').find('div', class_='game-section').find('div',class_='col-left').find('div').find('div').find_all('div', class_='hoverable-box')
            emptyList = False
            for gameInList in listOfGames:
                if 'empty' in gameInList['class']:
                    emptyList = True
                    print("The game has not been found")
                    break
                else:
                    #gamePageFound = True
                    listingName = gameInList.find('div',class_='game-info-wrapper').find('div').find('div').text
                    #make them both all lower case
                    if listingName.lower() == originalGameString.lower():
                        price = gameInList.find('div',class_='game-info-wrapper').find('div', class_='price-wrap').find('div', class_="shop-price-keyshops").find('div').text
                        if price.strip() == 'Unavailable':
                            pass
                        else:
                            while not price[0].isnumeric():
                                price = price[1:]
            #if the games that have been found in the list do not match the given game then have
            #the user confirm if there is a matching game
            if not emptyList and  price == '':
                for gameInList in listOfGames:
                    listingName = gameInList.find('div',class_='game-info-wrapper').find('div').find('div').text
                    print("Is your game "+listingName+"?(Y/N)")
                    answer = (input()).lower()
                    if (answer == 'y'):
                        price = gameInList.find('div',class_='game-info-wrapper').find('div', class_='price-wrap').find('div', class_="shop-price-keyshops").find('div').text
                        if price.strip() == 'Unavailable':
                            pass
                        else:
                            while not price[0].isnumeric():
                                price = price[1:]
                        break
                    else:
                        continue
                if price == '':
                    print("The game in question("+originalGameString+")could not be found")  
        else:
            print("Game found right away")
            gamePageFound = True
            soup = BeautifulSoup(r.text,parser)
    else:
        with open(ggdotdealshtml, encoding="utf8") as fp:
            soup = BeautifulSoup(fp,parser)
    #if the page of the game has been found
    if gamePageFound and price == '':
        game_card = soup.body.find('div', class_ = "main-content").find('div',id="page").find('div',id="game-card")
        price = game_card.find('div').find('div').find('div', class_='col-right').find('div').find('div',class_="header-game-prices-tabs-content").find('div').find('div').find('div',class_="best-deal").find('a').find('span').text
        if price == 'Unavailable':
            pass
        else:
            while not price[0].isnumeric():
                price = price[1:]
    return price

def organize_json(is_ascending, json_object):
    return_json = sorted(json_object['games'],key = lambda game: game["price"],reverse = not is_ascending)
    return return_json

def create_table():
    json_games_with_data = ''
    json_var = ''
    try:
        json_games_with_data = fd.askopenfilename()
    except:
        print("You have not selected a file or it does not exist.")
    with open(json_games_with_data,"r", encoding="utf-8") as file:
        json_var = json.loads(file.read())
    if json_var:
        print("Do you want to order by (1)ascending, (2)descending, or (3)none?")
        order = input()
        if order == '1' or order == '2':
            order = int(order)
        else:
            order = 3
        file_table_string = "files/table.txt"
        if os.path.exists(file_table_string):
            os.remove(file_table_string)
        file_table = open(file_table_string,"w", encoding="utf-8")
        if order == 1:
            json_var['games'] = organize_json(True,json_var)
        elif order == 2:
            json_var['games'] = organize_json(False,json_var)
        print("Do you want to include game prices? (y/n)")
        with_prices = input()
        if with_prices.lower() == 'y':
            file_table.write(tabulate(json_var['games'], headers = 'keys' ,tablefmt = 'fancy_grid'))
        else:
            temp_list = list()
            for game in json_var['games']:
                temp_list.append([game['game']])
            print(temp_list)
            file_table.write(tabulate(temp_list, headers = ['Games'],tablefmt = 'fancy_grid'))

        file_table.close()

def main():
    userRunning = True
    while (userRunning):
        print("\n---------------------------------------\nWhat would you like to do?\n")
        print("1. Convert text file of games to include lowest grey market place value.\n2. See the lowest grey marketplace value of a game")
        print("3. Create table\n4. Quit program\n5. Test routine")
        user_input = int(input())
        if user_input == 1:
            print("Txt files will be assumed that games are seperated by newlines.")
            convert_games_file_to_json()
        if user_input == 2:
            game = input("What's the name of the game?\n")
            print(game_to_lowest_grey_markerplace_value(game))
        if user_input == 3:
            create_table()
        if user_input == 4:
            userRunning = False
        if user_input == 5:
            test()    

if __name__ == "__main__":
    main()