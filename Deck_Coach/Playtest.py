import json
import msvcrt


# Life counter loggs to game_stats 
def playtest(path):
    life = 40
    turn_count = 0
    cards_drawn = 0
    exp_cnt = 0
    lands = 0
    win = False

    while True:
        print(f't) Turn        {turn_count}\nL/+/-) Life   {life}\nd) Cards Drawn {cards_drawn}\ne) Exp         {exp_cnt}\nl) Lands       {lands}\nw) Win\nf) Lose\n')
            
        interact = msvcrt.getch()
            
        if interact.decode() == 't':
            turn_count += 1
        elif interact.decode() == '+' or interact.decode() == '2':
            life += 1
        elif interact.decode() == '-' or interact.decode() == '1':
            life -= 1
        elif interact.decode() == 'e':
            exp_cnt += 1
        elif interact.decode() == 'd':
          cards_drawn += 1
        elif interact.decode() == 'l':
            lands += 1
        elif interact.decode() == 'w':
            win = True
            break
        elif interact.decode() == 'f':
            break
            

        if life <= 0:
            break
    
    old_path = path
    path = path + '/game_stats.json'
    
    try:
        with open(path, 'r') as file:
            session_list = json.load(file)
    except:
        session_list = []
    finally:
        stats_dict = {}
        stats_dict['turn'] = turn_count
        stats_dict['life'] = life
        stats_dict['exp'] = exp_cnt
        stats_dict['cards'] = cards_drawn
        stats_dict['lands'] = lands
        stats_dict['win'] = win
        session_list.append(stats_dict)
    with open(path, 'w') as file:
        json.dump(session_list, file, indent=4)
    survey(old_path, turn_count, win)
    shoutout(old_path)

# ask user survey questions for tracked cards 
def survey(path, turn_count, worl):
    deck_path = path + '/Deck_list.json'
    try:
        with open(deck_path, 'r') as file:
            deck = json.load(file)
        deck_list = deck['card_list']
        for i in range(len(deck_list)):
            if deck_list[i]['tracked'] == True:
                if worl == False:
                    deck_list[i]['tracked_stats']['wins'].append(0)
                else:
                    deck_list[i]['tracked_stats']['wins'].append(1)
                    deck_list[i]['tracked_stats']['win_turns'].append(turn_count)
                print(f'Did you play with {deck_list[i]['name']} this game?')
                print('1 ) Yes')
                print('2 ) No')
                if vet_user_num('') == 1:
                    print(f'How satisfied were you with the perfomance of {deck_list[i]['name']} this game?')
                    rating = vet_user_num('Enter a number 1-5: ')
                    if rating > 0 and rating < 6:
                        deck_list[i]['tracked_stats']['survey'].append(rating)
                else:
                    continue
        with open(deck_path, 'w') as file:
            json.dump(deck, file, indent=4)

    except:
        print('Unable to open deck list file.')


# Returns an integer value of a user input, positive number.   
def vet_user_num(string):
    while True:
        user_num = input(string)
        if user_num.isdigit():
            return int(user_num) 
        
def shoutout(path):
    try:
        with open(path + '/Deck_list.json', 'r') as file:
            deck = json.load(file)
            deck_list = deck['card_list']
        while True:
            print('Before we shuffle up and play again are there any cards that deserve a shoutout from the last game?')
            card = input('Enter a card of q to quit: ')
            card = card.lower()
            if card == 'q':
                break
            for i in range(len(deck_list)):
                if deck_list[i]['name'] == card:
                    if 'shoutout' in deck_list[i]:
                        deck_list[i]['shoutout'] += 1
                    else:
                        deck_list[i]['shoutout'] = 1
        with open(path + '/Deck_list.json', 'w') as file:
            json.dump(deck, file, indent=4)
    except:
        print('\nUnable to open deck list file. Enter cards via manage deck list')