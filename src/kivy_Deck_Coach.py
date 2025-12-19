from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import sp
import os
import shutil
import json
import statistics

class Deck_Coach(App):

    deck_name = None

    def build(self):
        sm = ScreenManager()

        sm.add_widget(Main_Menu(name='main'))
        sm.add_widget(New_Deck_Screen(name='new_deck_screen'))
        sm.add_widget(Deck_Menu_Screen(name='deck_menu'))
        sm.add_widget(Warning_Screen(name='warning_screen'))
        sm.add_widget(Deck_List_Menu(name='deck_list_menu'))
        sm.add_widget(View_Stats_Menu(name='view_stats_menu'))
        sm.add_widget(Goldfish_Stats_Menu(name='goldfish_stats_menu'))
        sm.add_widget(Game_Stats_Menu(name='game_stats_menu'))
        sm.add_widget(Life_Counter_Screen(name='life_counter_screen'))
        sm.add_widget(Goldfish_Screen(name='goldfish_screen'))

        sm.current = 'main'
        return sm
    
# Fully Functional
class Main_Menu(Screen):
    def on_enter(self, **kwargs):
        super().__init__(**kwargs)

        self.clear_widgets()
        #layout format current layout on screen
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        decks_list = self.get_decks()
        #create list of buttons to display and bind to functions
        buttons = [('New Deck', self.new_deck)]
        exit_btn = ('Exit', self.exit_app)
        for i in range(len(decks_list)):
            deck_btn = (decks_list[i], self.deck_selection)
            buttons.append(deck_btn)
        buttons.append(exit_btn)

        for text, callback in buttons:
            btn = Button(text=text, size_hint=(1, None), height=50)
            btn.bind(on_press=callback)
            layout.add_widget(btn)

        self.add_widget(layout)
        
    def get_decks(self):
        path = 'Decks' #set base path
        #error check for file already named Decks and make Directory
        if os.path.exists(path) and os.path.isdir(path + '/') == False:
            # Hard Remove, your fault if you put files in my app directory
            os.remove(path)
            os.mkdir(path)
        elif os.path.exists(path) == False:
            os.mkdir(path)
        return os.listdir(path)
        
    def new_deck(self, instance):
        self.manager.current = 'new_deck_screen'


    def exit_app(self, instance):
        App.get_running_app().stop()

    def deck_selection(self, instance):
        app = App.get_running_app()
        app.deck_name = instance.text
        self.manager.current = 'deck_menu'
# Fully Functional
class New_Deck_Screen(Screen):
    def on_enter(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text="Enter a name for your new deck")
        self.txtbox = TextInput(multiline=False, size_hint=(1, None), height=40)
        submit_btn = Button(text='Submit', size_hint=(1, None), height=50)

        self.layout.add_widget(popup_label)
        self.layout.add_widget(self.txtbox)
        self.layout.add_widget(submit_btn)

        submit_btn.bind(on_press=self.submit_name)

        self.add_widget(self.layout)
    
    def submit_name(self, instance):
        path = 'Decks/'
        try:
            os.mkdir(path + self.txtbox.text)
        except Exception as e:
            print("Deck already exists with that name", e)

        self.manager.current = 'main'
