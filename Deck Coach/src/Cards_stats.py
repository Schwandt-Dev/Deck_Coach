import json

#compiles all 100 cars into a deck_list and returns a dictionary with two items. The deck list and the tags of all cards in the list.
def get_cards(path):
    try:
        with open(path + '/Deck_list.json', 'r') as file:
            deck = json.load(file)
            saved_tags = deck['tags']
    except:
        deck = {}
        deck['card_list'] = []
        saved_tags = []
    finally:  
        while len(deck) < 100:
            card, tags_to_save = get_card(saved_tags)
            if card['name'] == 'q':
                break
            deck['card_list'].append(card)
            saved_tags = list(set(saved_tags + tags_to_save))
        deck['tags'] = saved_tags
        with open(path + '/Deck_list.json', 'w') as file:
            json.dump(deck, file, indent=4)
     
#retuns a single card as a dictionary
def get_card(saved_tags):
    card = {}
    print('Enter a card name exactly as it says on the card or press q to stop adding cards.')
    card_name = input()
    card['name'] = card_name.lower()
    if card['name'] == 'q':
        return card, []
    elif card['name'] in ['swamp', 'forest', 'plains', 'mountain', 'island', 'wastes']:
        card['copies'] = vet_user_num('How many copies are in your deck? ')
    print('What is the casting cost of the card? Enter a numerical value:')
    cost = vet_user_num('')
    card['cost'] = cost
    tags = []
    while True:
        
        print('\nLets enter some tags for this card. What is it\'s purpose in the deck?')
        print('Be sure to tag your commander as \'Commander\' and lands as \'land\'')
        print(f'Your current tags are {saved_tags}')
        print('Enter q to stop adding tags for this card')
        tag = input()
        if tag.lower() == 'q':
            break
        tags.append(tag.lower())
    card['tags'] = tags
    card['tracked'] = False
    return card, tags

# Returns an integer value of a user input, positive number.   
def vet_user_num(string):
    while True:
        user_num = input(string)
        if user_num.isdigit():
            return int(user_num)   
        
def edit_card(path):
    try:
        with open(path + '/Deck_list.json', 'r') as file:
            deck = json.load(file)
            saved_tags = deck['tags']
            deck_list = deck['card_list']
        while True:
            card = input('Enter the name of a card to edit or q to quit: ')
            card = card.lower()
            if card == 'q':
                break
            for i in range(len(deck_list)):
                if deck_list[i]['name'] == card:
                    print('Card info:')
                    print('Name: ', card)
                    print('Cost: ', deck_list[i]['cost'])
                    print('Tags: ', deck_list[i]['tags'])
                    if 'copies' in deck_list[i]:
                        print('Copies: ', deck_list[i]['copies'])
                    else:
                        print('Copies: 1')
                    print('Select 1) Edit Name 2) Edit cost 3) Edit Tags 4) Add/Remove Copies')
                    print('9) Delete Card')
                    choice = vet_user_num('')
                    if choice == 1:
                        new_name = input('Enter a new name for your card: ')
                        deck_list[i]['name'] = new_name
                    elif choice == 2:
                        new_cost = vet_user_num('Enter the cost of your card: ')
                        deck_list[i]['cost'] = new_cost
                    elif choice == 3:
                        tags = []
                        while True:
                            
                            print('\nLets enter some tags for this card. What is it\'s purpose in the deck?')
                            print('Be sure to tag your commander as \'Commander\'')
                            print('A single card can have as many tags as you like. Enter something like: Card Draw, Removal or Ramp')
                            print(f'Your current tags are {saved_tags}')
                            print('Enter q to stop adding tags for this card')
                            tag = input()
                            if tag.lower() == 'q':
                                break
                            tags.append(tag.lower())
                        deck_list[i]['tags'] = tags
                    elif choice == 4:
                        new_copies = vet_user_num('How many copies are in your deck? ')
                        deck_list[i]['copies'] = new_copies
                        saved_tags = cleanup_tags(deck_list)
                        
                    elif choice == 9:
                        del(deck_list[i])
                        saved_tags = cleanup_tags(deck_list)
                    

        with open(path + '/Deck_list.json', 'w') as file:
            deck['tags'] = saved_tags
            json.dump(deck, file, indent=4)


    except:
        print('Unable to read deck list file. Manage deck list and import cards first.')
        

def cleanup_tags(deck_list):
    tag_set = set()
    for i in range(len(deck_list)):
        tag_set.update(deck_list[i]['tags'])
    return list(sorted(tag_set))

def view_decklist(path):
    print('')
    try:
        with open(path + '/Deck_list.json', 'r') as file:
            deck = json.load(file)
            deck_list = deck['card_list']
            for i in range(len(deck_list)):
                print(deck_list[i]['name'])
        print('')
    except:
        print('\nUnable to open decklist file\n')
        
