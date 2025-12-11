# main.py
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')

import os
import json
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

DECKS_DIR = "decks"


# -------------------------------
# Main Menu Screen
# -------------------------------
class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", spacing=10, padding=16)

        new_deck_btn = Button(text="New Deck", size_hint=(1, 0.1))
        new_deck_btn.bind(on_press=self.go_new_deck)
        root.add_widget(new_deck_btn)

        # Dynamic deck list in a scrollview
        self.deck_scroll = ScrollView(size_hint=(1, 0.75))
        self.deck_list = GridLayout(cols=1, size_hint_y=None, spacing=8, padding=(0,8))
        self.deck_list.bind(minimum_height=self.deck_list.setter('height'))
        self.deck_scroll.add_widget(self.deck_list)
        root.add_widget(self.deck_scroll)

        exit_btn = Button(text="Exit", size_hint=(1, 0.1))
        exit_btn.bind(on_press=self.exit_app)
        root.add_widget(exit_btn)

        self.add_widget(root)

    def on_pre_enter(self, *args):
        self.refresh_deck_list()

    def refresh_deck_list(self):
        self.deck_list.clear_widgets()
        os.makedirs(DECKS_DIR, exist_ok=True)
        decks = sorted(os.listdir(DECKS_DIR))
        if not decks:
            self.deck_list.add_widget(Label(text="No decks found.", size_hint_y=None, height=40))
            return
        for deck in decks:
            btn = Button(text=deck, size_hint_y=None, height=60)
            btn.bind(on_press=lambda inst, d=deck: self.open_deck(d))
            self.deck_list.add_widget(btn)

    def open_deck(self, deck_name):
        deck_menu = self.manager.get_screen("deck_menu")
        deck_menu.set_deck(deck_name)
        self.manager.current = "deck_menu"

    def go_new_deck(self, instance):
        self.manager.current = "new_deck"

    def exit_app(self, instance):
        App.get_running_app().stop()


# -------------------------------
# New Deck Screen
# -------------------------------
class NewDeckScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", spacing=10, padding=20)

        self.input_name = TextInput(hint_text="Enter new deck name", multiline=False, size_hint=(1, 0.1))
        root.add_widget(self.input_name)

        create_btn = Button(text="Create Deck", size_hint=(1, 0.1))
        create_btn.bind(on_press=self.create_deck)
        root.add_widget(create_btn)

        back_btn = Button(text="Back", size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_back)
        root.add_widget(back_btn)

        self.status = Label(text="", size_hint=(1, 0.1))
        root.add_widget(self.status)

        self.add_widget(root)

    def create_deck(self, instance):
        name = self.input_name.text.strip()
        if not name:
            self.status.text = "Enter a valid name."
            return
        path = os.path.join(DECKS_DIR, name)
        os.makedirs(path, exist_ok=True)
        # initialize stats files if absent
        gf_file = os.path.join(path, "goldfish_stats.json")
        lc_file = os.path.join(path, "lifecounter_stats.json")
        if not os.path.exists(gf_file):
            with open(gf_file, "w") as f:
                json.dump([], f)
        if not os.path.exists(lc_file):
            with open(lc_file, "w") as f:
                json.dump([], f)
        self.input_name.text = ""
        self.manager.current = "main"

    def go_back(self, instance):
        self.manager.current = "main"


# -------------------------------
# Deck Menu Screen
# -------------------------------
class DeckMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.deck_name = None
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", spacing=10, padding=20)

        self.deck_label = Label(text="", font_size=28, size_hint=(1, 0.1))
        root.add_widget(self.deck_label)

        gf_btn = Button(text="Goldfish (Stats)", size_hint=(1, 0.12))
        gf_btn.bind(on_press=self.on_goldfish)
        root.add_widget(gf_btn)

        # Renamed Life Counter button to "Enter Game Stats"
        lc_btn = Button(text="Enter Game Stats", size_hint=(1, 0.12))
        lc_btn.bind(on_press=self.on_life_counter)
        root.add_widget(lc_btn)

        stats_btn = Button(text="View Stats", size_hint=(1, 0.12))
        stats_btn.bind(on_press=self.on_view_stats)
        root.add_widget(stats_btn)

        imp_btn = Button(text="Import Deck (placeholder)", size_hint=(1, 0.12))
        imp_btn.bind(on_press=self.on_import)
        root.add_widget(imp_btn)

        back_btn = Button(text="Back to Main Menu", size_hint=(1, 0.12))
        back_btn.bind(on_press=self.go_back)
        root.add_widget(back_btn)

        self.add_widget(root)

    def set_deck(self, deck_name):
        self.deck_name = deck_name
        self.deck_label.text = f"Deck: {deck_name}"

    def on_goldfish(self, instance):
        gold = self.manager.get_screen("goldfish")
        gold.set_deck(self.deck_name)
        self.manager.current = "goldfish"

    def on_life_counter(self, instance):
        # Open the lifecounter screen (identical UI but saves to separate file)
        lc = self.manager.get_screen("lifecounter")
        lc.set_deck(self.deck_name)
        self.manager.current = "lifecounter"

    def on_view_stats(self, instance):
        vs = self.manager.get_screen("view_stats")
        vs.set_deck(self.deck_name)
        self.manager.current = "view_stats"

    def on_import(self, instance):
        print(f"Import placeholder for deck: {self.deck_name}")

    def go_back(self, instance):
        self.manager.current = "main"