# Fully Functional
class Deck_Menu_Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        goldfish_btn = Button(text='Goldfish', size_hint=(1, None), height=50)
        life_counter_btn = Button(text='Life Counter', size_hint=(1, None), height=50)
        view_stats_btn = Button(text='View Stats', size_hint=(1, None), height=50)
        deck_list_btn = Button(text='Deck List', size_hint=(1, None), height = 50)
        back_btn = Button(text='Back', size_hint=(1, None), height=50)
        delete_btn = Button(text='Delete Deck', size_hint=(1, None), height = 50)

        layout.add_widget(goldfish_btn)
        layout.add_widget(life_counter_btn)
        layout.add_widget(view_stats_btn)
        layout.add_widget(deck_list_btn)
        layout.add_widget(back_btn)
        layout.add_widget(delete_btn)

        goldfish_btn.bind(on_press=self.goto_goldfish)
        life_counter_btn.bind(on_press=self.goto_life_counter)
        view_stats_btn.bind(on_press=self.goto_view_stats)
        deck_list_btn.bind(on_press=self.goto_deck_list)
        back_btn.bind(on_press=self.go_back)
        delete_btn.bind(on_press=self.goto_warning)

        self.add_widget(layout)

    def goto_goldfish(self, instance):
        self.manager.current = 'goldfish_screen'
    def goto_life_counter(self, instance):
        self.manager.current = 'life_counter_screen'
    def goto_view_stats(self, instance):
        self.manager.current = 'view_stats_menu'
    def goto_deck_list(self, instance):
        self.manager.current = 'deck_list_menu'
    def go_back(self, instance):
        self.manager.current = 'main'
    def goto_warning(self, instance):
        self.manager.current = 'warning_screen'
