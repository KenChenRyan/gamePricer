#! python3
from sys import platform
import json
import os
import requests
import urllib.parse
from bs4 import BeautifulSoup
from tkinter import filedialog as fd
from tabulate import tabulate
from html.parser import HTMLParser

def main():
    userRunning = True
    while (userRunning):
        print("\n---------------------------------------\nWhat would you like to do?\n")
        print("1. Convert text file of games to include lowest grey market place value.\n2. Create Table")
        print("3. See the lowest grey marketplace value of a game\n4. Quit program\n5. Test routine")
        user_input = input()
        if user_input.isnumeric():
            user_input = int(user_input)
        if user_input == 1:
            print("Txt files will be assumed that games are seperated by newlines.")
            convert_games_file_to_json()
        elif user_input == 3:
            game = input("What's the name of the game?\n")
            print(game_to_lowest_grey_markerplace_value(game))
        elif user_input == 2:
            create_table()
        elif user_input == 4:
            userRunning = False
        elif user_input == 5:
            test()
        else:
            print("Try again")

#Function converts text file of a list of  games to include lowest grey market place value
def convert_games_file_to_json(file_games_name = ''):
    file_games = ''
    #check for OS of user (regarding directory style ("\" or "/"))
    windows = ''
    if platform == 'win32' or platform == 'cygwin':
        json_games_data = 'files\game_data.json' 
        windows = True
    else:
        json_games_data = 'files/game_data.json'
        windows = False
    #try to get a file from the user
    file_selected = True
    #if the func hasn't been given a file name
    if not file_games_name:
        try:
            file_games_name = fd.askopenfilename()
        except:
            print("The popup failed.")
        if not file_games_name:
            print('Please insert your .txt games list file in the "files" folder.')
            print("Please type in your files name. (Assuming it's in the files folder)")
            file_games_name = input()
            if not file_games_name:
                file_selected = False
            else:
                if windows:
                    file_games_name = "files\\"+file_games_name
                else:
                    file_games_name = "files/"+file_games_name
    #if the user has given a file name
    if file_selected:
        if(os.path.splitext(file_games_name)[1] == '.txt'):
            #if there is a character that differentiates between the games (either EOL, comma, or a line)
            print("Are your games seperated by empty lines?")
            ans = input()
            seperatedByLine = False
            if ans.lower() == "yes" or ans.lower() == "y":
                seperatedByLine = True
            try:
                #avoid setting parameter encoding='utf-8' b/c it will affect performence
                #and omit bugs when reading json file into json variable in create_table()
                with open(file_games_name,'r') as file_games:
                    if(os.path.exists(json_games_data)):
                        os.remove(json_games_data)
                    json_file = open(json_games_data,"a")
                    json_file.write('{\n"games": [\n')
                    beginning = True
                    skip = False
                    for line in file_games:
                        #if there is a character that differentiates between the games (either EOL, comma, or a line)
                        if seperatedByLine:
                            if skip:
                                skip = False
                                continue
                            else:
                                skip = True
                        line = line.strip()
                        #Have ran into lists with this non utf-8 character
                        #https://stackoverflow.com/questions/2477452/%C3%A2%E2%82%AC-showing-on-page-instead-of
                        line = line.replace("â€™","'")
                        print(line)
                        price = game_to_lowest_grey_markerplace_value(line)
                        if isinstance(price, float) or isinstance(price, int):
                            price = str(price)
                            pass
                        elif price[0].isnumeric():
                            pass
                        #this is here for the case that price is a string ("Unavaible" or "Coming soon")
                        else:
                            price = '"'+price+'"'
                        #If there was an error while retriving the price then this game will be skipped
                        if not beginning:
                            json_file.write(',\n')
                        else:
                            beginning = False
                        json_file.write('{"game":"'+line+'", "price":'+price+'}')
                        if price == str(-1):
                            print(line+" was not found so it'll be listed as -1.")
                    json_file.write('\n]\n}')
                    json_file.close()
            except:
                print("File does not exist")
        else:
            print("Your file format is not of type .txt")

