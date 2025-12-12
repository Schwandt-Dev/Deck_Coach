import json

#enter prompted values in a single player
#game data will be stored in deck directory
#for future analysis
def goldfish(path):
    mul_count = 0
    turn_count = 1
    timer = 9999
    damage = 0
    kept = 7
   
    print('1 ) Golfish Hand')
    print('2 ) Goldfish Game')
   
    choice = vet_user_num('')               
    print('Let\'s shuffle up and draw 7, good luck!')
    old_path = path
   
    if choice == 1:    
        path = path + '/goldfish_hands.txt'
    elif choice == 2:
        path = path + '/goldfish_stats.txt'
       
    mulled_lands = []
       
    with open(path, 'a+') as file:   
        while True:
            print('1 ) Keep')
            print('2 ) Mulligan')
            choice = vet_user_num('')
            if choice == 2:
                mul_count += 1
                if mul_count == 9:
                    print('Drew -1 cards, you lose :(\n')
                    return 
                kept = mulligan(mul_count)
                mulled_lands.append(vet_user_num('How many lands are in your mulliganed hand? '))
            elif choice == 1:
                break
            else:
                continue               
        lands = vet_user_num('How many lands are in your hand? ')
       
        if 'hands' in path:
            for i in range(len(mulled_lands)):
                file.write(f'- Mulliganed hand with {mulled_lands[i]} lands.\n')
            file.write(f'Kept {kept} cards with {lands} lands\n')
            return
        timer = vet_user_num('How many turns would you like to play? ')       
        print('Combo or deal 120 damage. Good luck!')
        while turn_count <= timer:
            print('Damage:', damage, 'turn', turn_count, 'select an option:')
            print('1 ) Deal Damage')
            print('2 ) Pass Turn')
            print('3 ) Win')           
            choice = vet_user_num('')          
            if choice == 1:
                damage += vet_user_num('How much damage would you like to log? ')
                if damage >= 120:
                    print('You Win!!')
                    log_game(path, 'Win', turn_count, kept, lands, mulled_lands)
                    gen_game_summary(path, 'won', turn_count)
                    return
                continue
            elif choice == 2:
                turn_count += 1
                continue
            elif choice == 3:
                print('You Win!!')
                log_game(path, 'Win', turn_count, kept, lands, mulled_lands)
                gen_game_summary(path, 'won', turn_count)
                return
        print('You lose :(')
        log_game(path, 'Loss', turn_count, kept, lands, mulled_lands)
        gen_game_summary(path, 'lost', turn_count)
        return
    





def write_tbt(path, tbt_list):
    with open(path, 'a+') as file:
        for i in range(len(tbt_list)):
            file.write(tbt_list[i])
        return
    
def gen_game_summary(path, c, turn_count):
    sessions = get_sessions(path, '*')
    wins = get_sessions(path, 'W')   
       
    win_rate = ((wins - 1) / (sessions - 1)) * 100
   
    print(f'\nGame {c} on turn {turn_count}\nYour current win rate is %{win_rate}\n')
    return

#returns integer value of cards kept after
#mulligans are done       
def mulligan(mul_count):
    print('Draw', 8 - mul_count, 'and try again')
    return 8 - mul_count

#write game stats/golfish stats to file
def log_game(path, c, turn_count, cards_kept, lands_kept, mulled_lands):
   
    with open(path, 'a+') as file:
        sessions = get_sessions(path, '*')
        file.write(f'\n*** Session {sessions} ***\n')
        for i in range(len(mulled_lands)):
            file.write(f'- Mulliganed hand with {mulled_lands[i]} lands.\n')
        file.write(f'Kept {cards_kept} cards with {lands_kept} lands\n')
        file.write(c + '\n')
        file.write(f'Turn {turn_count}\n')
    return

# Returns an integer value of a user input, positive number.   
def vet_user_num(string):
    while True:
        user_num = input(string)
        if user_num.isdigit():
            return int(user_num)                             
                                     
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