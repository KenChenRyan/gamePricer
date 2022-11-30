# Game Pricer
A program that gives the user a list or chart of their spare PC game codes and their respective grey market place value.

### Installation
Either install the requried libraries that are listed in ```requirements.txt``` or install a Python virtual enviornment first.

To Install a virtual enviornment
```python3 -m venv venv```.
To activate/enter the virtual enviorenment
```./venv/Scripts/activate``` ("\" for a Windows based enviornment and "/" for a Unix based (Linux or macOS)

To install the required Python libraries (Whether inside a virtual enviorenment or instaling it outside)
```pip3 install -r .\requirements.txt```
### Running the program
```python3 game_pricer.py``` to run the program

To utilize the feature of converting a txt file of a list of games, the games in the files must be seperated by lines. See files/games.txt for an example.
### Features
- Take games from a .txt file (games should be seperated by lines) and give back a JSON file that has their respective grey market price listed. That JSON file can then be converted into a table that is saved to a .txt file.
- The table can be ordered from ascending, desending (in price) or left the way the games are given.
- Can find prices of individual games.

### To Do
- To see the mean of the first couple of listed prices. Or the lowest listed depending on if the amount of listings doesn't exceed a minimum. The option to only do the lowest listed should be avaiable.
- Have it exclude a lisitng based on the DRM of it (Steam/Epic Games Store/Rockstar Games Launcher/GOG/Ubisoft Launcher (UPlay)/EA Games Launcher)
