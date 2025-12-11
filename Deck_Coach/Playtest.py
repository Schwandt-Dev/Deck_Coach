import json
import msvcrt

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

