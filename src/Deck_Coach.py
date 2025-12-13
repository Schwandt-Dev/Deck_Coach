import os
import shutil
import Goldfish
import View_Stats
import Cards_stats
import Playtest
import Track_card
import auto_update


####################################################################################
    # Walk user through setting up git account so they can recieve updates (optional) from git 
    # or store data locally.
    # convert to exe so we can click run instead of relying on users installing python 12
    # add method in view stats to view the stats of tracked cards
    # add chopping block file
        # all cards start on the chopping block
        # cards with shoutouts are removed 
        # lands are removed
        # cards with least tags will rank highest on the chopping block
            # sub sort by cost high to low
        # identify veggies (card draw, removal) and remove from the chopping block
####################################################################################

# Returns an integer value of a user input, positive number.   
def vet_user_num(string):
    while True:
        user_num = input(string)
        if user_num.isdigit():
            return int(user_num)                             
                                        



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
            print('1 ) View card list')
            print('2 ) Add cards')
            print('3 ) Edit cards')
            print('4 ) Track cards')
            choice = vet_user_num('')
            if choice == 2:
                Cards_stats.get_cards(path)
            elif choice == 1:
                Cards_stats.view_decklist(path) 
            elif choice == 3:
                Cards_stats.edit_card(path)
            elif choice == 4:
                Track_card.set_tracking(path)
             
            

#prints main menu options
#create new deck and enter selected deck menu                       
def main_menu_loop():
    
    print('Select one of the following to continue:')
    print('1 ) New Deck') 
    path = '../Decks/' #set base path
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
            exit()
        elif choice == 1:
            deck_name = input('Enter a name for your new deck: ')
            os.mkdir(path + deck_name)
            return
        elif choice - 2 >= len(decks_list):
            return
        else:
            path = path + decks_list[choice - 2]
            print('\n' + decks_list[choice - 2], 'Selected\n')
            deck_menu_loop(path)
            return


                   

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
        exit(0)

if __name__ == "__main__":
    auto_update.check_for_updates()
    print('Welcome to Deck Coach Version!')
    while True:
        main_menu_loop() 