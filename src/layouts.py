from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class DynamicLayoutApp(App):
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        add_button = Button(text="Add New Section", size_hint=(1, None), height=50)
        add_button.bind(on_press=self.add_section)
        self.main_layout.add_widget(add_button)

        return self.main_layout

    def add_section(self, instance):
        # Create a new horizontal layout dynamically
        new_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        new_layout.add_widget(Label(text="New Section Label"))
        new_layout.add_widget(Button(text="Click Me"))

        # Add the new layout to the main layout
        self.main_layout.add_widget(new_layout)

if __name__ == "__main__":
    DynamicLayoutApp().run()
