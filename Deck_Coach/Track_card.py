import json

def set_tracking(path):
    try:
        with open(path + '/Deck_list.json', 'r') as file:
            deck = json.load(file)
            card_list = deck['card_list']
        while True:
            print('Enter a card name that you would like to track or press q to go back')
            card_name = input().lower()
            res = toggle_tracking(card_name, card_list)
            if res == 'q':
                break
        with open(path + '/Deck_list.json', 'w') as file:                        
            json.dump(deck, file, indent=4)
            return

    except:
        print('Could not open deck list file. Import deck before setting tracking.')
        return

def toggle_tracking(card_name, card_list):
        
    if card_name == 'q':
        return 'q'
    for i in range(len(card_list)):
        if card_list[i]['name'] == card_name:
            if card_list[i]['tracked'] == True:
                card_list[i]['tracked'] = False
                print(f'{card_name} has been deselected for tracking.')
            else:
                card_list[i]['tracked'] = True
                print(f'{card_name} has been set for tracking.')
                wins = []
                win_turns = []
                survey = []
                card_list[i]['tracked_stats'] = {}
                card_list[i]['tracked_stats']['wins'] = wins
                card_list[i]['tracked_stats']['win_turns'] = win_turns
                card_list[i]['tracked_stats']['survey'] = survey