# Fully Functional
class Warning_Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.warning_label = Label(text='', size_hint_y=None, height=80)
        confirm_btn = Button(text='Confirm', size_hint=(1, None), height=80)
        back_btn = Button(text='Back', size_hint=(1, None), height=80)

        confirm_btn.bind(on_press=self.delete_deck)
        back_btn.bind(on_press=self.go_back)

        layout.add_widget(self.warning_label)
        layout.add_widget(confirm_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_enter(self):
        app = App.get_running_app()
        self.path = 'Decks/' + app.deck_name
        self.warning_label.text = f'Are you sure you want to delete {app.deck_name}'

    def go_back(self, instance):
        self.manager.current = 'deck_menu'
    def delete_deck(self, instance):
        app = App.get_running_app()
        self.path = 'Decks/' + app.deck_name
        shutil.rmtree(self.path)
        self.manager.current = 'main'

class Deck_List_Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        view_card_list_btn = Button(text='View Deck List', size_hint=(1, None), height=50)
        add_cards_btn = Button(text='Add Cards', size_hint=(1, None), height=50)
        edit_cards_btn = Button(text='Edit Cards', size_hint=(1, None), height=50)
        track_cards_btn = Button(text='Track Cards', size_hint=(1, None), height=50)
        back_btn = Button(text='Back', size_hint=(1, None), height=50)

        layout.add_widget(view_card_list_btn)
        layout.add_widget(add_cards_btn)
        layout.add_widget(edit_cards_btn)
        layout.add_widget(track_cards_btn)
        layout.add_widget(back_btn)

        view_card_list_btn.bind(on_press=self.goto_view_cards)
        add_cards_btn.bind(on_press=self.goto_add_cards)
        edit_cards_btn.bind(on_press=self.goto_edit_cards)
        track_cards_btn.bind(on_press=self.goto_track_cards)
        back_btn.bind(on_press=self.go_back)

        self.add_widget(layout)

    def goto_view_cards(self, instance):
        pass
    def goto_add_cards(self, instance):
        pass
    def goto_edit_cards(self, instance):
        pass
    def goto_track_cards(self, instance):
        pass
    def go_back(self, instance):
        self.manager.current = 'deck_menu'
# Need to implement add cards first
class View_Stats_Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        goldfish_stats_btn = Button(text='Goldfish Stats', size_hint=(1, None), height=50)
        game_stats_btn = Button(text='Game Stats', size_hint=(1, None), height=50)
        tracked_card_stats_btn = Button(text='Tracked Card Stats', size_hint=(1, None), height=50)
        back_btn = Button(text='Back', size_hint=(1, None), height = 50)

        layout.add_widget(goldfish_stats_btn)
        layout.add_widget(game_stats_btn)
        layout.add_widget(tracked_card_stats_btn)
        layout.add_widget(back_btn)

        goldfish_stats_btn.bind(on_press=self.goto_view_goldfish_stats)
        game_stats_btn.bind(on_press=self.goto_view_game_stats)
        tracked_card_stats_btn.bind(on_press=self.goto_view_tracked_card_stats)
        back_btn.bind(on_press=self.go_back)

        self.add_widget(layout)

    def goto_view_goldfish_stats(self, instance):
        self.manager.current = 'goldfish_stats_menu'
    def goto_view_game_stats(self, instance):
        self.manager.current = 'game_stats_menu'
    def goto_view_tracked_card_stats(self, instance):
        pass
    def go_back(self, instance):
        self.manager.current = 'deck_menu'

class Goldfish_Stats_Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        lands_in_opening_hand_btn = Button(text='Lands in opening hand', size_hint=(1, None), height=50)
        game_length_btn = Button(text='Game Length', size_hint=(1, None), height=50)
        cards_in_opening_hand_btn = Button(text='Cards in opening hand', size_hint=(1, None), height=50)
        back_btn = Button(text='Back', size_hint=(1, None), height=50)

        layout.add_widget(lands_in_opening_hand_btn)
        layout.add_widget(game_length_btn)
        layout.add_widget(cards_in_opening_hand_btn)
        layout.add_widget(back_btn)

        lands_in_opening_hand_btn.bind(on_press=self.get_opening_lands_stats)
        game_length_btn.bind(on_press=self.get_game_length_stats)
        cards_in_opening_hand_btn.bind(on_press=self.get_opening_cards_stats)
        back_btn.bind(on_press=self.go_back)

        self.add_widget(layout)

    def get_opening_lands_stats(self, instance):
        pass
    def get_game_length_stats(self, instance):
        pass
    def get_opening_cards_stats(self, instance):
        pass
    def go_back(self, instance):
        self.manager.current = 'view_stats_menu'
# Fully Functional
class Game_Stats_Menu(Screen):
    def on_enter(self, **kwargs):
        super().__init__(**kwargs)
        self.clear_widgets()

        app = App.get_running_app()
        self.path = 'Decks/' + app.deck_name + '/game_stats.json'

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        lands_per_game_btn = Button(text='Lands per Game', size_hint=(1, None), height=50)
        game_length_btn = Button(text='Game Length', size_hint=(1, None), height=50)
        win_rate_btn = Button(text='Win Rate', size_hint=(1, None), height=50)
        cards_drawn_btn = Button(text='Cards Drawn', size_hint=(1, None), height=50)
        back_btn = Button(text='Back', size_hint=(1, None), height=50)

        layout.add_widget(lands_per_game_btn)
        layout.add_widget(game_length_btn)
        layout.add_widget(win_rate_btn)
        layout.add_widget(cards_drawn_btn)
        layout.add_widget(back_btn)

        lands_per_game_btn.bind(on_press=self.view_lands_per_game)
        game_length_btn.bind(on_press=self.view_game_length)
        win_rate_btn.bind(on_press=self.view_win_rate)
        cards_drawn_btn.bind(on_press=self.view_cards_drawn)
        back_btn.bind(on_press=self.go_back)

        self.add_widget(layout)

    def view_lands_per_game(self, instance):
        try:
            with open(self.path, 'r') as file:
                games_list = json.load(file)

                cards_drawn_list = []
            for game in games_list:
                cards_drawn_list.append(game['Lands'])

            if sum(cards_drawn_list) == 0:
                cards_average = 0
            else:
                cards_average = sum(cards_drawn_list) / len(cards_drawn_list)

            self.clear_widgets()
            layout = BoxLayout(orientation = 'vertical', padding=10, spacing=10)
            cards_label = Label(text=f'By the end of a typical game you will have played an average of {cards_average} lands.\nAnd by the end of most games you will have played {statistics.mode(cards_drawn_list)} lands.', font_size=sp(24))
            back_btn = Button(text='Back', size_hint=(1, None), height=100)
            back_btn.bind(on_press=self.reload)
            layout.add_widget(cards_label)
            layout.add_widget(back_btn)

            self.add_widget(layout)

        except:
            self.clear_widgets()
            layout = BoxLayout(orientation = 'vertical', padding=10, spacing=10)
            fail_label = Label(text='Unable to open Game Stats file.\nThe file will not exist if you have not played games via the life counter.', font_size=sp(24))
            back_btn = Button(text='Back', size_hint=(1, None), height=100)
            back_btn.bind(on_press=self.reload)
            layout.add_widget(fail_label)
            layout.add_widget(back_btn)

            self.add_widget(layout)
    def view_game_length(self, instance):
        try:
            with open(self.path, 'r') as file:
                games_list = json.load(file)

                cards_drawn_list = []
            for game in games_list:
                cards_drawn_list.append(game['Turn'])

            if sum(cards_drawn_list) == 0:
                cards_average = 0
            else:
                cards_average = sum(cards_drawn_list) / len(cards_drawn_list)

            self.clear_widgets()
            layout = BoxLayout(orientation = 'vertical', padding=10, spacing=10)
            cards_label = Label(text=f'Your typiacal game lasts {cards_average} turns.\nAnd will end most often by turn {statistics.mode(cards_drawn_list)}.', font_size=sp(24))
            back_btn = Button(text='Back', size_hint=(1, None), height=100)
            back_btn.bind(on_press=self.reload)
            layout.add_widget(cards_label)
            layout.add_widget(back_btn)

            self.add_widget(layout)

        except Exception as e:
            print(e)
            self.clear_widgets()
            layout = BoxLayout(orientation = 'vertical', padding=10, spacing=10)
            fail_label = Label(text='Unable to open Game Stats file.\nThe file will not exist if you have not played games via the life counter.', font_size=sp(24))
            back_btn = Button(text='Back', size_hint=(1, None), height=100)
            back_btn.bind(on_press=self.reload)
            layout.add_widget(fail_label)
            layout.add_widget(back_btn)

            self.add_widget(layout)
    def view_win_rate(self, instance):
        try:
            with open(self.path, 'r') as file:
                games_list = json.load(file)

                results_list = []
            for game in games_list:
                if game['result'] == 'Win':
                    results_list.append(1)
                else: results_list.append(0)

            if sum(results_list) == 0:
                win_rate = 0
            else:
                win_rate = (sum(results_list) / len(results_list)) * 100

            self.clear_widgets()
            layout = BoxLayout(orientation = 'vertical', padding=10, spacing=10)
            cards_label = Label(text=f'Your Current win rate is %{win_rate}', font_size=sp(32))
            back_btn = Button(text='Back', size_hint=(1, None), height=100)
            back_btn.bind(on_press=self.reload)
            layout.add_widget(cards_label)
            layout.add_widget(back_btn)

            self.add_widget(layout)

        except Exception as e:
            print(e)
            self.clear_widgets()
            layout = BoxLayout(orientation = 'vertical', padding=10, spacing=10)
            fail_label = Label(text='Unable to open Game Stats file.\nThe file will not exist if you have not played games via the life counter.', font_size=sp(24))
            back_btn = Button(text='Back', size_hint=(1, None), height=100)
            back_btn.bind(on_press=self.reload)
            layout.add_widget(fail_label)
            layout.add_widget(back_btn)

            self.add_widget(layout) 
    def view_cards_drawn(self, instance):
        try:
            with open(self.path, 'r') as file:
                games_list = json.load(file)

                cards_drawn_list = []
            for game in games_list:
                cards_drawn_list.append(game['Draws'])

            if sum(cards_drawn_list) == 0:
                cards_average = 0
            else:
                cards_average = sum(cards_drawn_list) / len(cards_drawn_list)

            self.clear_widgets()
            layout = BoxLayout(orientation = 'vertical', padding=10, spacing=10)
            cards_label = Label(text=f'By the end of a typical game you will have drawn average of {cards_average} cards.\nAnd by the end of most games you will have drawn {statistics.mode(cards_drawn_list)} cards.', font_size=sp(24))
            back_btn = Button(text='Back', size_hint=(1, None), height=100)
            back_btn.bind(on_press=self.reload)
            layout.add_widget(cards_label)
            layout.add_widget(back_btn)

            self.add_widget(layout)

        except Exception as e:
            print(e)
            self.clear_widgets()
            layout = BoxLayout(orientation = 'vertical', padding=10, spacing=10)
            fail_label = Label(text='Unable to open Game Stats file.\nThe file will not exist if you have not played games via the life counter.', font_size=sp(24))
            back_btn = Button(text='Back', size_hint=(1, None), height=100)
            back_btn.bind(on_press=self.reload)
            layout.add_widget(fail_label)
            layout.add_widget(back_btn)

            self.add_widget(layout)    
        
    def go_back(self, instance):
        self.manager.current = 'view_stats_menu'

    def reload(self, instance):
        self.on_enter()

# Fully Functional
class Life_Counter_Screen(Screen):
    def on_enter(self):
        self.clear_widgets()

        app = App.get_running_app()
        self.path = 'Decks/' + app.deck_name + '/game_stats.json'

        layout = GridLayout(
            cols=4,
            padding=10,
            spacing=10,
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))

        self.values = {
            'Life':40,
            'Turn':0,
            'Draws':0,
            'Lands':0,
            'Exp':0
        }

        self.value_labels = {}


        for name in self.values:
            minus_btn = Button(text='-', size_hint=(1, None), height=50)
            minus_btn.row_name = name
            minus_btn.bind(on_press=self.decrement)

            value_label = Label(text=str(self.values[name]))
            value_label.row_name = name
            self.value_labels[name] = value_label

            plus_btn = Button(text='+', size_hint=(1, None), height=50)
            plus_btn.row_name = name
            plus_btn.bind(on_press=self.increment)

            name_label = Label(text=name)

            layout.add_widget(minus_btn)
            layout.add_widget(value_label)
            layout.add_widget(plus_btn)
            layout.add_widget(name_label)

        win_btn = Button(text='Win', size_hint=(1, None), height=50)
        back_btn = Button(text='Back', size_hint=(1, None), height=50)
        lose_btn = Button(text='Lose', size_hint=(1, None), height=50)

        win_btn.bind(on_press=self.end_game)
        lose_btn.bind(on_press=self.end_game)
        back_btn.bind(on_press=self.go_back)

        layout.add_widget(win_btn)
        layout.add_widget(back_btn)
        layout.add_widget(lose_btn)

        self.add_widget(layout)

    def decrement(self, instance):
        name = instance.row_name
        self.values[name] -= 1
        self.value_labels[name].text = str(self.values[name])
    def increment(self, instance):
        name = instance.row_name
        self.values[name] += 1
        self.value_labels[name].text = str(self.values[name])
    def go_back(self, instance):
        self.manager.current = 'deck_menu'
    def end_game(self, instance):
        result = instance.text

        try:
            with open(self.path, 'r') as file:
                games_list = json.load(file)
        except:
            games_list = []
        
        game = {'result':result}
        game.update(self.values)
        games_list.append(game)
        
        try:
            with open(self.path, 'w') as file:
                json.dump(games_list, file, indent=4)
        except Exception as e:
            print('Houston we have a problem ', e)

        self.manager.current = 'deck_menu'
