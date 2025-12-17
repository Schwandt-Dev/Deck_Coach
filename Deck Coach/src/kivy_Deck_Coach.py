from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
import os
import shutil

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

        sm.current = 'main'
        return sm

class Main_Menu(Screen):
    def on_enter(self, **kwargs):
        super().__init__(**kwargs)
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
        print('Exiting...')
        App.get_running_app().stop()

    def deck_selection(self, instance):
        app = App.get_running_app()
        app.deck_name = instance.text
        self.manager.current = 'deck_menu'

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

class Deck_Menu_Screen(Screen):
    def on_enter(self):

        app = App.get_running_app()
        path = 'Decks/' + app.deck_name

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
        pass
    def goto_life_counter(self, instance):
        pass
    def goto_view_stats(self, instance):
        self.manager.current = 'view_stats_menu'
    def goto_deck_list(self, instance):
        self.manager.current = 'deck_list_menu'
    def go_back(self, instance):
        self.manager.current = 'main'
    def goto_warning(self, instance):
        self.manager.current = 'warning_screen'

class Warning_Screen(Screen):
    def on_enter(self):
        app = App.get_running_app()
        self.path = 'Decks/' + app.deck_name

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        warning_label = Label(text=f'Are you sure you want to delete {app.deck_name}?')
        confirm_btn = Button(text='Confirm', size_hint=(1, None), height=80)
        back_btn = Button(text='Back', size_hint=(1, None), height=80)

        confirm_btn.bind(on_press=self.delete_deck)
        back_btn.bind(on_press=self.go_back)

        layout.add_widget(warning_label)
        layout.add_widget(confirm_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'deck_menu'
    def delete_deck(self, instance):
        shutil.rmtree(self.path)
        self.go_back(instance)

class Deck_List_Menu(Screen):
    def on_enter(self):
        app = App.get_running_app()
        path = 'Decks/' + app.deck_name

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

class View_Stats_Menu(Screen):
    def on_enter(self):

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
        pass
    def goto_view_tracked_card_stats(self, instance):
        pass
    def go_back(self, instance):
        self.manager.current = 'deck_menu'

class Goldfish_Stats_Menu(Screen):
    def on_enter(self):

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



if __name__ == "__main__":
    Deck_Coach().run()