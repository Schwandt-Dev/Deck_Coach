import os
import sys
import shutil
import Goldfish
import View_Stats
import Cards_stats
import Playtest
import Track_card
import auto_update
import subprocess
import requests


CURRENT_VERSION = "1.0.2"
HARM_MESSAGE = 'You may encounter some errors if you already have files or folders named Deck_Coach\nRemove any folders with this name if an error occurs and re-run.\n' \
'Recommended action is to delete these files before installing this update.'
UPDATE_MESSAGE = 'File system manager updated! Deck Coach will now Create it\'s own Deck Coach folder to store itself and all of your precious decks.\n' \
'Run once to create file system and then open the Deck Coach folder and double click on Deck Coach!'
def on_update_func():
    try:
        if os.path.exists('../Decks'):
            old_folder = '../Decks'
            new_folder = 'Decks'

            shutil.move(old_folder, new_folder)
    except:
        print('THERE CAN ONLY BE ONE\nIf you already have a file or folder named Deck_Coach remove it and restart the application')
    pass
############################### CHANGE LOG #########################################
   
####################################################################################

################################## TODO ############################################
    # add chopping block file
        # all cards start on the chopping block
        # cards with shoutouts are removed 
        # lands are removed
        # cards with least tags will rank highest on the chopping block
            # sub sort by cost high to low
        # identify veggies (card draw, removal) and remove from the chopping block
    # add feature to view games played in Deck Coach 
        #need to be able to delete bad stats that might be stored in game stats
    # use json for goldfish stats
####################################################################################

# Returns an integer value of a user input, positive number.   
def vet_user_num(string):
    while True:
        user_num = input(string)
        if user_num.isdigit():
            return int(user_num)                             
                                        
# Configures file system for Deck Coach if it is not already configured
def configure_fs():
    OWNER = "Schwandt-Dev"
    REPO = "Deck_Coach"
    APP_NAME = "Deck_Coach.exe"
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
    if 'Deck_Coach' not in os.getcwd():
        if not os.path.isdir('Deck_Coach'):
            os.mkdir('Deck_Coach')
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return

        data = response.json()

        for asset in data["assets"]:
            if asset["name"] == APP_NAME:
                auto_update.download_update(asset["browser_download_url"])
        auto_update.create_update_bat()
        subprocess.Popen([os.path.join(os.getcwd(), "update.bat")], creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit(0)

#main menu for an individual deck
def deck_menu_loop(path):   
    while True:
        print('Lets get some stats')
        print('Select one of the following:')
        print('1 ) Goldfish')
        print('2 ) Life Counter')
        print('3 ) View Stats')
        print('4 ) Manage Deck List')
        print('5 ) Back')
        print('6 ) Delete Deck')

                  
        choice = vet_user_num('')     
        if choice == 1:
           Goldfish.goldfish(path)
        elif choice == 2:
            Playtest.playtest(path)
        elif choice == 3:
            View_Stats.view_stats(path)
        elif choice == 5:
            return
        elif choice == 6:
            choice = vet_user_num(f'Are you sure you would like to delete {path}?\n1 ) Yes\n2 ) No\n')
            if choice == 1:
                shutil.rmtree(path)
                return
        elif choice == 4:
            while True:
                print('1 ) View card list')
                print('2 ) Add cards')
                print('3 ) Edit cards')
                print('4 ) Track cards')
                print('5 ) Back')
                choice = vet_user_num('')
                if choice == 2:
                    Cards_stats.get_cards(path)
                elif choice == 1:
                    Cards_stats.view_decklist(path) 
                elif choice == 3:
                    Cards_stats.edit_card(path)
                elif choice == 4:
                    Track_card.set_tracking(path)
                elif choice == 5:
                    break
             
            

#prints main menu options
#create new deck and enter selected deck menu                       
def main_menu_loop():
    
    print('Select one of the following to continue:')
    print('1 ) New Deck') 
    path = 'Decks/' #set base path
    try:
        decks_list = os.listdir(path)
    except:
        os.mkdir(path)
        decks_list = os.listdir(path)
    finally:
    #print list of decks created
        for i in range(len(decks_list)):
            print(i + 2, ')', decks_list[i]) 
        print('0 ) Save and Exit')
        choice = vet_user_num('') 
        if choice == 0:
            sys.exit()
        elif choice == 1:
            deck_name = input('Enter a name for your new deck: ')
            os.mkdir(path + deck_name)
        else:
            path = path + decks_list[choice - 2]
            print('\n' + decks_list[choice - 2], 'Selected\n')
            deck_menu_loop(path)


                   

# return count of matching character for the starting character of each line +1 to prevent divide by 0 errors.
def get_sessions(path, c):
    try:
        with open(path, 'r') as file:
            file.seek(0)
            stats = file.readlines()
            sessions = 1
            for line in stats:
               if line[0] == c:
                    sessions += 1
            return sessions
    except:
        print(f'\nError\nUnable to find file {path}\nIf you have not yet entered goldfish or game stats no file will exist\n')
        sys.exit()

if __name__ == "__main__":
    configure_fs()
    auto_update.check_for_updates(CURRENT_VERSION, HARM_MESSAGE)
    print(f'Welcome to Deck Coach Version {CURRENT_VERSION}!')
    if UPDATE_MESSAGE != '': print(UPDATE_MESSAGE)
    on_update_func()
    while True:
        main_menu_loop() 