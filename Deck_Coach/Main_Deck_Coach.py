import os
import shutil
import Goldfish
import View_Stats
import Cards_stats
import Playtest
import Track_card


####################################################################################
    # add survey at the end of life counter
    # add option to compare tracked card with another card.
        # add option to replace tracked card with card being compared against 
### add method in view stats to view the status of tracked cards
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
        print('5 ) Track Cards')
        print('6 ) Back')
        print('7 ) Delete Deck')

                  
        choice = vet_user_num('')     
        if choice == 1:
           Goldfish.goldfish(path)
        elif choice == 2:
            Playtest.playtest(path)
        elif choice == 3:
            View_Stats.view_stats(path)
        elif choice == 6:
            return
        elif choice == 7:
            choice = vet_user_num(f'Are you sure you would like to delete {path}?\n1 ) Yes\n2 ) No\n')
            if choice == 1:
                shutil.rmtree(path)
                return
        elif choice == 4:
          Cards_stats.get_cards(path) 
        elif choice == 5:
            Track_card.set_tracking(path) 

#prints main menu options
#create new deck and enter selected deck menu                       
def main_menu_loop():
    print('Welcome to Deck Coach')
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


while True:
    main_menu_loop() 