#helper function
def price_validation(price):
    #To avoid running into a bug when sorting the json file into a table if the price is unavaiable then it will be reflected as 0
    if price.strip() == 'Unavailable' or price.strip() == 'Coming soon':
        print("The price is listed as "+price+" so the game will be listed as 0.")
        price = 0.00
    else:
        #For when the '~' and the money symble (USD, GBP, EUR, etc.) is before the number.
        while not price[0].isnumeric():
            price = price[1:]
    return price

def game_to_lowest_grey_markerplace_value(game):
    #should be done with lxml instead of html.parser for speed purposes
    parser = 'html.parser'
    price = ''
    soup = ''
    #boolean for if the game will not be found in the search page
    hasBeenBundled = False
    modifiedGameString = game.replace(" ","-")
    #gg.deals changes commas to dashes
    modifiedGameString = modifiedGameString.replace(',','-')
    #GG.deals listing page URL ignores these characters "'",":"
    modifiedGameString = modifiedGameString.replace("'","")
    modifiedGameString = modifiedGameString.replace(":","")
    try:
        r = requests.get("https://gg.deals/game/"+modifiedGameString)
    except:
        print("Check your internet connection")
        return -1
    #if page of game has not been found right away
    if (r.status_code == 404):
        gamePageFound = False
        #requests.get encodes the gameString to ASCII automatically
        r = requests.get("https://gg.deals/games/",params = {'title': game})
        soup = BeautifulSoup(r.text,parser)
        listOfGames = soup.body.find('div', class_='main-content').find('div', id ='page').find('div', id='games-container').find('div', class_='game-section').find('div',class_='col-left').find('div').find('div').find_all('div', class_='hoverable-box')
        #Doesn't actually go through the whole list, just looks at the first element
        for gameInList in listOfGames:
            #if list is empty
            if 'empty' in gameInList['class']:
                print("The game in question ("+game+") could not be found")
                return -1
            else:
                #in the case that the first game in the search page is the matching game
                listingName = gameInList.find('div',class_='game-info-wrapper').find('div').find('div').find('a').get_text()
                #make them both all lower case
                if listingName.lower() == game.lower():
                    price = gameInList.find('div',class_='game-info-wrapper').find('div', class_='price-wrap').find('div', class_="shop-price-keyshops").find('div').text
                    return (price_validation(price))
        #if the 1st game that has been found in the list do not match the given game then have
        #the user confirm if there is a matching game
        if price == '':
            for gameInList in listOfGames:
                listingName = gameInList.find('div',class_='game-info-wrapper').find('div').find('div').find('a').get_text()
                answer = ''
                while(not (answer == 'y' or answer == 'yes' or answer == 'n' or answer == 'no')):
                    print("Is your game "+listingName+"?(y/n)")
                    answer = (input()).lower()                
                if (answer == 'y' or answer == 'yes'):
                    try:
                        price = gameInList.find('div',class_='game-info-wrapper').find('div', class_='price-wrap').find('div', class_="shop-price-keyshops").find('div').text
                        price = price_validation(price)
                    except:
                        return -1
                    break
                elif (answer == 'n' or answer == 'no'):
                    continue
            if price == '':
                print("The game in question("+game+")could not be found")
                price = -1
    else:
        print("Game found right away")
        gamePageFound = True
        soup = BeautifulSoup(r.text,parser)
    #if the page of the game has been found
    if gamePageFound and price == '':
        try:
            game_card = soup.body.find('div', class_ = "main-content").find('div',id="page").find('div',id="game-card")
            price = game_card.find('div').find('div').find('div', class_='col-right').find('div').find('div',class_="header-game-prices-tabs-content").find('div').find('div').find('div').find_next_sibling().find('a').find('span').text
            bundled = game_card.find('div', class_='game-tabs-container-wrapper').find('div').find('div').find('div').find('ul').find('li',id='tab-bundles')
            #Bundled status is still to be iplemented into the json file
            if bundled:
                hasBeenBundled = True
            #print(hasBeenBundled)
            price = price_validation(price)
        except:
            print("Error encountered in page. Price set to -1")
            return -1
    return price

