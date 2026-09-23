from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

class US30Bot(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='US30 BOT', font_size=40))
        layout.add_widget(Label(text='Build Success! APK Working!', font_size=20))
        layout.add_widget(Label(text='Next: Add Charts & Signals', font_size=16))
        return layout

US30Bot().run()