# Fix Goldfish Hand
class Goldfish_Screen(Screen):
    def on_enter(self):
        self.clear_widgets()

        app = App.get_running_app()
        self.path = 'Decks/' + app.deck_name + '/goldfish_stats.json'

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        gfh_btn = Button(text='Goldfish Hand', size_hint=(1, None), height=200)
        gfg_btn = Button(text='Goldfish Game', size_hint=(1, None), height=200)

        gfh_btn.bind(on_press=self.goldfish_hand)
        gfg_btn.bind(on_press=self.goldfish_game)

        layout.add_widget(gfh_btn)
        layout.add_widget(gfg_btn)

        self.add_widget(layout)


    def goldfish_hand(self, instance):
        self.clear_widgets()

        layout = GridLayout(
            cols=4,
            padding=10,
            spacing=10,
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))

        self.values = {
            'Damage':120,
            'Life':40,
            'Turn':0,
            'Draws':0,
            'Lands':0,
            'Exp':0
        }

        self.value_labels = {}


        for name in self.values:
            minus_btn = Button(text='-', size_hint=(1, None), height=50)
            minus_btn.row_name = name
            minus_btn.bind(on_press=self.decrement)

            value_label = Label(text=str(self.values[name]))
            value_label.row_name = name
            self.value_labels[name] = value_label

            plus_btn = Button(text='+', size_hint=(1, None), height=50)
            plus_btn.row_name = name
            plus_btn.bind(on_press=self.increment)

            name_label = Label(text=name)

            layout.add_widget(minus_btn)
            layout.add_widget(value_label)
            layout.add_widget(plus_btn)
            layout.add_widget(name_label)

        win_btn = Button(text='Keep', size_hint=(1, None), height=50)
        back_btn = Button(text='Back', size_hint=(1, None), height=50)
        lose_btn = Button(text='Mulligan', size_hint=(1, None), height=50)

        win_btn.bind(on_press=self.end_game)
        lose_btn.bind(on_press=self.end_game)
        back_btn.bind(on_press=self.go_back)

        layout.add_widget(win_btn)
        layout.add_widget(back_btn)
        layout.add_widget(lose_btn)

        self.add_widget(layout)
    def goldfish_game(self, instance):
        self.clear_widgets()

        layout = GridLayout(
            cols=4,
            padding=10,
            spacing=10,
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter('height'))

        self.values = {
            'Damage':120,
            'Life':40,
            'Turn':0,
            'Draws':0,
            'Lands':0,
            'Exp':0
        }

        self.value_labels = {}


        for name in self.values:
            minus_btn = Button(text='-', size_hint=(1, None), height=50)
            minus_btn.row_name = name
            minus_btn.bind(on_press=self.decrement)

            value_label = Label(text=str(self.values[name]))
            value_label.row_name = name
            self.value_labels[name] = value_label

            plus_btn = Button(text='+', size_hint=(1, None), height=50)
            plus_btn.row_name = name
            plus_btn.bind(on_press=self.increment)

            name_label = Label(text=name)

            layout.add_widget(minus_btn)
            layout.add_widget(value_label)
            layout.add_widget(plus_btn)
            layout.add_widget(name_label)

        win_btn = Button(text='Win', size_hint=(1, None), height=50)
        back_btn = Button(text='Back', size_hint=(1, None), height=50)
        lose_btn = Button(text='Lose', size_hint=(1, None), height=50)

        win_btn.bind(on_press=self.end_game)
        lose_btn.bind(on_press=self.end_game)
        back_btn.bind(on_press=self.go_back)

        layout.add_widget(win_btn)
        layout.add_widget(back_btn)
        layout.add_widget(lose_btn)

        self.add_widget(layout)

    def decrement(self, instance):
        name = instance.row_name
        self.values -= 1
        self.value_labels[name].text = str(self.values[name])
    def increment(self, instance):
        name = instance.row_name
        self.values += 1
        self.value_labels[name].text = str(self.values[name])
    def go_back(self, instance):
        self.manager.current = 'deck_menu'
    def end_game(self, instance):
        result = instance.text

        try:
            with open(self.path, 'r') as file:
                games_list = json.load(file)
        except:
            games_list = []
        
        game = {'result':result}
        game.update(self.values)
        game['Damage'] = 120 - game['Damage']
        games_list.append(game)
        
        try:
            with open(self.path, 'w') as file:
                json.dump(games_list, file, indent=4)
        except Exception as e:
            print('Houston we have a problem ', e)

        self.manager.current = 'deck_menu'

# Need to implement add cards first
class Tracked_Card_Stats_Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        pass

        
if __name__ == "__main__":
    Deck_Coach().run()