# -------------------------------
# Unified Stats Screen UI builder helper
# -------------------------------
def build_stats_ui(root_layout, stats_keys, stat_update_callback, save_callback, back_callback):
    """
    Builds and returns a dict of widgets for a stats UI given:
      - root_layout: parent layout to which the UI will be added
      - stats_keys: ordered list of stat names
      - stat_update_callback(key, delta): function to call when +/- pressed
      - save_callback(): bound to Save Game button
      - back_callback(): bound to Back button

    Returns:
      dict with references: {'labels': {key: Label}, 'life_label': Label}
    """
    widgets = {}
    layout = BoxLayout(orientation="vertical", spacing=8, padding=12)
    # Deck title placeholder (the caller should place a deck label above if needed)
    # Life row
    life_row = BoxLayout(orientation="horizontal", spacing=6, size_hint_y=None, height=68)
    life_label = Label(text="Life: 40", font_size=28)
    widgets['life_label'] = life_label

    # small buttons around life
    minus1 = Button(text="-1", size_hint=(0.18, 1))
    minus1.bind(on_press=lambda inst: stat_update_callback("Life", -1))
    plus1 = Button(text="+1", size_hint=(0.18, 1))
    plus1.bind(on_press=lambda inst: stat_update_callback("Life", 1))

    # optional larger step buttons (kept minimal)
    minus5 = Button(text="-5", size_hint=(0.18, 1))
    minus5.bind(on_press=lambda inst: stat_update_callback("Life", -5))
    plus5 = Button(text="+5", size_hint=(0.18, 1))
    plus5.bind(on_press=lambda inst: stat_update_callback("Life", 5))

    # arrange: -5, -1, label, +1, +5
    life_row.add_widget(minus5)
    life_row.add_widget(minus1)
    life_row.add_widget(life_label)
    life_row.add_widget(plus1)
    life_row.add_widget(plus5)
    layout.add_widget(life_row)

    # Stats list (scrollable)
    stats_grid = GridLayout(cols=1, size_hint_y=None, spacing=6)
    stats_grid.bind(minimum_height=stats_grid.setter('height'))
    sv = ScrollView(size_hint=(1, 0.68))
    sv.add_widget(stats_grid)
    layout.add_widget(sv)

    widgets['labels'] = {}
    for key in stats_keys:
        if key == "Life":
            continue
        row = BoxLayout(orientation="horizontal", spacing=6, size_hint_y=None, height=52)
        lbl = Label(text=f"{key}: 0", font_size=20)
        widgets['labels'][key] = lbl
        row.add_widget(lbl)
        inc = Button(text="+1", size_hint=(0.18, 1))
        inc.bind(on_press=lambda inst, k=key: stat_update_callback(k, 1))
        dec = Button(text="-1", size_hint=(0.18, 1))
        dec.bind(on_press=lambda inst, k=key: stat_update_callback(k, -1))
        row.add_widget(inc)
        row.add_widget(dec)
        stats_grid.add_widget(row)

    # Save and Back buttons
    save_btn = Button(text="Save Game (append & reset)", size_hint=(1, 0.08))
    save_btn.bind(on_press=save_callback)
    layout.add_widget(save_btn)

    back_btn = Button(text="Back to Deck Menu", size_hint=(1, 0.08))
    back_btn.bind(on_press=back_callback)
    layout.add_widget(back_btn)

    root_layout.add_widget(layout)
    return widgets