#helper function
def organize_json(is_ascending, json_object):
    return_json = sorted(json_object['games'],key = lambda game: game["price"],reverse = not is_ascending)
    return return_json

def create_table():
    json_games_with_data = ''
    #not being used currently. Likely to be taken out
    #json_games_with_data_ext = ''
    json_var = ''
    popupFailed = False
    windows = False
    if platform == 'win32' or platform == 'cygwin':
        windows = True
    try:
        json_games_with_data = fd.askopenfilename()
        if json_games_with_data == '':
            raise Exception()
        #json_games_with_data_ext = os.path.splitext(json_games_with_data)[1]
    except:
        popupFailed = True
        print("You have not selected a file or the pop up failed.")
    if popupFailed:
        json_games_with_data = "files/game_data.json"
        if windows:
            json_games_with_data = "files\game_data.json"
        else:
            json_games_with_data = "files/game_data.json"
        print("Is your file located at "+json_games_with_data+" ?(y/n)")
        answer = input().lower()
        if 'y' == answer or 'yes' == answer:
            pass
        else:
            print("Please type in the path to your file (relative to this python file)")
            json_games_with_data = input()
            #json_games_with_data_ext = os.path.splitext(json_games_with_data)[1]
    try:
        with open(json_games_with_data,"r", encoding="utf-8") as file:
            json_var = json.loads(file.read())
    except:
        print("File either doesn't exist or is of wrong type")
        json_var = ''
    if json_var:
        print("Do you want to order by (1)ascending, (2)descending, or (3)none?")
        order = input()
        if order == '1' or order == '2':
            order = int(order)
        else:
            order = 3
        if windows:
            file_table_string = "files\\table.txt"
        else:
            file_table_string = "files/table.txt"
        if os.path.exists(file_table_string):
            os.remove(file_table_string)
        file_table = open(file_table_string,"w", encoding="utf-8")
        try:
            if order == 1:
                json_var['games'] = organize_json(True,json_var)
            elif order == 2:
                json_var['games'] = organize_json(False,json_var)
            #list without game prices is not working
            #not a priority so we will just comment out a couple of lines
            #print("Do you want to include game prices? (y/n)")
            #with_prices = input().lower()
            with_prices = 'y'
            if with_prices == 'y' or with_prices == 'yes':
                file_table.write(tabulate(json_var['games'], headers = 'keys' ,tablefmt = 'fancy_grid'))
            elif with_prices == 'n' or with_prices == 'no':
                temp_list = list()
                for game in json_var['games']:
                    temp_list.append([game['game']])
                file_table.write(tabulate(temp_list, headers = ['Games'],tablefmt = 'fancy_grid'))
            else:
                print("Response not understood")
        except:
            print("Something is wrong with your file")
        file_table.close()

def test():
    test_case = 2
    #game that doesn't exist but has results
    if test_case == 0:
        game = "Borderlands 4"
        print("Looking for "+game)
        print(game_to_lowest_grey_markerplace_value(game))
    #game with comma
    elif test_case == 1:
        game = "7,62 Hard Life"
        print("Looking for "+game)
        print(game_to_lowest_grey_markerplace_value(game))
    #game with "odd" character (’ instead of ')
    elif test_case == 2:
        game = "Morbid: The Seven Acolyte’s"
        print("Looking for "+game)
        print(game_to_lowest_grey_markerplace_value(game))
    elif test_case == 3:
        if platform == 'win32' or platform == 'cygwin': 
            convert_games_file_to_json(file_games_name='files/list.txt')
        else:
            convert_games_file_to_json(file_games_name='files\list.txt')

if __name__ == "__main__":
    main()
