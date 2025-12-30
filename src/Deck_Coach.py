from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import sp
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import os
import shutil
import json
import statistics
from time import sleep
import sys
import requests
import subprocess
import threading


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
        sm.add_widget(Add_Cards_Screen(name='add_cards_screen'))
        sm.add_widget(Track_Cards_Screen(name='track_cards_screen'))
        sm.add_widget(View_Cards_Screen(name='view_cards_screen'))
        sm.add_widget(Edit_Cards_Screen(name='edit_cards_screen'))
        sm.add_widget(View_Tracked_Cards_Stats_Screen(name='view_tracked_cards_stats_screen'))
        sm.add_widget(Update_Check_Screen(name='update_check'))
        sm.add_widget(Bootstrap_Screen(name='bootstrap'))
        

        sm.current = 'main'
        #sm.current = 'bootstrap'
        return sm
    
 
class Bootstrap_Screen(Screen):
    def on_enter(self):
        if not self.is_bootstrapped():
            os.mkdir('Deck Coach')
            source_exe = sys.executable
            self.create_bootstrap_bat(source_exe)
            subprocess.Popen(
                ["bootstrap.bat"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            sys.exit(0)
            return

        # Already bootstrapped → continue
        self.manager.current = "update_check"
    def is_bootstrapped(self):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        return os.path.basename(exe_dir).lower() == "deck coach"

    def create_bootstrap_bat(self, source_exe_path):
        """
        source_exe_path = full path to the currently running exe
        """
        source_dir = os.path.dirname(os.path.abspath(source_exe_path))
        target_dir = os.path.join(source_dir, "Deck Coach")


        exe_name = os.path.basename(source_exe_path)
        target_exe_path = os.path.join(target_dir, exe_name)

        bat_path = os.path.join(os.getcwd(), "bootstrap.bat")

        with open(bat_path, "w") as f:
            f.write(f"""@echo off
    echo Bootstrapping Deck Coach...

    REM Give the app time to fully exit
    timeout /t 3 /nobreak >nul

    REM Wait until the EXE is no longer running
    :wait
    tasklist /FI "IMAGENAME eq {exe_name}" 2>NUL | find /I "{exe_name}" >NUL
    if not errorlevel 1 (
        timeout /t 2 /nobreak >nul
        goto wait
    )

    REM Copy EXE to Deck_Coach folder
    copy /Y "{source_exe_path}" "{target_exe_path}"

    REM Verify copy succeeded
    if not exist "{target_exe_path}" (
        echo ERROR: Copy failed.
        pause
        exit /b 1
    )

    REM Delete original EXE
    del /F /Q "{source_exe_path}"

    REM Launch app from correct location
    start "" "{target_exe_path}"

    REM Delete this batch file
    del "%~f0"
    """)

class Update_Check_Screen(Screen):
    def on_enter(self):
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.status_label = Label(
            text='Checking for updates...',
            font_size=24
        )
        layout.add_widget(self.status_label)
        self.add_widget(layout)

        # Run update check in background thread
        threading.Thread(
            target=self.check_for_updates,
            daemon=True
        ).start()

    # -----------------------------
    # Background thread
    # -----------------------------
    def check_for_updates(self):
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"

        try:
            response = requests.get(
                url,
                timeout=10,
                headers={'User-Agent': 'DeckCoach-Kivy-App'}
            )
            response.raise_for_status()
            data = response.json()
            latest_version = data['tag_name'].lstrip('v')

            Clock.schedule_once(
                lambda dt: self.on_update_check_complete(latest_version, data)
            )

        except Exception as e:
            Clock.schedule_once(
                lambda dt: self.on_update_check_failed(str(e))
            )

    # -----------------------------
    # UI thread callbacks
    # -----------------------------
    def on_update_check_complete(self, latest_version, data):
        if latest_version == CURRENT_VERSION:
            self.goto_main_menu()
            return

        self.clear_widgets()

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        layout.add_widget(Label(
            text=f'New version available:\n{CURRENT_VERSION} -> {latest_version}',
            font_size=24
        ))

        layout.add_widget(Label(
            text=HARM_MESSAGE,
            font_size=18
        ))

        yes_btn = Button(text='Update Now', size_hint=(1, None), height=80)
        no_btn = Button(text='Skip', size_hint=(1, None), height=80)

        yes_btn.bind(on_press=lambda *_: self.install_update(data))
        no_btn.bind(on_press=lambda *_: self.goto_main_menu())

        layout.add_widget(yes_btn)
        layout.add_widget(no_btn)

        self.add_widget(layout)

    def on_update_check_failed(self, error):
        # Fail gracefully — never block app startup
        print(f'Update check failed: {error}')
        self.goto_main_menu()

    # -----------------------------
    # Navigation
    # -----------------------------
    def goto_main_menu(self):
        self.manager.current = 'main'

    # -----------------------------
    # Update install logic
    # -----------------------------
    def install_update(self, data):
        for asset in data.get("assets", []):
            if asset["name"] == APP_NAME:
                self.download_update(asset["browser_download_url"])

        self.create_update_bat()
        subprocess.Popen(
            [os.path.join(os.getcwd(), "update.bat")],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        sleep(1)
        os._exit(0)

    def download_update(self, url):
        run_dir = os.path.dirname(os.path.abspath(sys.executable))

        staging_dir = os.path.join(run_dir, "_update")
        os.makedirs(staging_dir, exist_ok=True)

        exe_path = os.path.join(staging_dir, APP_NAME)

        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(exe_path, "wb") as f:
                for chunk in r.iter_content(8192):
                    if chunk:
                        f.write(chunk)

    def create_update_bat(self):
        exe_name = APP_NAME
        run_dir = os.path.dirname(os.path.abspath(sys.executable))

        bat_path = os.path.join(run_dir, "update.bat")

        with open(bat_path, "w") as f:
            f.write(f"""@echo off
    echo Applying update...
    timeout /t 3 /nobreak >nul

    :wait
    tasklist /FI "IMAGENAME eq {exe_name}" | find /I "{exe_name}" >nul
    if not errorlevel 1 (
        timeout /t 2 /nobreak >nul
        goto wait
    )

    del /f "{exe_name}"
    move /y "_update\\{exe_name}" "{exe_name}"

    rmdir /s /q "_update"
    del "%~f0"
    """)

# Fully Functional
class Main_Menu(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
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

        old_path = '../Decks'
        if os.path.exists(old_path) and os.path.isdir(old_path):
            shutil.move(old_path, './')
            sleep(2)
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
# Fully Functional
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
        self.manager.current = 'view_cards_screen'
    def goto_add_cards(self, instance):
        self.manager.current = 'add_cards_screen'
    def goto_edit_cards(self, instance):
        self.manager.current = 'edit_cards_screen'
    def goto_track_cards(self, instance):
        self.manager.current = 'track_cards_screen'
    def go_back(self, instance):
        self.manager.current = 'deck_menu'
# Fully Functional
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
        self.manager.current = 'view_tracked_cards_stats_screen'
    def go_back(self, instance):
        self.manager.current = 'deck_menu'
# Fully Functional
class Game_Stats_Menu(Screen):
    def on_enter(self, **kwargs):
        super().__init__(**kwargs)
        self.clear_widgets()
        self.update_path()
        self.gf_hand_btn_text = ''
        self.gf_hand_btn = Button()
        self.gf_hand_option()
        self.gf_hand_btn = Button(text=self.gf_hand_btn_text, size_hint=(1, None), height=50)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        
        lands_per_game_btn = Button(text='Lands per Game', size_hint=(1, None), height=50)
        game_length_btn = Button(text='Game Length', size_hint=(1, None), height=50)
        win_rate_btn = Button(text='Win Rate', size_hint=(1, None), height=50)
        cards_drawn_btn = Button(text='Cards Drawn', size_hint=(1, None), height=50)
        back_btn = Button(text='Back', size_hint=(1, None), height=50)

        if self.gf_hand_btn_text != '':
            self.gf_hand_btn.bind(on_press=self.view_opening_hand_stats)
            layout.add_widget(self.gf_hand_btn)

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
    def gf_hand_option(self):
        pass
    def view_opening_hand_stats(self, instance):
        pass
    def update_path(self):
        app = App.get_running_app()
        self.path = 'Decks/' + app.deck_name + '/game_stats.json'
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
            fail_label = Label(text='Unable to open Game Stats or Goldfish Stats file.\nThe file will not exist if you have not played games via the life counter.', font_size=sp(24))
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
        self.decklist_path = 'Decks/' + app.deck_name + '/deck_list.json'

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
        Window.bind(on_key_down=self.on_key_down)
        

        layout.add_widget(win_btn)
        layout.add_widget(back_btn)
        layout.add_widget(lose_btn)

        self.add_widget(layout)

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        print(key)
        if key == 256:
            self.go_back(key)
        elif key == 257:
            self.values['Life'] -= 1
            self.value_labels['Life'].text = str(self.values['Life'])
        elif key == 258:
            self.values['Life'] += 1
            self.value_labels['Life'].text = str(self.values['Life'])
        elif key == 260:
            self.values['Turn'] += 1
            self.value_labels['Turn'].text = str(self.values['Turn'])
        elif key == 261:
            self.values['Draws'] += 1
            self.value_labels['Draws'].text = str(self.values['Draws'])
        elif key == 262:
            self.values['Lands'] += 1
            self.value_labels['Lands'].text = str(self.values['Lands'])
        elif key == 263:
            self.values['Exp'] += 1
            self.value_labels['Exp'].text = str(self.values['Exp'])
        elif key == 264:
            class Win:
                text = 'Win'
            self.end_game(Win)
        elif key == 265:
            class Lose:
                text = 'Lose'
            self.end_game(Lose)


    def decrement(self, instance):
        name = instance.row_name
        print(name)
        self.values[name] -= 1
        self.value_labels[name].text = str(self.values[name])
    def increment(self, instance):
        name = instance.row_name
        print(name)
        self.values[name] += 1
        self.value_labels[name].text = str(self.values[name])
    def go_back(self, instance):
        self.manager.current = 'deck_menu'
    
    def end_game(self, instance):
        result = instance.text

        # ---- save game stats ----
        try:
            with open(self.path, 'r') as file:
                games_list = json.load(file)
        except:
            games_list = []

        game = {'result': result}
        game.update(self.values)
        games_list.append(game)

        with open(self.path, 'w') as file:
            json.dump(games_list, file, indent=4)

        # ---- load deck list ----
        try:
            with open(self.decklist_path, 'r') as file:
                self.deck_list = json.load(file)
        except:
            self.manager.current = 'deck_menu'
            return

        # ---- collect tracked cards ----
        self.tracked_cards = [
            card for card in self.deck_list
            if card.get('tracked', False)
        ]

        # ---- log win/loss stats ----
        for card in self.tracked_cards:
            card.setdefault('tracking', {'wins': [], 'win_turns': [], 'survey': []})
            card['tracking']['wins'].append(1 if result == 'Win' else 0)
            if result == 'Win':
                card['tracking']['win_turns'].append(self.values['Turn'])

        self.current_card_index = 0

        if self.tracked_cards:
            self.ask_played_card()
        else:
            self.finish_tracking()

    def ask_played_card(self):
        self.clear_widgets()

        self.card = self.tracked_cards[self.current_card_index]

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(
            text=f"Did you play with {self.card['name']} this game?",
            font_size=24
        )

        yes_btn = Button(text='Yes', size_hint=(1, None), height=50)
        no_btn = Button(text='No', size_hint=(1, None), height=50)

        yes_btn.bind(on_press=self.ask_rating)
        no_btn.bind(on_press=self.next_card)

        layout.add_widget(label)
        layout.add_widget(yes_btn)
        layout.add_widget(no_btn)

        self.add_widget(layout)

    def ask_rating(self, instance):
        self.clear_widgets()

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(
            text=f"Rate {self.card['name']} this game (1–5)",
            font_size=24
        )

        layout.add_widget(label)

        for i in range(1, 6):
            btn = Button(text=str(i), size_hint=(1, None), height=50)
            btn.bind(on_press=self.save_rating)
            layout.add_widget(btn)

        self.add_widget(layout)

    def save_rating(self, instance):
        rating = int(instance.text)
        self.card['tracking']['survey'].append(rating)
        self.next_card(instance)

    def next_card(self, instance):
        self.current_card_index += 1

        if self.current_card_index < len(self.tracked_cards):
            self.ask_played_card()
        else:
            self.finish_tracking()

    def finish_tracking(self):
        with open(self.decklist_path, 'w') as file:
            json.dump(self.deck_list, file, indent=4)

        self.manager.current = 'deck_menu'
# Fully Functional
class Goldfish_Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.mullcount = 0
    
    def on_enter(self):
        self.clear_widgets()

        app = App.get_running_app()
        self.path = 'Decks/' + app.deck_name + '/goldfish_stats.json'
        self.gfh_path = 'Decks/' + app.deck_name + '/goldfish_hand_stats.json'

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
            'Lands':0,
            'Castable Cards':0
        }

        self.mulled_lands = []
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

        name = 'Cards Kept'
        self.values[name] = 7
        value_label = Label(text=str(self.values[name]))
        value_label.row_name = name
        self.value_labels[name] = value_label
        name_label = Label(text=name)

        keep_btn = Button(text='Keep', size_hint=(1, None), height=50)
        back_btn = Button(text='Back', size_hint=(1, None), height=50)
        mull_btn = Button(text='Mulligan', size_hint=(1, None), height=50)

        keep_btn.bind(on_press=self.end_gf_hand)
        mull_btn.bind(on_press=self.end_gf_hand)
        back_btn.bind(on_press=self.go_back)

        layout.add_widget(mull_btn)
        layout.add_widget(value_label)
        layout.add_widget(keep_btn)
        layout.add_widget(name_label)
        layout.add_widget(back_btn)

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

    def end_gf_hand(self, instance):
        # Keep
        if instance.text == 'Keep':

            try:
                with open(self.gfh_path, 'r') as file:
                    games_list = json.load(file)
            except:
                games_list = []
            self.values['mulled_lands'] = self.mulled_lands
            games_list.append(self.values)
            with open(self.gfh_path, 'w') as file:
                json.dump(games_list, file, indent=4)

            self.manager.current = 'deck_menu'
        # Mulligan
        else:
            self.values['Cards Kept'] -= self.mullcount
            if self.mullcount < 1:self.mullcount += 1
            self.value_labels['Cards Kept'].text = str(self.values['Cards Kept'])
            self.mulled_lands.append(self.values['Lands'])
            self.values['Lands'] = 0
            self.values['Castable Cards'] = 0
            self.value_labels['Lands'].text = '0'
            self.value_labels['Castable Cards'].text = '0'



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
        game['Damage'] = 120 - game['Damage']
        games_list.append(game)
        
        try:
            with open(self.path, 'w') as file:
                json.dump(games_list, file, indent=4)
        except Exception as e:
            print('Houston we have a problem ', e)

        self.manager.current = 'deck_menu'
# Fully Functional
class Track_Cards_Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.tracking_label = Label()
        instructions_label = Label(
            text='Enter the name of a card to set for tracking (TAB to autocomplete)',
            font_size=24
        )

        self.input_box = TextInput(
            multiline=False,
            size_hint=(1, None),
            height=50
        )

        self.submit_btn = Button(text='Submit', size_hint=(1, None), height=50)
        back_btn = Button(text='Back', size_hint=(1, None), height=50)

        self.submit_btn.bind(on_press=self.set_tracking)
        back_btn.bind(on_press=self.go_back)

        layout.add_widget(self.tracking_label)
        layout.add_widget(instructions_label)
        layout.add_widget(self.input_box)
        layout.add_widget(self.submit_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

        # --- AUTOCOMPLETE STATE ---
        self.card_names = []
        self._matches = []
        self._match_index = 0

        # Reset matches when typing
        orig_insert = self.input_box.insert_text

        def insert_text_hook(substring, from_undo=False):
            self._reset_matches()
            return orig_insert(substring, from_undo)

        self.input_box.insert_text = insert_text_hook

        Window.bind(on_key_down=self._on_key_down)

    def on_enter(self):
        app = App.get_running_app()
        self.path = f'Decks/{app.deck_name}/deck_list.json'
        self.load_card_names()

    # -----------------------------
    # AUTOCOMPLETE LOGIC
    # -----------------------------

    def load_card_names(self):
        self.card_names.clear()
        try:
            with open(self.path, 'r') as file:
                deck_list = json.load(file)
                for card in deck_list:
                    name = card.get('name')
                    if name:
                        self.card_names.append(name)
        except:
            pass

    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        # TAB key
        if key != 9:
            return False

        if not self.input_box.focus:
            return False

        self.autocomplete_name()
        return True  # consume TAB

    def autocomplete_name(self):
        text = self.input_box.text
        cursor_index = self.input_box.cursor_index()
        fragment = text[:cursor_index].lower().strip()

        if not fragment:
            return

        if not self._matches:
            self._matches = [
                name for name in self.card_names
                if name.lower().startswith(fragment)
            ]
            self._match_index = 0

        if not self._matches:
            return

        match = self._matches[self._match_index]
        self._match_index = (self._match_index + 1) % len(self._matches)

        self.input_box.text = match
        self.input_box.cursor = self.input_box.get_cursor_from_index(len(match))

    def _reset_matches(self):
        self._matches = []
        self._match_index = 0

    # -----------------------------
    # BUTTON HANDLERS
    # -----------------------------

    def set_tracking(self, instance):
        try:
            with open(self.path, 'r') as file:
                deck_list = json.load(file)
        except:
            self.tracking_label.text = 'No cards added to deck list'
            sleep(2)
            self.go_back()
            return

        input_name = self.input_box.text.lower().strip()

        for card in deck_list:
            if input_name == card.get('name', '').lower():
                if not card.get('tracked', False):
                    card['tracking'] = {'wins': [], 'win_turns': [], 'survey': []}
                    card['tracked'] = True
                    self.tracking_label.text = f'{card["name"]} set for tracking!'
                else:
                    card['tracked'] = False
                    self.tracking_label.text = f'{card["name"]} deselected for tracking!'
                break

        self.input_box.text = ''
        self._reset_matches()

        with open(self.path, 'w') as file:
            json.dump(deck_list, file, indent=4)

    def go_back(self, instance):
        self.manager.current = 'deck_list_menu'
# Fully Functional
class Add_Cards_Screen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main layout for all widgets
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.main_layout)

        self.added_label = Label()
        name_label = Label(text='Card Name', font_size=24)
        self.name_text = TextInput(multiline=False, size_hint=(1, None), height=50)
        tags_label = Label(text='Tags', font_size=24)
        instructions_label = Label(
            text="Enter each tag separated by a comma ',' (TAB to autocomplete)",
            font_size=20
        )
        self.tags_text = TextInput(multiline=True, size_hint=(1, None), height=80)

        # Hook for tab completion
        orig_insert = self.tags_text.insert_text
        def insert_text_hook(substring, from_undo=False):
            self._reset_matches()
            return orig_insert(substring, from_undo)
        self.tags_text.insert_text = insert_text_hook

        # Buttons
        self.submit_btn = Button(text='Submit', size_hint=(1, None), height=50)
        self.back_btn = Button(text='Back', size_hint=(1, None), height=50)
        self.submit_btn.bind(on_press=self.submit_card)
        self.back_btn.bind(on_press=self.go_back)

        # Layout widgets
        self.main_layout.add_widget(self.added_label)
        self.main_layout.add_widget(name_label)
        self.main_layout.add_widget(self.name_text)
        self.main_layout.add_widget(tags_label)
        self.main_layout.add_widget(instructions_label)
        self.main_layout.add_widget(self.tags_text)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=50)
        btn_layout.add_widget(self.submit_btn)
        btn_layout.add_widget(self.back_btn)
        self.main_layout.add_widget(btn_layout)

        # ---------------- Tab Completion ----------------
        self.known_tags = set()
        self._matches = []
        self._match_index = 0
        Window.bind(on_key_down=self._on_key_down)

    # -----------------------------
    # Kivy Lifecycle
    # -----------------------------
    def on_enter(self):
        app = App.get_running_app()
        self.path = f'Decks/{app.deck_name}/deck_list.json'
        self.load_existing_tags()

    # -----------------------------
    # TAB COMPLETION LOGIC
    # -----------------------------
    def load_existing_tags(self):
        """Load tags from existing deck_list.json"""
        self.known_tags.clear()
        try:
            with open(self.path, 'r') as file:
                deck_list = json.load(file)
                for card in deck_list:
                    for tag in card.get('tags', []):
                        self.known_tags.add(tag.lower())
        except:
            pass

    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key != 9:  # TAB
            return False
        if not self.tags_text.focus:
            return False
        self.autocomplete_tag()
        return True

    def autocomplete_tag(self):
        text = self.tags_text.text
        cursor_index = self.tags_text.cursor_index()
        start = text.rfind(',', 0, cursor_index) + 1
        fragment = text[start:cursor_index].strip().lower()
        if not fragment:
            return
        if not self._matches:
            self._matches = sorted(tag for tag in self.known_tags if tag.startswith(fragment))
            self._match_index = 0
        if not self._matches:
            return
        match = self._matches[self._match_index]
        self._match_index = (self._match_index + 1) % len(self._matches)
        prefix = ' ' if start > 0 and text[start] == ' ' else ''
        new_text = text[:start] + prefix + match + text[cursor_index:]
        self.tags_text.text = new_text
        new_cursor = start + len(prefix) + len(match)
        self.tags_text.cursor = self.tags_text.get_cursor_from_index(new_cursor)

    def _reset_matches(self):
        self._matches = []
        self._match_index = 0

    # -----------------------------
    # BUTTON HANDLERS
    # -----------------------------
    def submit_card(self, instance):
        try:
            with open(self.path, 'r') as file:
                deck_list = json.load(file)
        except:
            deck_list = []

        name = self.name_text.text.strip()
        tags = [t.strip().lower() for t in self.tags_text.text.split(',') if t.strip()]
        card = {'name': name, 'tags': tags}

        deck_list.append(card)
        self.known_tags.update(tags)

        self.added_label.text = f'{name} added!'
        self.name_text.text = ''
        self.tags_text.text = ''
        self._reset_matches()

        with open(self.path, 'w') as file:
            json.dump(deck_list, file, indent=4)

    def go_back(self, instance):
        self.manager.current = 'deck_list_menu'
# Fully Functional
class View_Cards_Screen(Screen):
    def on_enter(self):
        self.clear_widgets()

        app = App.get_running_app()
        path = f'Decks/{app.deck_name}/deck_list.json'

        try:
            with open(path, 'r') as file:
                deck_list = json.load(file)
        except:
            self.manager.current = 'deck_list_menu'
            return

        root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        scroll = ScrollView(size_hint=(1, 1))

        list_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10
        )
        list_layout.bind(minimum_height=list_layout.setter('height'))

        for index, card in enumerate(deck_list):
            btn = Button(
                text=card['name'],
                size_hint_y=None,
                height=40
            )
            btn.card_index = index
            btn.bind(on_press=self.open_edit)

            list_layout.add_widget(btn)

        scroll.add_widget(list_layout)

        back_btn = Button(text='Back', size_hint=(1, None), height=50)
        back_btn.bind(on_press=self.go_back)

        root_layout.add_widget(scroll)
        root_layout.add_widget(back_btn)

        self.add_widget(root_layout)

    def open_edit(self, instance):
        edit_screen = self.manager.get_screen('edit_cards_screen')
        edit_screen.card_index = instance.card_index
        self.manager.current = 'edit_cards_screen'

    def go_back(self, instance):
        self.manager.current = 'deck_list_menu'
# Fully Functional
class Edit_Cards_Screen(Add_Cards_Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Change submit button text
        self.submit_btn.text = 'Save Changes'

        # Add delete button next to submit/back
        self.delete_btn = Button(text='Delete Card', size_hint=(1, None), height=50)
        self.delete_btn.bind(on_press=self.delete_card)
        self.main_layout.children[0].add_widget(self.delete_btn)  # add to btn layout (first child)

        # Track the card index
        self.card_index = None

    # -----------------------------
    # Load existing card for editing
    # -----------------------------
    def load_card(self, card_index):
        self.card_index = card_index
        app = App.get_running_app()
        path = f'Decks/{app.deck_name}/deck_list.json'
        try:
            with open(path, 'r') as file:
                deck_list = json.load(file)
        except:
            deck_list = []

        if 0 <= card_index < len(deck_list):
            card = deck_list[card_index]
            self.name_text.text = card.get('name', '')
            self.tags_text.text = ', '.join(card.get('tags', []))
            self.load_existing_tags()
        else:
            self.name_text.text = ''
            self.tags_text.text = ''

    # -----------------------------
    # Save changes
    # -----------------------------
    def submit_card(self, instance):
        app = App.get_running_app()
        path = f'Decks/{app.deck_name}/deck_list.json'
        try:
            with open(path, 'r') as file:
                deck_list = json.load(file)
        except:
            deck_list = []

        if self.card_index is None or not (0 <= self.card_index < len(deck_list)):
            return

        deck_list[self.card_index]['name'] = self.name_text.text.strip()
        deck_list[self.card_index]['tags'] = [
            t.strip().lower() for t in self.tags_text.text.split(',') if t.strip()
        ]

        self.known_tags.update(deck_list[self.card_index]['tags'])

        with open(path, 'w') as file:
            json.dump(deck_list, file, indent=4)

        self.added_label.text = f"{self.name_text.text.strip()} updated!"

    # -----------------------------
    # Delete card
    # -----------------------------
    def delete_card(self, instance):
        app = App.get_running_app()
        path = f'Decks/{app.deck_name}/deck_list.json'
        try:
            with open(path, 'r') as file:
                deck_list = json.load(file)
        except:
            deck_list = []

        if self.card_index is None or not (0 <= self.card_index < len(deck_list)):
            return

        deleted_name = deck_list[self.card_index]['name']
        del deck_list[self.card_index]

        with open(path, 'w') as file:
            json.dump(deck_list, file, indent=4)

        self.added_label.text = f"{deleted_name} deleted!"
        self.name_text.text = ''
        self.tags_text.text = ''
        self.card_index = None

    def on_pre_enter(self):
        if self.card_index is not None:
            self.load_card(self.card_index)
# Fully Functional
class View_Tracked_Cards_Stats_Screen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    def on_enter(self):
        self.clear_widgets()

        root_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        scroll = ScrollView(size_hint=(1, 1))

        list_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10
        )
        list_layout.bind(minimum_height=list_layout.setter('height'))

        app = App.get_running_app()
        dl_path = 'Decks/' + app.deck_name + '/deck_list.json'
        gs_path = 'Decks/' + app.deck_name + '/game_stats.json'

        try:
            with open(dl_path, 'r') as file:
                self.deck_list = json.load(file)
            with open(gs_path, 'r') as file:
                self.games_list = json.load(file)
        except Exception as e:
            print(e)
            self.manager.current = 'view_stats_menu'
            return

        for index, card in enumerate(self.deck_list):
            if 'tracked' in card and card['tracked'] == True:
                btn = Button(
                    text=card['name'],
                    size_hint_y=None,
                    height=40
                )
                btn.card_index = index
                btn.bind(on_press=self.view_tracked_card_stats)

                list_layout.add_widget(btn)

        scroll.add_widget(list_layout)

        back_btn = Button(text='Back', size_hint=(1, None), height=50)
        back_btn.bind(on_press=self.go_back)

        root_layout.add_widget(scroll)
        root_layout.add_widget(back_btn)

        self.add_widget(root_layout)

    def go_back(self, instatnce):
        self.manager.current = 'view_stats_menu'

    def view_tracked_card_stats(self, instance):

        win_rate_list = []
        win_turn_list = []

        for game in self.games_list:
            if game['result'] == 'Win':
                win_turn_list.append(game['Turn'])
                win_rate_list.append(1)
            else: win_rate_list.append(0)

        card_index = instance.card_index
        if 0 <= card_index < len(self.deck_list):
            card = self.deck_list[card_index]

        if sum(win_rate_list) != 0 and win_rate_list != []:
            win_rate_average = (sum(win_rate_list) / len(win_rate_list)) * 100
        else: win_rate_average = 0

        if sum(win_turn_list) != 0 and win_turn_list != []:
            win_turn_average = (sum(win_turn_list) / len(win_turn_list))
        else: win_turn_average = 0

        if sum(card['tracking']['wins']) != 0 and card['tracking']['wins'] != []:
            tracked_win_rate_average = (sum(card['tracking']['wins']) / len(card['tracking']['wins']) * 100)
        else: tracked_win_rate_average = 0

        if sum(card['tracking']['win_turns']) != 0 and card['tracking']['win_turns'] != []:
            tracked_win_turn_average = sum(card['tracking']['win_turns']) / len(card['tracking']['win_turns'])
        else: tracked_win_turn_average = 0

        if sum(card['tracking']['survey']) != 0 and card['tracking']['survey'] != []:
            survey_average = sum(card['tracking']['survey']) / len(card['tracking']['survey'])
            self.survey_text = f'Your average rating of {card['name']} out of 5 is {survey_average}'
        else: self.survey_text = f'No Surveys taken with {card['name']}'        

        self.win_rate_text = f'Your overall win rate is %{win_rate_average},'
        self.win_rate_text_pt2 = f'Your win rate with {card['name']} is %{tracked_win_rate_average}'
        self.win_turn_text = f'Your average win occurns on turn {win_turn_average},'
        self.win_turn_text_pt2 = f'Your average win with {card['name']} occurs on turn {tracked_win_turn_average}'

        self.clear_widgets()        

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        win_rate_label = Label(text=self.win_rate_text, font_size=24)
        win_rate_label_pt2 = Label(text=self.win_rate_text_pt2, font_size=24)
        win_turn_label = Label(text=self.win_turn_text, font_size=24)
        win_turn_label_pt2 = Label(text=self.win_turn_text_pt2, font_size=24)
        survey_label = Label(text=self.survey_text, font_size=24)
        back_btn = Button(text='Back', size_hint=(1, None), height=50)

        back_btn.bind(on_press=self.reload)

        layout.add_widget(win_rate_label)
        layout.add_widget(win_rate_label_pt2)
        layout.add_widget(win_turn_label)
        layout.add_widget(win_turn_label_pt2)
        layout.add_widget(survey_label)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def reload(self, instance):
        self.on_enter()
# Fully Functional
class Goldfish_Stats_Menu(Game_Stats_Menu):
    def __init__(self, **kw):
        super().__init__(**kw)

        

    def update_path(self):
        app = App.get_running_app()
        self.path = 'Decks/' + app.deck_name + '/goldfish_stats.json' 

    def gf_hand_option(self):
        self.gf_hand_btn_text = 'Opening Hand Stats'
        

    def view_opening_hand_stats(self, instance):
        app = App.get_running_app()
        self.path = 'Decks/' + app.deck_name + '/goldfish_hand_stats.json'
        try:
            with open(self.path, 'r') as file:
                hands_list = json.load(file)
        except Exception as e: 
            print(e)
            self.manager.current = 'view_stats_menu'
            hands_list = []

        kept_cards = []
        mulled_lands = []
        kept_castable =[]
        kept_lands = []


        for hand in hands_list:
            kept_lands.append(hand['Lands'])
            kept_cards.append(hand['Cards Kept'])
            kept_castable.append(hand['Castable Cards'])
            for entry in hand['mulled_lands']:
                mulled_lands.append(entry)
            


        average_castable = self.get_average(kept_castable)
        castable_str = f'Your average keepable hand contains {average_castable} castable cards'

        average_cards_kept = self.get_average(kept_cards)
        cards_kept_str = f'Your average hand contains {average_cards_kept} cards.'

        average_kept_lands = self.get_average(kept_lands)
        lands_kept_str = f'Your average keepable hand contains {average_kept_lands} lands.'

        total_lands = kept_lands + mulled_lands
        average_lands = self.get_average(total_lands)
        total_lands_str = f'Your average hand contains {average_lands} lands.'

        if len(total_lands) != 0:
            keep_percent = (len(kept_lands) / len(total_lands)) * 100 
        else: keep_percent = 0
        keep_percent_str = f'Your percentage of keepable hands is %{keep_percent}'

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        castable_label = Label(text=castable_str, font_size=24)
        cards_kept_label = Label(text=cards_kept_str, font_size=24)
        lands_kept_label = Label(text=lands_kept_str, font_size=24)
        total_lands_label = Label(text=total_lands_str, font_size=24)
        keep_percent_label = Label(text=keep_percent_str, font_size=24)
        back_btn = Button(text='Back', size_hint=(1, None), height=50)
        back_btn.bind(on_press=self.reload)

        layout.add_widget(keep_percent_label)
        layout.add_widget(cards_kept_label)
        layout.add_widget(total_lands_label)
        layout.add_widget(lands_kept_label)
        layout.add_widget(castable_label)
        layout.add_widget(back_btn)

        self.clear_widgets()
        self.add_widget(layout)


    def get_average(self, lst):
        if sum(lst) != 0 and lst != []:
            average_lst = sum(lst) / len(lst)
        else: average_lst = 0
        return average_lst
    

CURRENT_VERSION = "2.0.1"
HARM_MESSAGE = 'Devs at Schwandtsylvania are proud to bring you a new GUI version of deck coach with fancy screens and buttons!\n' \
'Your auto updater should take care of everything for you!' \
'Just be sure to re run the app if it closes the first time'

OWNER = "Schwandt-Dev"
REPO = "Deck_Coach"
APP_NAME = "Deck_Coach.exe"

############################### CHANGE LOG #########################################
   # View tracked cards now only shows tracked cards.
   # Added hot keys to Life Counter
####################################################################################

################################## TODO ############################################
    # add chopping block file
        # all cards start on the chopping block
        # cards with shoutouts are removed 
        # lands are removed
        # cards with least tags will rank highest on the chopping block
            # sub sort by cost high to low
        # identify veggies (card draw, removal) and remove from the chopping block
    # add feature to view games played in Deck Coach 
        #need to be able to delete bad stats that might be stored in game stats
    # ship to andriod
    # add option to view tags and edit
    # add hot keys for menu and game buttons
####################################################################################  



if __name__ == "__main__":
    Deck_Coach().run()