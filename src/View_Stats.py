import statistics
import json

def view_stats(path):
    print('Let\'s compile our results and see what we collected!')
    while True:
        print('What kind of stats would you like to view?')
        print('1 ) Goldfish Stats')
        print('2 ) Game Stats')
        print('3 ) Tracked Card Stats')
        print('4 ) Back')

        choice = vet_user_num('')
        if choice == 4:
            break    
        elif choice == 1:
            gf_stats_menu(path)
        elif choice == 3:
            view_tracked_card_stats(path)

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

            turn_list = []
            wins = 0
            lands_list = []
            cards_list = []
            wturn_list = []
            lturn_list = []

            for i in range(len(stats_list)):
                turn_list.append(stats_list[i]['turn'])
                lands_list.append(stats_list[i]['lands'])
                cards_list.append(stats_list[i]['cards'])
                if stats_list[i]['win'] == True:
                    wins += 1
                    wturn_list.append(stats_list[i]['turn'])
                else:
                    lturn_list.append(stats_list[i]['turn'])

            #lands per game
            if choice == 1:
                print_lands_per_game(lands_list)
            #game length
            elif choice == 2: 
                try:
                    turn_average = sum(turn_list) / len(turn_list)
                    print(f'\nYour average game will last {turn_average} turns\nAnd will end most often on turn {statistics.mode(turn_list)}\n')
                except:
                    print('No games played')
                try:
                    wturn_average = sum(wturn_list) / len(wturn_list)
                    print(f'\nYour average win happens on turn {wturn_average}\n And you win most often on turn {statistics.mode(wturn_list)}\n')
                except:
                    print('Zero wins bro, maybe try harder')
                try:
                    lturn_average = sum(lturn_list) / len(lturn_list)
                    print(f'\nYour average loss happens on turn {lturn_average}\nAnd you lose most often on turn {statistics.mode(lturn_list)}\n')
                except:
                    print('See no L\'s, take no L\'s')
            #win rate
            elif choice == 3:
                try:
                    win_rate = (wins / len(stats_list)) * 100
                    print(f'\nYour current win rate is %{win_rate}\n')
                except:
                    print('%0 win rate :(')
            #cards drawn
            elif choice == 4:
                try:
                    average_cards = sum(cards_list) / len(cards_list)
                    print(f'\nDurring your average game you will draw {average_cards} cards\nAnd in most games you will have drawn {statistics.mode(cards_list)} cards.\n')
                except:
                    print('You haven\'t drawn any cards. I\'m sure that\'s part of the plan')
                    
def print_lands_per_game(lands):
    lands_average = sum(lands) / len(lands)
    print(f'\nDurring your average game you will play {lands_average} and in most games you will have played {statistics.mode(lands)} lands\n')


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
                                     

def view_tracked_card_stats(path):

    path = path + '/Deck_list.json'
    try:
        with open(path, 'r') as file:
            deck = json.load(file)
            deck_list = deck['card_list']
    except:
        print('Unable to open deck list file')

    tracked_list = []

    for card in deck_list:
        if card['tracked'] == True:
            tracked_list.append(card)

    while True:
        print('What card would you like to view stats for?')

        for i in range(len(tracked_list)):
            print(f'{i + 1} ) {tracked_list[i]['name']}')
        print(f'{len(tracked_list) + 1} ) Back')

        choice = vet_user_num('') - 1

        if choice == len(tracked_list):
            break

        print(f'{tracked_list[choice]['name']} Selected!')

        while True:
            print('1 ) Win Rate')
            print('2 ) Win Turn')
            print('3 ) Vibes')
            print('4 ) Back')
            
            choice2 = vet_user_num('')

            if choice2 == 1:
                wins_list = tracked_list[choice]['tracked_stats']['wins']
                try:
                    wins_average = sum(wins_list) / len(wins_list)
                    print(f'Your current win rate with {tracked_list[choice]['name']} is {wins_average * 100}')
                except:
                    print(f'No wins with {tracked_list[choice]['name']}')
            elif choice2 == 2:
                win_turn_list = tracked_list[choice]['tracked_stats']['win_turns']
                try:
                    win_turn_average = sum(win_turn_list) / len(win_turn_list)
                    print(f'In a given game that win and play {tracked_list[choice]['name']}, you win by turn {win_turn_average} on average')
                    print(f'And by turn {statistics.mode(win_turn_list)} most often')
                except:
                    print(f'No wins with {tracked_list[choice]['name']}')
            elif choice2 == 3:
                survey_list = tracked_list[choice]['tracked_stats']['survey']
                try:
                    survey_average = sum(survey_list) / len(survey_list)
                    print(f'On a scale of 1-5 you rate {tracked_list[choice]['name']} as a {survey_average} on average')
                    print(f'And as a {statistics.mode(survey_list)} most often')
                except:
                    print(f'No games played with {tracked_list[choice]['name']}')
            elif choice2 == 4:
                break


        
        