# -------------------------------
# Goldfish Screen (saves to goldfish_stats.json)
# -------------------------------
class GoldfishScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.deck_name = None
        self.stats = {
            "Life": 40,
            "Cards Drawn": 0,
            "Lands Played": 0,
            "Mulligans": 0,
            "Experience Counters": 0,
            "Spells Cast": 0,
            "Turn Count": 0
        }
        self.widgets = {}
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", spacing=6, padding=8)

        self.deck_label = Label(text="", font_size=22, size_hint=(1, 0.08))
        root.add_widget(self.deck_label)

        keys = list(self.stats.keys())
        self.widgets = build_stats_ui(
            root,
            keys,
            stat_update_callback=self.update_stat,
            save_callback=self.save_game,
            back_callback=self.go_back
        )

        self.add_widget(root)

    def set_deck(self, deck_name):
        self.deck_name = deck_name
        self.deck_label.text = f"Deck: {deck_name}"
        # start fresh each time (do not load previous session)
        self.stats = {
            "Life": 40,
            "Cards Drawn": 0,
            "Lands Played": 0,
            "Mulligans": 0,
            "Experience Counters": 0,
            "Spells Cast": 0,
            "Turn Count": 0
        }
        self.refresh_display()

    def update_stat(self, key, delta):
        if key not in self.stats:
            return
        # ensure non-negative for these stats (except life can go negative)
        if key == "Life":
            self.stats[key] += delta
        else:
            self.stats[key] = max(0, self.stats[key] + delta)
        self.refresh_display()

    def refresh_display(self):
        # update life label
        life_lbl = self.widgets.get('life_label')
        if life_lbl:
            life_lbl.text = f"Life: {self.stats['Life']}"
        # update other labels
        for k, lbl in self.widgets.get('labels', {}).items():
            lbl.text = f"{k}: {self.stats.get(k,0)}"

    def save_game(self, instance):
        if not self.deck_name:
            return
        deck_path = os.path.join(DECKS_DIR, self.deck_name)
        os.makedirs(deck_path, exist_ok=True)
        stats_file = os.path.join(deck_path, "goldfish_stats.json")

        all_sessions = []
        if os.path.exists(stats_file):
            try:
                with open(stats_file, "r") as f:
                    all_sessions = json.load(f)
            except Exception:
                all_sessions = []

        session = self.stats.copy()
        session["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        all_sessions.append(session)

        with open(stats_file, "w") as f:
            json.dump(all_sessions, f, indent=2)

        # reset stats
        self.stats = {
            "Life": 40,
            "Cards Drawn": 0,
            "Lands Played": 0,
            "Mulligans": 0,
            "Experience Counters": 0,
            "Spells Cast": 0,
            "Turn Count": 0
        }
        self.refresh_display()

    def go_back(self, instance):
        self.manager.current = "deck_menu"


# -------------------------------
# Life Counter Screen (identical UI but saves to lifecounter_stats.json)
# -------------------------------
class LifeCounterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.deck_name = None
        self.stats = {
            "Life": 40,
            "Cards Drawn": 0,
            "Lands Played": 0,
            "Mulligans": 0,
            "Experience Counters": 0,
            "Spells Cast": 0,
            "Turn Count": 0
        }
        self.widgets = {}
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", spacing=6, padding=8)

        self.deck_label = Label(text="", font_size=22, size_hint=(1, 0.08))
        root.add_widget(self.deck_label)

        keys = list(self.stats.keys())
        self.widgets = build_stats_ui(
            root,
            keys,
            stat_update_callback=self.update_stat,
            save_callback=self.save_game,
            back_callback=self.go_back
        )

        self.add_widget(root)

    def set_deck(self, deck_name):
        self.deck_name = deck_name
        self.deck_label.text = f"Deck: {deck_name}"
        # start fresh each time
        self.stats = {
            "Life": 40,
            "Cards Drawn": 0,
            "Lands Played": 0,
            "Mulligans": 0,
            "Experience Counters": 0,
            "Spells Cast": 0,
            "Turn Count": 0
        }
        self.refresh_display()

    def update_stat(self, key, delta):
        if key not in self.stats:
            return
        if key == "Life":
            self.stats[key] += delta
        else:
            self.stats[key] = max(0, self.stats[key] + delta)
        self.refresh_display()

    def refresh_display(self):
        life_lbl = self.widgets.get('life_label')
        if life_lbl:
            life_lbl.text = f"Life: {self.stats['Life']}"
        for k, lbl in self.widgets.get('labels', {}).items():
            lbl.text = f"{k}: {self.stats.get(k,0)}"

    def save_game(self, instance):
        if not self.deck_name:
            return
        deck_path = os.path.join(DECKS_DIR, self.deck_name)
        os.makedirs(deck_path, exist_ok=True)
        stats_file = os.path.join(deck_path, "lifecounter_stats.json")

        all_sessions = []
        if os.path.exists(stats_file):
            try:
                with open(stats_file, "r") as f:
                    all_sessions = json.load(f)
            except Exception:
                all_sessions = []

        session = self.stats.copy()
        session["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        all_sessions.append(session)

        with open(stats_file, "w") as f:
            json.dump(all_sessions, f, indent=2)

        # reset stats
        self.stats = {
            "Life": 40,
            "Cards Drawn": 0,
            "Lands Played": 0,
            "Mulligans": 0,
            "Experience Counters": 0,
            "Spells Cast": 0,
            "Turn Count": 0
        }
        self.refresh_display()

    def go_back(self, instance):
        self.manager.current = "deck_menu"


# -------------------------------
# View Stats Screen (choose which file type to view)
# -------------------------------
class ViewStatsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.deck_name = None
        self.current_type = "goldfish"  # or "lifecounter"
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", spacing=8, padding=12)

        self.deck_label = Label(text="", font_size=22, size_hint=(1, 0.08))
        root.add_widget(self.deck_label)

        # selector buttons
        selector = BoxLayout(size_hint=(1, 0.08), spacing=6)
        btn_gf = Button(text="Show Goldfish Sessions")
        btn_gf.bind(on_press=lambda inst: self.select_type("goldfish"))
        btn_lc = Button(text="Show Enter Game Stats Sessions")
        btn_lc.bind(on_press=lambda inst: self.select_type("lifecounter"))
        selector.add_widget(btn_gf)
        selector.add_widget(btn_lc)
        root.add_widget(selector)

        # sessions list
        self.scroll = ScrollView(size_hint=(1, 0.76))
        self.list_grid = GridLayout(cols=1, size_hint_y=None, spacing=6)
        self.list_grid.bind(minimum_height=self.list_grid.setter('height'))
        self.scroll.add_widget(self.list_grid)
        root.add_widget(self.scroll)

        back_btn = Button(text="Back to Deck Menu", size_hint=(1, 0.08))
        back_btn.bind(on_press=self.go_back)
        root.add_widget(back_btn)

        self.add_widget(root)

    def set_deck(self, deck_name):
        self.deck_name = deck_name
        self.deck_label.text = f"Sessions for: {deck_name}"
        self.select_type("goldfish")

    def select_type(self, t):
        if t not in ("goldfish", "lifecounter"):
            t = "goldfish"
        self.current_type = t
        self.load_and_display()

    def load_and_display(self):
        self.list_grid.clear_widgets()
        filename = "goldfish_stats.json" if self.current_type == "goldfish" else "lifecounter_stats.json"
        stats_file = os.path.join(DECKS_DIR, self.deck_name, filename)
        if not os.path.exists(stats_file):
            self.list_grid.add_widget(Label(text="No sessions found.", size_hint_y=None, height=40))
            return
        try:
            with open(stats_file, "r") as f:
                sessions = json.load(f)
        except Exception:
            sessions = []

        if not sessions:
            self.list_grid.add_widget(Label(text="No sessions found.", size_hint_y=None, height=40))
            return

        for s in reversed(sessions):  # newest first
            ts = s.get("timestamp", "unknown time")
            box = BoxLayout(orientation="vertical", size_hint_y=None, height=160, padding=6)
            box.add_widget(Label(text=f"Session: {ts}", size_hint_y=None, height=30))
            for key in ["Life", "Turn Count", "Cards Drawn", "Lands Played", "Mulligans", "Experience Counters", "Spells Cast"]:
                box.add_widget(Label(text=f"{key}: {s.get(key, 0)}", size_hint_y=None, height=20))
            self.list_grid.add_widget(box)

    def go_back(self, instance):
        self.manager.current = "deck_menu"


# -------------------------------
# App and ScreenManager
# -------------------------------
class DeckApp(App):
    def build(self):
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(MainMenu(name="main"))
        sm.add_widget(NewDeckScreen(name="new_deck"))
        sm.add_widget(DeckMenuScreen(name="deck_menu"))
        sm.add_widget(GoldfishScreen(name="goldfish"))
        sm.add_widget(LifeCounterScreen(name="lifecounter"))
        sm.add_widget(ViewStatsScreen(name="view_stats"))
        return sm


if __name__ == "__main__":
    DeckApp().run()
