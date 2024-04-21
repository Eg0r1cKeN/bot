from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from kivy.core.window import Window

Window.clearcolor = (120 / 255, 133 / 255, 139 / 255, 1)
Window.fullscrean = 'auto'

class MyApp(App):

    def __init__(self):
        super().__init__()
        self.label = Label(text='Моя программа\nВсе работает!', pos=(444, 100))

    def build(self):
        box = BoxLayout()

        box.add_widget(self.label)
        return box


if __name__ == "__main__":
    MyApp().run()
