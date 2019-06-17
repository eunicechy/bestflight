import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class Selection(GridLayout):
    def __init__(self, **kwargs):
        super(Selection,self).__init__(**kwargs)
        self.add_widget(
            CheckBox()
        )

class MyApp(App):
    def build(self):
        root = Selection()
        return root


if __name__ == '__main__':
    MyApp().run()