import statistics
import json

def view_stats(path):
    print('Let\'s compile our results and see what we collected!')
    while True:
        print('What kind of stats would you like to view?\n1 ) Goldfish Stats\n2 ) Game Stats\n3 ) Tracked Card Stats\n4 ) Back')
        choice = vet_user_num('')
        if choice == 4:
            break    
        elif choice == 1:
            gf_stats_menu(path)
            
        elif choice == 2:
            gs_path = path + '/game_stats.json'
            print('Select an option to view your game stats.')
            print('1 ) Lands per game')
            print('2 ) Game length')
            print('3 ) Win rate')
            print('4 ) Cards drawn')

            choice = vet_user_num('')

            try:
                with open(gs_path, 'r') as file:
                    stats_list = json.load(file)
            except:
                print('Unable to open game stats file')

            sessions = len(stats_list)
            turn_list = []
            wins = 0
            lands_list = []
            cards_list = []

            for i in range(len(stats_list)):
                turn_list.append(stats_list[i]['turn'])
                lands_list.append(stats_list[i]['lands'])
                cards_list.append(stats_list[i]['cards'])
                if stats_list[i]['win'] == True:
                    wins += 1

            #lands per game
            if choice == 1:
                print(lands_list)
            elif choice == 2:
                print('todo')
            elif choice == 3:
                print('todo')
            elif choice == 4:
                print('todo')

def print_lands_per_game(lands):
    lands_average = sum(lands) / len(lands)
    print(f'Durring your average game you will play {lands_average} and in most games you will have played {statistics.mode(lands)}')


def gf_stats_menu(path):
    gf_path = path + '/goldfish_stats.txt'
    while True:
        print('Select an option to view your goldfish stats:')            
        print('1 ) Lands in opening hand')
        print('2 ) Game length')
        print('3 ) Cards in opening hand')
        print('4 ) Back')
        choice = vet_user_num('')
        
        kept_cards, opening_lands, game_turn, win_rate_list, mulled_lands = view_common_stats(gf_path)
        
        tmp_path = path + '/goldfish_hands.txt'
        
        gfh_kept_cards, gfh_opening_lands, gfh_mulled_lands = gf_hands_stats(tmp_path)
        
        kept_cards.extend(gfh_kept_cards)
        opening_lands.extend(gfh_opening_lands)
        mulled_lands.extend(gfh_mulled_lands)

        if choice == 4:
            return

        elif choice == 1:
            print_opening_lands(opening_lands, mulled_lands)
                
        elif choice == 2:
            print_game_length(win_rate_list, game_turn)
            
            
        elif choice == 3:
            print_opening_cards(kept_cards)


def print_opening_cards(kept_cards):
    hand_average = sum(kept_cards) / len(kept_cards)
    print(f'Your hands contain an average of {hand_average} cards and are most likely to contain {statistics.mode(kept_cards)} cards.\n')


def print_game_length(win_rate_list, game_turn):
    w_game_turns = []
    l_game_turns = []
              
    for i in range(len(win_rate_list)):
        if win_rate_list[i] == 'w':
           w_game_turns.append(game_turn[i])
        elif win_rate_list[i] == 'l':
            l_game_turns. append(game_turn[i])
                
    if game_turn != [] or w_game_turns != [] or l_game_turns != []:
        if game_turn != []:
            print(f'\nYour average game lasts {sum(game_turn) / len(game_turn)} turns\n')
        if w_game_turns != []:
            print(f'Your average game win occurs in {sum(w_game_turns) / len(w_game_turns)} turns\nand you win most often on turn {statistics.mode(w_game_turns)}\n')
        if l_game_turns != []:
             print(f'Your average game loss occurs in {sum(l_game_turns) / len(l_game_turns)} turns\nand you lose most often on turn {statistics.mode(l_game_turns)}\n')
               
    else:
        print('\nnot enough stats to determine\n')


def print_opening_lands(opening_lands, mulled_lands):
    total_lands = sum(opening_lands) + sum(mulled_lands)
    total_len = len(opening_lands) + len(mulled_lands)
    kept_lands_average = sum(opening_lands) / len(opening_lands)
    print(f'\nYour kept opening hands have an average of {kept_lands_average}\n lands and are most likely to contain {statistics.mode(opening_lands)} lands after mulligans\n')
    opening_lands.extend(mulled_lands)
    print(f'Your average opening hand contains an average of {total_lands / total_len}\n lands and is most likely to contain {statistics.mode(opening_lands)} lands.\n')
    return 

def gf_hands_stats(path):
    kept_cards = []
    opening_lands = []
    mulled_lands = []
    
    try:
        with open(path, 'r') as file:
            for line in file:
                if line[0] == '-':
                    mulled_lands.append(int(line[23]))
                else:
                    kept_cards.append(int(line[5]))
                    opening_lands.append(int(line[18]))
            return kept_cards, opening_lands, mulled_lands
    except:
        return kept_cards, opening_lands, mulled_lands


def view_common_stats(path):
    kept_cards = []
    opening_lands = []
    game_turn = []
    win_rate_list = []     
    mulled_lands = []
   
    try:
        with open(path, 'r') as file:
            stats = file.readlines()
                   
            for i in range(len(stats)):
                if stats[i][0] == 'K':
                    kept_cards.append(int(stats[i][5]))
                    opening_lands.append(int(stats[i][18]))
                elif stats[i][0] == 'T':
                    game_turn.append(int(stats[i][5]))
                elif stats[i][0] == 'W':
                    win_rate_list.append('w')
                elif stats[i][0] == 'L':
                    win_rate_list.append('l')
                elif stats[i][0] == '-':
                    mulled_lands.append(int(stats[i][23]))
               
    except:
        print('Unable to open goldfish_stats.txt file. File may not exist yet if goldfish games have not been played.')
    finally:
        return kept_cards, opening_lands, game_turn, win_rate_list, mulled_lands
    
# Returns an integer value of a user input, positive number.   
def vet_user_num(string):
    while True:
        user_num = input(string)
        if user_num.isdigit():
            return int(user_num)                             
                                     

