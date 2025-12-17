from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import os


class Deck_Coach(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.path = 'Decks/' #set base path
        try:
            decks_list = os.listdir(self.path)
        except:
            os.mkdir(self.path)
            decks_list = os.listdir(self.path)
        
        buttons = [('New Deck', self.new_deck)]
        exit_btn = ('Exit', self.exit_app)
        for i in range(len(decks_list)):
            deck_btn = (decks_list[i], self.deck_selection)
            buttons.append(deck_btn)
        buttons.append(exit_btn)

        for text, callback in buttons:
            btn = Button(text=text, size_hint=(1, None), height=50)
            btn.bind(on_press=callback)
            self.layout.add_widget(btn)
        return self.layout
    
    def new_deck(self, instance):
        self.create_deck_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text="Enter a name for your new deck")
        self.create_deck_layout.add_widget(popup_label)
        self.txtbox = TextInput(multiline=False, size_hint=(1, None), height=40)
        self.create_deck_layout.add_widget(self.txtbox)
        submit_btn = Button(text='Submit', size_hint=(1, None), height=50)
        submit_btn.bind(on_press=self.submit_name)
        self.create_deck_layout.add_widget(submit_btn)
        self.layout.add_widget(self.create_deck_layout)

    def exit_app(self, instance):
        print('Exiting...')
        self.stop()

    def deck_selection(self, instance):
        print(instance.text, 'Clicked!')

    def submit_name(self, instance):
        new_deck_btn = Button(text=self.txtbox.text, size_hint=(1, None), height=50)
        new_deck_btn.bind(on_press=self.deck_selection)
        self.layout.add_widget(new_deck_btn)

        self.layout.remove_widget(self.create_deck_layout)
        try:
            os.mkdir(self.path + self.txtbox.text)
        except:
            print("Houston we have a problem")


if __name__ == "__main__":
    Deck_Coach().run()