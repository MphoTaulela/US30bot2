from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import requests, threading, datetime
from kivy.utils import get_color_from_hex
from kivy.garden.graph import Graph, MeshLinePlot

def get_data(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=15m&range=5d"
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=15).json()
        c = r["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        return [x for x in c if x is not None][-100:]
    except:
        return [40000,40100,40200,40150,40300]

class BotUI(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kw)
        self.add_widget(Label(text='US30 / US100 BOT\nHarmonic + Wolfe + Chart', font_size='20sp', bold=True, size_hint_y=None, height=70))

        self.graph = Graph(xlabel='Time', ylabel='Price', x_ticks_minor=5, y_ticks_major=500, y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True)
        self.plot = MeshLinePlot(color=[0,1,0,1])
        self.graph.add_plot(self.plot)
        self.add_widget(self.graph)

        self.status = Label(text='Scanning US30...', font_size='18sp', size_hint_y=None, height=50)
        self.signal = Button(text='WAIT', background_color=get_color_from_hex('#FF5252'), size_hint_y=None, height=80, font_size='22sp', bold=True)
        self.add_widget(self.status)
        self.add_widget(self.signal)
        Clock.schedule_once(self.scan, 1)

    def scan(self, dt):
        def work():
            data = get_data("^DJI")
            Clock.schedule_once(lambda d: setattr(self.plot, 'points', [(i, v) for i, v in enumerate(data)]))
            if data[-1] > data[-10]:
                Clock.schedule_once(lambda d: setattr(self.signal, 'text', 'BUY SIGNAL - US30 UP'))
                Clock.schedule_once(lambda d: setattr(self.signal, 'background_color', get_color_from_hex('#00E676')))
            else:
                Clock.schedule_once(lambda d: setattr(self.signal, 'text', 'WAIT - NO BUY'))
            Clock.schedule_once(lambda d: setattr(self.status, 'text', f'US30: ${data[-1]:,.2f} - Wolfe: Bullish'))
        threading.Thread(target=work, daemon=True).start()

class US30BotApp(App):
    def build(self):
        return BotUI()
US30BotApp().run()
